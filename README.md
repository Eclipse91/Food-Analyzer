# Food Analyzer Project

## Overview

This script is designed to extract nutritional data from a given `foods.txt` file containing various foods, process the data to convert measurements into milligrams (mg), and save the data to a SQLite database. Any value is based on 100 grams of the product.

## Requirements

- Python 3.x
- Required Python packages are listed in the requirements.txt file.
- APY_KEY of U.S. Department of Agriculture

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Eclipse91/Food-Analyzer.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Food-Analyzer
   ```   

3. **Install the required dependencies** (creating a virtual environment is strongly recommended):
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file**: Include the following text in the file. Refer to the [Configuration](#configuration) section for detailed instructions on obtaining a valid API key.   
    USDA_API_KEY=_your_secret_key_

5. **Create a `foods.txt` file**: Add the foods you usually eat, one per line.

6. **Run the application**:
   ```bash
   python3 main.py
   ```

## Configuration

Ensure to set up your U.S. Department of Agriculture API key in the `.env` file:
- **Obtain Your API Key**: Visit [this link](https://fdc.nal.usda.gov/api-key-signup.html) and complete the form to receive your API key.
- **Set API Key in .env**: Open the .env file and add the following line, replacing your_API_Key with your actual API key (without quotation marks):

## Required Files

- `foods.txt`: A text file containing the list of foods you usually eat, one per line.

## Optional Files to Speed Up

- `corrected_foods.txt`: A text file containing the list of foods which you are sure are present in the U.S. Department of Agriculture database with that name. Add its path to the CORRECTED_FOODS constant in the main.py file.

## Usage

1. **Prepare file**: Ensure `foods.txt` is filled with the foods you eat regularly.
2. **Run the Script**:
   ```bash
   python3 main.py
   ```
3. **Compare the values in the db**: Check if some value is less than expected compared with your RDA.

## License
This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.

## Notes
Feel free to contribute or report issues! This README provides a clear structure, concise information, and instructions for setting up and running the Food Table Reader. Adjust the content as needed for your project.

## Acknowledgements
- [U.S. Department of Agriculture](https://fdc.nal.usda.gov/fdc-app.html#/food-search?query=&type=Foundation)
