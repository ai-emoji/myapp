import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


import duckdb
from core.database import Database


class EmployeeRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng employee nếu chưa tồn tại"""
        try:
            log_to_debug("EmployeeRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_employee START 1")
            except Exception:
                pass  # Sequence đã tồn tại

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS employee (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_employee'),
                    employee_code VARCHAR UNIQUE,
                    name VARCHAR NOT NULL,
                    department_id INTEGER,
                    job_title_id INTEGER,
                    gender VARCHAR,
                    hire_date DATE,
                    attendance_code VARCHAR,
                    attendance_name VARCHAR,
                    date_of_birth DATE,
                    birthplace VARCHAR,
                    hometown VARCHAR,
                    id_number VARCHAR,
                    id_place_issued VARCHAR,
                    ethnicity VARCHAR,
                    nationality VARCHAR,
                    current_address VARCHAR,
                    phone_number VARCHAR,
                    emergency_contact VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (department_id) REFERENCES department(id),
                    FOREIGN KEY (job_title_id) REFERENCES job_title(id)
                )
                """
            )

            con.close()
            log_to_debug("EmployeeRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_all(self):
        """Lấy tất cả nhân viên với đầy đủ thông tin"""
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """SELECT id, employee_code, name, department_id, job_title_id, gender, 
                   hire_date, attendance_code, attendance_name, date_of_birth, birthplace, 
                   hometown, id_number, id_place_issued, ethnicity, nationality, 
                   current_address, phone_number, emergency_contact 
                   FROM employee ORDER BY id ASC"""
            ).fetchall()
            con.close()
            return [
                {
                    "id": r[0],
                    "employee_code": r[1],
                    "name": r[2],
                    "department_id": r[3],
                    "job_title_id": r[4],
                    "gender": r[5],
                    "hire_date": r[6],
                    "attendance_code": r[7],
                    "attendance_name": r[8],
                    "date_of_birth": r[9],
                    "birthplace": r[10],
                    "hometown": r[11],
                    "id_number": r[12],
                    "id_place_issued": r[13],
                    "ethnicity": r[14],
                    "nationality": r[15],
                    "current_address": r[16],
                    "phone_number": r[17],
                    "emergency_contact": r[18],
                }
                for r in result
            ]
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_by_department(self, department_id):
        """Lấy nhân viên theo phòng ban"""
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, name, department_id, job_title_id, email, phone FROM employee WHERE department_id = ? ORDER BY name ASC",
                [department_id],
            ).fetchall()
            con.close()
            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "department_id": r[2],
                    "job_title_id": r[3],
                    "email": r[4],
                    "phone": r[5],
                }
                for r in result
            ]
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: get_by_department() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_by_id(self, emp_id):
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            r = con.execute(
                "SELECT id, name, department_id, job_title_id, email, phone, address FROM employee WHERE id=?",
                [emp_id],
            ).fetchone()
            con.close()
            if r:
                return {
                    "id": r[0],
                    "name": r[1],
                    "department_id": r[2],
                    "job_title_id": r[3],
                    "email": r[4],
                    "phone": r[5],
                    "address": r[6],
                }
            return None
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: get_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def add(
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
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """INSERT INTO employee (name, department_id, job_title_id, employee_code, 
                   gender, hire_date, attendance_code, attendance_name, date_of_birth, 
                   birthplace, hometown, id_number, id_place_issued, ethnicity, nationality, 
                   current_address, phone_number, emergency_contact) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
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
                ],
            )
            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: add() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update(
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
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """UPDATE employee SET name=?, department_id=?, job_title_id=?, employee_code=?,
                   gender=?, hire_date=?, attendance_code=?, attendance_name=?, date_of_birth=?,
                   birthplace=?, hometown=?, id_number=?, id_place_issued=?, ethnicity=?, nationality=?,
                   current_address=?, phone_number=?, emergency_contact=?, updated_at=now() WHERE id=?""",
                [
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
                    emp_id,
                ],
            )
            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: update() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete(self, emp_id):
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM employee WHERE id=?", [emp_id])

            # Kiểm tra xem còn bản ghi nào không
            count_result = con.execute("SELECT COUNT(*) FROM employee").fetchone()
            record_count = count_result[0] if count_result else 0

            # Nếu không còn bản ghi nào, reset sequence bằng cách drop và tạo lại
            if record_count == 0:
                try:
                    con.execute("DROP SEQUENCE seq_employee")
                    con.execute("CREATE SEQUENCE seq_employee START 1")
                    log_to_debug("EmployeeRepository: Sequence dropped and recreated")
                except Exception as seq_error:
                    log_to_debug(
                        f"EmployeeRepository: Error resetting sequence: {seq_error}"
                    )

            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: delete() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def count(self):
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            r = con.execute("SELECT COUNT(*) FROM employee").fetchone()
            con.close()
            return r[0] if r else 0
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: count() error: {e}\n{traceback.format_exc()}"
            )
            return 0

    def is_employee_code_exists(self, employee_code, exclude_emp_id=None):
        """Kiểm tra xem mã nhân viên đã tồn tại chưa"""
        try:
            if not employee_code:
                return False
            con = duckdb.connect(self.db_path, read_only=True)
            if exclude_emp_id:
                # Khi sửa, loại trừ nhân viên hiện tại
                r = con.execute(
                    "SELECT COUNT(*) FROM employee WHERE employee_code = ? AND id != ?",
                    [employee_code, exclude_emp_id],
                ).fetchone()
            else:
                # Khi thêm mới
                r = con.execute(
                    "SELECT COUNT(*) FROM employee WHERE employee_code = ?",
                    [employee_code],
                ).fetchone()
            con.close()
            return (r[0] if r else 0) > 0
        except Exception as e:
            log_to_debug(
                f"EmployeeRepository: is_employee_code_exists() error: {e}\n{traceback.format_exc()}"
            )
            return False
