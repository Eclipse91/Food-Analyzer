import os
import json
import logging
import requests
from dotenv import load_dotenv
import util
from create_db import FoodDatabase
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, exc, inspect, text, select, func
from sqlalchemy.exc import SQLAlchemyError


# Adda list of valid foods. Check example_corrected_foods.txt or directly the USDA Site
CORRECTED_FOODS = 'example_corrected_foods.txt' # 'example_corrected_foods.txt'

def convert_to_mg(data):
    '''
    Convert data to mg if necessary.
    '''
    processed_data = []
    for mineral, value, unit in data:
        if unit == 'µg':
            value_mg = value / 1000  # Convert µg to mg
        elif unit == 'g':
            value_mg = value * 1000  # Convert g to mg
        else:
            value_mg = value
        processed_data.append([mineral, value_mg])
    
    return processed_data

def list_to_dict(data):
    '''
    Transform a list into a dictionary in order to convert it into a pandas DataFrame.
    '''
    food_dict = {}
    for item in data:
        key = item[0]
        value = item[1]
        food_dict[key] = value
    return food_dict

def get_record_count(connection, table):
    '''
    Get the count of records in a specified database table.
    '''
    count_stmt = select((func.count())).select_from(table)
    result = connection.execute(count_stmt)
    count = result.scalar()
    return count

def save_to_db(df, table_name, db_path='sqlite:///food_components.db'):
    '''
    Save a DataFrame into its specific table in food_components.db.
    '''
    logging.info('Starting save_to_db function')
    engine = create_engine(db_path)
    meta = MetaData()
    inspector = inspect(engine)

    # Define initial columns (assuming 'Food' as the primary key)
    initial_columns = [Column('Food', String, primary_key=True)]
    for col in df.columns:
        if col != 'Food':
            initial_columns.append(Column(col, Float))

    logging.info('Initial columns for table')

    with engine.connect() as connection:
        # Check if the table exists
        if not connection.dialect.has_table(connection, table_name):
            # Define the table schema
            table = Table(table_name, meta, *initial_columns, extend_existing=True)
            # Create table in database if it doesn't exist
            try:
                meta.create_all(engine)
                logging.info('Table created successfully')
            except exc.SQLAlchemyError as e:
                logging.error(f'Error creating table {table_name}: {e}')
        else:
            logging.info('Table already exists')
            # Get existing columns
            existing_columns = inspector.get_columns(table_name)
            existing_column_names = [col['name'] for col in existing_columns]
            logging.info('Existing columns')

            # Find new columns to add
            new_columns = []
            for col in df.columns:
                if col not in existing_column_names:
                    new_columns.append(Column(col, String))
            
            logging.info('New columns to add')

            # Add new columns if any
            if new_columns:
                for column in new_columns:
                    alter_stmt = text(f'ALTER TABLE {table_name} ADD COLUMN "{column.name}" FLOAT')
                    try:
                        connection.execute(alter_stmt)
                        logging.info(f'Added column {column.name} to table {table_name}')
                    except exc.SQLAlchemyError as e:
                        logging.error(f'Error adding column {column.name}: {e}')

                # Update existing rows with default values for new columns
                for column in new_columns:
                    update_stmt = text(f'UPDATE {table_name} SET "{column.name}" = "0"')
                    try:
                        connection.execute(update_stmt)
                        logging.info(f'Updated existing rows with default value for column {column.name}')
                    except exc.SQLAlchemyError as e:
                        logging.error(f'Error updating existing rows for column {column.name}: {e}')

        # Insert or update the records
        table = Table(table_name, meta, autoload_with=engine)

    # Insert or update the record
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            # Count records before insertion
            count_before = get_record_count(connection, table)
            logging.info(f'Record count before insertion: \t{count_before}')

            for _, row in df.iterrows():
                data = row.to_dict()
                # Convert all data to string
                data = {key: str(value) for key, value in data.items()}
                logging.info('Data to insert:', data)
                stmt = table.insert().values(data).prefix_with('OR REPLACE')
                logging.info('SQL Statement')
                connection.execute(stmt)
            transaction.commit()
            logging.info(f'Data {data["Food"]} inserted successfully to "{table_name}"')

            # Count records after insertion
            count_after = get_record_count(connection, table)
            logging.info(f'Record count after insertion: \t\t{count_after}')

            if count_after == count_before:
                raise SQLAlchemyError('Record count did not change after insertion')

        except SQLAlchemyError as e:
            transaction.rollback()
            logging.error(f'Error inserting data "{table_name}": {e}')

    logging.info(f'Completed save_to_db function of "{table_name}"')

def save_to_csv(data, file_path):
    '''
    Save a DataFrame to food_components.csv.
    '''
    if os.path.exists(file_path):
        # If the file exists, read it into a DataFrame
        existing_data = pd.read_csv(file_path)
        # Append the new data, aligning columns and filling missing values with NaN
        combined_data = pd.concat([existing_data, data], ignore_index=True)
        # Save the combined DataFrame back to the CSV file
        combined_data.to_csv(file_path, mode='w', header=True, index=False)
    else:
        # If the file does not exist, create it and write the header
        data.to_csv(file_path, mode='w', header=True, index=False)

def reduce_json(original_json):
    # Extract the description
    reduced_json = {
        "description": original_json.get("description", "")
    }

    # Extract the relevant nutrient information
    reduced_json["foodNutrients"] = [
        {
            "nutrientName": nutrient.get("nutrientName", ""),
            "unitName": nutrient.get("unitName", ""),
            "value": nutrient.get("value", 0.0)
        }
        for nutrient in original_json.get("foodNutrients", [])
    ]

    return reduced_json

def json_to_list_of_lists(reduced_json):
    # Start with the 'Food' and description
    result = [["Food", reduced_json.get("description", "")]]

    # Add each nutrient's information
    for nutrient in reduced_json.get("foodNutrients", []):
        nutrient_list = [
            nutrient.get("nutrientName", ""),
            nutrient.get("value", 0.0),
            nutrient.get("unitName", "")
        ]
        result.append(nutrient_list)

    return result

def search_single_food_usda(query, API_KEY):
    '''
    Searches for a specific food item in the USDA FoodData Central database.
    This function sends a GET request to the USDA FoodData Central API
    using the /foods/search endpoint. It retrieves detailed nutritional 
    information for the first food item that matches the given query.
    '''
    search_url = f'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': API_KEY,
        'query': query,
        'dataType': 'Foundation, SR Legacy',
        'pageSize': 1
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        food_data = response.json()
        if food_data['totalHits'] > 0:
            return food_data['foods'][0]
        else:
            return 'No results found.'
    else:
        return f"Error: {response.status_code}"
    
def read_file(file_path):
    '''
    Read the files with the foods or URLs and return their content as a list.
    '''
    with open(file_path, 'r') as file:
        variables = [line.strip() for line in file.readlines()]

    return variables    

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_food_list(API_KEY, page_number, page_size):
    '''
    Retrieves a list of foods from the USDA FoodData Central database.
    This function sends a GET request to the USDA FoodData Central API
    using the /foods/list endpoint. It returns a paginated list of food items 
    along with their descriptions and FDC IDs.
    '''
    list_url = 'https://api.nal.usda.gov/fdc/v1/foods/list'
    
    params = {
        'api_key': API_KEY,
        'pageNumber': page_number,
        'pageSize': page_size,
    }
    
    response = requests.get(list_url, params=params) # + API_KEY + '&page_size=49')
    
    if response.status_code == 200:
        try:
            food_data = response.json()
            return food_data
        except Exception as e:
            logging.error(f"Data Error: {e}")
    else:
        logging.error(f"Error, status code: {response.status_code}")
    
    return []

def search_all_foods_usda(query, API_KEY):
    '''
    Searches for a specific food item in the USDA FoodData Central database.
    This function sends a GET request to the USDA FoodData Central API
    using the /foods/search endpoint. It retrieves detailed nutritional 
    information for all food items that match the given query.
    '''
    search_url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    all_foods = []
    page_number = 1
    page_size = 50  # Adjust this number as needed

    while True:
        params = {
            'api_key': API_KEY,
            'query': query,
            'dataType': 'Foundation, SR Legacy',
            'pageSize': page_size,
            'pageNumber': page_number
        }
        
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            food_data = response.json()
            if food_data['totalHits'] > 0:
                all_foods.extend(food_data['foods'])
                if len(food_data['foods']) < page_size:
                    break  # Exit loop if fewer results than page size
            else:
                break  # No more results
        else:
            return f"Error: {response.status_code}"
        
        page_number += 1  # Move to the next page
    
    if all_foods:
        return all_foods
    else:
        return 'No results found.'

def save_data(food_data, food_item):
    food_data = reduce_json(food_data)
    food_data = json_to_list_of_lists(food_data)
    food_data = convert_to_mg(food_data[1:])
    food_data.insert(0, ['Food', food_item])
    food_data = list_to_dict(food_data)
    print(food_data)
    write_to_json(food_data, './jsons/' + food_item + '.json')

    food_data = pd.DataFrame([food_data])
    save_to_db(food_data, 'foods_data', 'sqlite:///food_components.db')
    save_to_csv(food_data, 'food_components.csv')
    
    save_to_csv(food_data, 'csvs/' + food_item + '.csv')

    logging.info(f'Inserted Food:{food_item}')

@util.execution_time
def main():
    # Configure
    # Configure and initialize the logger file
    log_file = util.log_configurator()
    logging.info(f'Logger configured: {log_file}')
    
    util.jsons_configurator()
    util.csvs_configurator()

    logging.info('Program started')

    # # Configure the folder where to put the results
    # results_folder = util.results_configurator()

    # Create instance of the class and run the process
    food_db = FoodDatabase()
    food_db.run()

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the USDA API Key from environment variables
    API_KEY = os.getenv('USDA_API_KEY')

    # Read eated foods or the corrected Version or None of them
    if CORRECTED_FOODS == '':
        foods = read_file('foods.txt')

        # Create corrected foods from foods.txt
        corrected_foods = []
        for food in foods:
            results = search_all_foods_usda(food, API_KEY)
            if isinstance(results, list):
                try:
                    for result in results:
                        corrected_foods.append(result['description'])
                except:
                    logging.error(f'Issues adding: {result}')
            else:
                logging.error(f'Food not found: {food}')
                logging.error(f'Food not found: {results}')

        with open('example_corrected_foods.txt', 'a') as file:
            for food in corrected_foods:
                file.write(f"{food}\n")
    else:
        foods = read_file(CORRECTED_FOODS)

    for food in foods:
        # food = 'Fish, salmon, chinook, raw'
        food_data = search_single_food_usda(food, API_KEY)
        save_data(food_data, food)

    logging.info('Program ended successfully')


if __name__ == '__main__':
    # unique_foods_creator()
    main()