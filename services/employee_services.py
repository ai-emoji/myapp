import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepository()

    def get_all_employees(self):
        return self.repo.get_all()

    def get_employees_by_department(self, department_id):
        return self.repo.get_by_department(department_id)

    def get_employee_by_id(self, emp_id):
        return self.repo.get_by_id(emp_id)

    def add_employee(
        self,
        name,
        department_id=None,
        job_title_id=None,
        employee_code=None,
        gender=None,
        hire_date=None,
        attendance_code=None,
        attendance_name=None,
        date_of_birth=None,
        birthplace=None,
        hometown=None,
        id_number=None,
        id_place_issued=None,
        ethnicity=None,
        nationality=None,
        current_address=None,
        phone_number=None,
        emergency_contact=None,
    ):
        # Không cho phép tên trống
        if not name or not name.strip():
            log_to_debug(f"EmployeeService: Tên nhân viên trống")
            return False
        return self.repo.add(
            name,
            department_id,
            job_title_id,
            employee_code,
            gender,
            hire_date,
            attendance_code,
            attendance_name,
            date_of_birth,
            birthplace,
            hometown,
            id_number,
            id_place_issued,
            ethnicity,
            nationality,
            current_address,
            phone_number,
            emergency_contact,
        )

    def update_employee(
        self,
        emp_id,
        name,
        department_id=None,
        job_title_id=None,
        employee_code=None,
        gender=None,
        hire_date=None,
        attendance_code=None,
        attendance_name=None,
        date_of_birth=None,
        birthplace=None,
        hometown=None,
        id_number=None,
        id_place_issued=None,
        ethnicity=None,
        nationality=None,
        current_address=None,
        phone_number=None,
        emergency_contact=None,
    ):
        # Không cho phép tên trống
        if not name or not name.strip():
            log_to_debug(f"EmployeeService: Tên nhân viên trống")
            return False
        return self.repo.update(
            emp_id,
            name,
            department_id,
            job_title_id,
            employee_code,
            gender,
            hire_date,
            attendance_code,
            attendance_name,
            date_of_birth,
            birthplace,
            hometown,
            id_number,
            id_place_issued,
            ethnicity,
            nationality,
            current_address,
            phone_number,
            emergency_contact,
        )

    def delete_employee(self, emp_id):
        try:
            return self.repo.delete(emp_id)
        except Exception as e:
            log_to_debug(
                f"EmployeeService: delete_employee() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def count(self):
        return self.repo.count()

    def is_employee_code_exists(self, employee_code, exclude_emp_id=None):
        """Kiểm tra xem mã nhân viên đã tồn tại chưa"""
        return self.repo.is_employee_code_exists(employee_code, exclude_emp_id)
