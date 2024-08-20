import os
import json
# import yaml
import logging
import configparser
from datetime import datetime
from dotenv import load_dotenv, dotenv_values

def results_configurator() -> str:
    '''
    Configure the folder where to put all the resulting files.
    '''
    results_directory = './results/'
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
    folder_name = results_directory + formatted_datetime
    os.makedirs(folder_name, exist_ok=True)

    return folder_name

def jsons_configurator():
    '''
    Configure the folder where to put all the resulting jsons files.
    '''
    jsons_directory = './jsons/'
    os.makedirs(jsons_directory, exist_ok=True)

def csvs_configurator():
    '''
    Configure the folder where to put all the resulting csvs files.
    '''
    csvs_directory = './csvs/'
    os.makedirs(csvs_directory, exist_ok=True)

def log_configurator() -> str:
    '''
    Configure and initialize the logger.
    '''
    log_directory = './logs/'
    os.makedirs(log_directory, exist_ok=True)
    current_datetime = datetime.now()
    current_file_name = os.path.splitext(os.path.basename(__file__))[0]
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
    log_file = f'{log_directory}{current_file_name}_{formatted_datetime}.log'

    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    logging.info('Program started')

    return log_file

def load_json_config(config_path: str) -> dict:
    '''
    Load the json configuration file.
    '''
    try: 
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except:
        return {}

def load_ini_config(config_path: str) -> dict:
    '''
    Load the ini configuration file.
    '''
    config = configparser.ConfigParser()
    config.read(config_path)
    return {section: dict(config.items(section)) for section in config.sections()}

def load_env_file():
    '''
    Load the ini configuration file.
    '''
    if load_dotenv():
        return dotenv_values()
    
    return ''

def execution_time(func):
    '''
    Decorator that prints the current date and time before and after
    executing the given function, and measures the time taken for execution.
    '''
    def wrapper():
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
        print(f'Program started at {formatted_datetime}')
        func()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
        print(f'Program ended at {formatted_datetime}')

    return wrapper