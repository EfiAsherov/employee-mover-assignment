import sys
from src.employee_mover import EmployeeMover
from src.extract_employee import EmployeeDataExtractor
import tests.test_employees_data as test_employees_data

def get_args():
    try:
        return (
            sys.argv[1] if (sys.argv[1][-5:] == '.xlsx') else sys.argv[1] + ".xlsx",
            sys.argv[2] if (sys.argv[2][-5:] == '.xlsx') else sys.argv[2] + ".xlsx",
            sys.argv[3] if (sys.argv[3][-5:] == '.xlsx') else sys.argv[3] + ".xlsx",
            float(sys.argv[4]),
            int(sys.argv[5])
        )
    except: raise ValueError("some of the arguments are incorrect")

def main():
    employees_data_file, output_file, expected_result_file, default_currency_val, default_register_id_val = get_args()

    employee_mover = EmployeeMover(employees_data_file, output_file, default_currency_val, default_register_id_val)
    employee_mover.move_employees()
    
    expected_data = EmployeeDataExtractor(expected_result_file)
    expected_data.extract_employees_data(read_only=True)

    test_employees_data.test_employees_data(employee_mover.employees, expected_data.employees, default_currency_val, default_register_id_val)


if __name__ == '__main__':
    main()