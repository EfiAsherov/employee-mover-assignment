import ast
import openpyxl
import requests
from src.employee import Employee
from src.extract_employee import EmployeeDataExtractor
from concurrent.futures import ThreadPoolExecutor
import src.design_compared_data as design_data

class EmployeeMover(EmployeeDataExtractor):
    def __init__(self, employees_data_file: str, output_file: str, default_currency_val: float, default_register_id_val: int):
        super().__init__(employees_data_file)
        self.output_file = output_file
        self.default_currency_val = default_currency_val
        self.default_register_id_val = default_register_id_val

    def move_employees(self):
        super().extract_employees_data(read_only=True)
        self.save_to_output_file()
    
    def load_employee_data(self, data_cell) -> Employee:
        data = ast.literal_eval(data_cell[0].value)
        employee = Employee(**data)
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_currency = executor.submit(
                lambda: self.get_exchange_rate(data['currency'])
            ) 
            future_registered_id = executor.submit(
                lambda: self.get_register_id(employee.name, employee.age)
            )
        employee.currency = future_currency.result()
        employee.cash = self.convert_cash(data['cash'], employee.currency)
        employee.registered_id = future_registered_id.result()
        return employee

    def get_exchange_rate(self, currency: str) -> float:
        currency_request = requests.get("https://api.coinbase.com/v2/exchange-rates", )
        if 200 <= currency_request.status_code < 300:
            return float(currency_request.json()['data']['rates'][currency])
        else:
            return self.default_currency_val

    def get_register_id(self, name: str, age: int) -> int:
        register_id_request = requests.post("https://reqres.in/api/users", {"name" : name, "age" : age})
        if 200 <= register_id_request.status_code < 300:
            return register_id_request.json()['id']
        else:
            return self.default_register_id_val

    def convert_cash(self, cash: float, currency: float) -> float:
        return cash * currency

    def save_to_output_file(self):
        output_workbook = openpyxl.Workbook()
        output_sheet = output_workbook.active
        design_data.initiate_columns_titles(output_sheet, ['test_id', 'name', 'age', 'currency', 'converted_cash', 'registered_id'])
        self.output_employees_data(output_sheet)
        design_data.set_width(output_sheet)
        output_workbook.save(self.output_file)
    
    def output_employees_data(self, output_sheet):
        for test_id, employee in self.employees.items():
            output_sheet.append([test_id, employee.name, employee.age, employee.currency, employee.cash, employee.registered_id])
