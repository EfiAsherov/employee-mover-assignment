import openpyxl
import src.design_xlsx_file_data as design_data

num_of_failed_assertions = 0
output_curr = expected_curr = 1
default_currency = default_register_id = None
number_of_expected_employees = 0
small_inaccuracy_data = moderte_inaccuracy_data = high_inaccuracy_data = 0
num_of_registered_id_inaccuracy = num_of_default_registered_id = 0
currency_inaccuracy = num_of_default_currencies = 0

def test_employees_data(output_employees_data, expected_employees_data, default_currency_val, default_register_id_val):
    compared_results = []
    missing_employees_data = []
    global default_currency, default_register_id, output_curr, expected_curr, number_of_expected_employees
    default_currency, default_register_id = default_currency_val, default_register_id_val
    number_of_expected_employees = len(expected_employees_data)
    for test_id, expected_employee in expected_employees_data.items():
        if test_id not in output_employees_data:
            missing_employees_data.append([test_id, expected_employee])
            continue
        output_curr = output_employees_data[test_id].currency
        expected_curr = expected_employee.currency
        
        assertions = [
            lambda: assert_name(output_employees_data[test_id].name, expected_employee.name),
            lambda: assert_age(output_employees_data[test_id].age, expected_employee.age),
            lambda: assert_currency(output_curr, expected_curr),
            lambda: assert_cash(output_employees_data[test_id].cash, expected_employee.cash),
            lambda: assert_id(output_employees_data[test_id].registered_id, expected_employee.registered_id)
        ]

        for assertion in assertions:
            try:
                assertion()
            except AssertionError as e:
                compared_results.append([test_id]+e.args[0])
            
    create_file_from_compared_results(compared_results)
    if len(missing_employees_data)!=0:
        create_file_from_missing_employees_data(missing_employees_data)


def assert_name(output_name: str, expected_name: str):
    assert output_name == expected_name, ["name", output_name, expected_name, design_compared_results('name')]
    
def assert_age(output_age: int, expected_age: int):
    assert output_age == expected_age, ["age", output_age, expected_age, design_compared_results('age')]
    
def assert_currency(output_currency: float, expected_currency: float):
    assert output_currency == expected_currency,\
         ["currency", output_currency, expected_currency,\
             design_compared_results('currency/cash', output_currency, expected_currency)
        ]
    
def assert_cash(output_cash: float, expected_cash: float):
    assert output_cash == expected_cash,\
         ["cash", output_cash, expected_cash,\
             design_compared_results('currency/cash', output_curr, expected_curr)
        ]
    
def assert_id(output_registered_id: int, expected_registered_id: int):
    assert output_registered_id == expected_registered_id,\
         ["registered_id", output_registered_id, expected_registered_id,\
            design_compared_results('registered_id', output_registered_id, expected_registered_id)
        ]

def design_compared_results(field, output=None, expected=None):
    match field:
        case "name":
            return [get_and_increment_num_of_failed_assertions()+1, 'left']
        case "age":
            return [get_and_increment_num_of_failed_assertions()+1]
        case "currency/cash":
            return compare_difference(output,expected, 0.1, 0.5)
        case "registered_id":
            return compare_register_id_differrence(output)

def get_and_increment_num_of_failed_assertions():
    global num_of_failed_assertions
    num_of_failed_assertions += 1
    return num_of_failed_assertions

def compare_difference(output, expected, lower_threshold, mid_threshold):
    global small_inaccuracy_data, moderte_inaccuracy_data, high_inaccuracy_data, num_of_default_currencies, currency_inaccuracy
    currency_inaccuracy += 1

    if output == default_currency:
        num_of_default_currencies += 1
        return [get_and_increment_num_of_failed_assertions()+1, 'right', '0000FF']
    elif expected - lower_threshold <= output <= expected + lower_threshold:
        small_inaccuracy_data += 1
        return [get_and_increment_num_of_failed_assertions()+1, 'right', '008000']
    elif expected - mid_threshold <= output <= expected + mid_threshold:
        moderte_inaccuracy_data += 1
        return [get_and_increment_num_of_failed_assertions()+1, 'right', 'FFA500']
    else:
        high_inaccuracy_data += 1
        return [get_and_increment_num_of_failed_assertions()+1, 'right', 'FF0000']

def compare_register_id_differrence(output_register_id):
    global num_of_default_registered_id, num_of_registered_id_inaccuracy, high_inaccuracy_data
    num_of_registered_id_inaccuracy += 1

    if output_register_id == default_register_id:
        num_of_default_registered_id += 1
        return [get_and_increment_num_of_failed_assertions()+1, 'right', '0000FF']

    high_inaccuracy_data += 1
    return [get_and_increment_num_of_failed_assertions()+1, 'right', 'FF0000']

def create_file_from_compared_results(compared_results):
    compared_results_file = openpyxl.Workbook()
    compared_results_sheet = compared_results_file.active
    design_data.initiate_columns_titles(compared_results_sheet, ['test_id', 'field', 'output_value', 'expected_value'])
    for result in compared_results:
        row_to_append = result[:4]
        row_num = result[4][0]
        style_args = result[4][1:]
        compared_results_sheet.append(row_to_append)
        design_data.set_style(compared_results_sheet[row_num], 2, *style_args)
        design_data.seperate_lines(compared_results_sheet)

    design_data.set_width(compared_results_sheet)
    
    compared_results_file.save("./data/compared_results.xlsx")

    print("conclusions:")
    print(f"number of employees: {number_of_expected_employees}")
    print(f"number of inaccurate data: {num_of_failed_assertions}")
    print(f"high inaccuracy: {high_inaccuracy_data}")
    print(f"moderate inaccuracy: {moderte_inaccuracy_data}")
    print(f"small inaccuracy: {small_inaccuracy_data}")
    print(f"currency and cash inaccurency: {currency_inaccuracy}, from them {num_of_default_currencies//2} currencies got default value")
    print(f"registered id inaccurency: {num_of_registered_id_inaccuracy}, from them {num_of_default_registered_id} got default value")

def create_file_from_missing_employees_data(missing_employees_data):
    missing_employees_data_file = openpyxl.Workbook()
    missing_employees_data_sheet = missing_employees_data_file.active
    design_data.initiate_columns_titles(missing_employees_data_sheet, ['test_id', 'name', 'age', 'currency', 'converted_cash', 'registered_id'])
    for [test_id, employee] in missing_employees_data:
        missing_employees_data_sheet.append([test_id, employee.name, employee.age, employee.currency, employee.cash, employee.registered_id])
    
    design_data.set_width(missing_employees_data_sheet)
    missing_employees_data_file.save("./data/missing_employees_data.xlsx")
    
    print(f"number of missing employees data: {len(missing_employees_data)}")