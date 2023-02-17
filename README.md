## Installation
To download and install the required dependencies, run the following commands in the terminal:
* pip install openpyxl
* pip install requests
Or run the following command instead: pip install -r requirements.txt

## Running The Application
To run the application, open a terminal window and navigate to the project directory. Then, run the following command:
python main.py {test_input_path} {output_path} {expected_results_path} {default_currency_value} {default_register_id_value}

## Output
To see the result of the program, enter the data folder and see the compared results between the output and the expected file in the compared_results.xlsx file.
* red means high inaccurate data
* orange means moderate inaccurate data
* green means small inaccurate data
* blue means that this field got a default value, because an api failed request

## Running The Application Using Docker
To build the Docker container, open a terminal window and navigate to the project directory. 
Then, run the following command: docker build -t {image_name}

To run the Docker container use the following command: docker run -v {path_to_local_file}:/At-Bay-Assignment {image_name}
