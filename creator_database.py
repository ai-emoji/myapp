# Đảm bảo import được module nội bộ khi chạy trực tiếp
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import Database
import logging
import duckdb


def create_company_table():
    """
    Mô tả:
        Tạo bảng company nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        icon_path TEXT
    );
    """

    try:
        with Database.connect() as conn:
            conn.execute(sql)
            print("[INFO] Đã tạo bảng company (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng company: {e}")


def create_job_title_table():
    """
    Mô tả:
        Tạo bảng job_title nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS job_title (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_job_title'),
        name TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            # Tạo sequence nếu chưa tồn tại
            try:
                conn.execute("CREATE SEQUENCE seq_job_title START 1")
            except:
                pass  # Sequence đã tồn tại

            conn.execute(sql)
            print("[INFO] Đã tạo bảng job_title (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng job_title: {e}")


def create_department_table():
    """
    Mô tả:
        Tạo bảng department nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_department'),
        name TEXT UNIQUE NOT NULL,
        parent_id INTEGER NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            # Tạo sequence nếu chưa tồn tại
            try:
                conn.execute("CREATE SEQUENCE seq_department START 1")
            except:
                pass
            conn.execute(sql)
            print("[INFO] Đã tạo bảng department (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng department: {e}")


def create_employee_table():
    """
    Mô tả:
        Tạo bảng employee nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
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
    );
    """

    try:
        with Database.connect() as conn:
            # Tạo sequence nếu chưa tồn tại
            try:
                conn.execute("CREATE SEQUENCE seq_employee START 1")
            except:
                pass  # Sequence đã tồn tại

            conn.execute(sql)
            print("[INFO] Đã tạo bảng employee (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng employee: {e}")


def create_holiday_table():
    """
    Mô tả:
        Tạo bảng holiday nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS holiday (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_holiday'),
        holiday_date DATE NOT NULL,
        name VARCHAR NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            # Tạo sequence nếu chưa tồn tại
            try:
                conn.execute("CREATE SEQUENCE seq_holiday START 1")
            except:
                pass  # Sequence đã tồn tại

            conn.execute(sql)
            print("[INFO] Đã tạo bảng holiday (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng holiday: {e}")


def create_attendance_symbol_table():
    """
    Mô tả:
        Tạo bảng attendance_symbol nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
        Bảng này lưu các ký hiệu chấm công.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS attendance_symbol (
        id INTEGER PRIMARY KEY DEFAULT 1,
        late_symbol VARCHAR DEFAULT 'Tr',
        early_leave_symbol VARCHAR DEFAULT 'Sm',
        on_time_symbol VARCHAR DEFAULT 'X',
        overtime_symbol VARCHAR DEFAULT '+',
        missing_checkout_symbol VARCHAR DEFAULT 'KR',
        missing_checkin_symbol VARCHAR DEFAULT 'KV',
        absent_symbol VARCHAR DEFAULT 'V',
        on_time_overnight_symbol VARCHAR DEFAULT 'D',
        no_schedule_symbol VARCHAR DEFAULT 'Off',
        show_late BOOLEAN DEFAULT TRUE,
        show_early_leave BOOLEAN DEFAULT TRUE,
        show_on_time BOOLEAN DEFAULT TRUE,
        show_overtime BOOLEAN DEFAULT TRUE,
        show_missing_checkout BOOLEAN DEFAULT TRUE,
        show_missing_checkin BOOLEAN DEFAULT TRUE,
        show_absent BOOLEAN DEFAULT TRUE,
        show_on_time_overnight BOOLEAN DEFAULT TRUE,
        show_no_schedule BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            conn.execute(sql)

            # Chèn dữ liệu mặc định nếu bảng trống
            result = conn.execute("SELECT COUNT(*) FROM attendance_symbol").fetchone()
            if result[0] == 0:
                conn.execute(
                    """
                    INSERT INTO attendance_symbol (
                        id, late_symbol, early_leave_symbol, on_time_symbol,
                        overtime_symbol, missing_checkout_symbol, missing_checkin_symbol,
                        absent_symbol, on_time_overnight_symbol, no_schedule_symbol,
                        show_on_time, show_on_time_overnight, show_no_schedule
                    ) VALUES (
                        1, 'Tr', 'Sm', 'X', '+', 'KR', 'KV', 'V', 'D', 'Off',
                        TRUE, TRUE, TRUE
                    )
                """
                )

            print("[INFO] Đã tạo bảng attendance_symbol (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng attendance_symbol: {e}")


def create_weekend_table():
    """
    Mô tả:
        Tạo bảng weekend nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
        Bảng lưu cấu hình các ngày trong tuần là ngày nghỉ cuối tuần.
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS weekend (
        id INTEGER PRIMARY KEY DEFAULT 1,
        monday BOOLEAN DEFAULT FALSE,
        tuesday BOOLEAN DEFAULT FALSE,
        wednesday BOOLEAN DEFAULT FALSE,
        thursday BOOLEAN DEFAULT FALSE,
        friday BOOLEAN DEFAULT FALSE,
        saturday BOOLEAN DEFAULT TRUE,
        sunday BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            conn.execute(sql)

            # Chèn dữ liệu mặc định nếu bảng mới tạo và chưa có dữ liệu
            check_data = conn.execute("SELECT COUNT(*) FROM weekend").fetchone()[0]
            if check_data == 0:
                conn.execute(
                    """
                    INSERT INTO weekend (
                        id, monday, tuesday, wednesday, thursday, friday, saturday, sunday
                    ) VALUES (
                        1, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE
                    )
                    """
                )
                print("[INFO] Đã chèn dữ liệu mặc định vào bảng weekend.")

            print("[INFO] Đã tạo bảng weekend (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng weekend: {e}")


def create_absence_symbol_table():
    """
    Mô tả:
        Tạo bảng absence_symbol nếu chưa tồn tại trong cơ sở dữ liệu DuckDB.
        Bảng lưu các ký hiệu loại vắng (nghỉ ốm, nghỉ phép, v.v.)
    """

    db_path = Database.get_db_path()
    print(f"[DEBUG] db_path: {db_path}")

    sql = """
    CREATE TABLE IF NOT EXISTS absence_symbol (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_absence_symbol'),
        code VARCHAR(10) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        symbol VARCHAR(10) NOT NULL,
        is_used BOOLEAN DEFAULT TRUE,
        is_paid BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with Database.connect() as conn:
            # Tạo sequence nếu chưa tồn tại
            try:
                conn.execute("CREATE SEQUENCE seq_absence_symbol START 1")
            except:
                pass

            conn.execute(sql)

            # Chèn dữ liệu mặc định nếu bảng mới tạo và chưa có dữ liệu
            check_data = conn.execute("SELECT COUNT(*) FROM absence_symbol").fetchone()[
                0
            ]
            if check_data == 0:
                default_data = [
                    ("A01", "Nghỉ ốm", "OM", True, False),
                    ("A02", "Nghỉ Thai Sản", "TS", True, False),
                    ("A03", "Việc riêng có lương", "R", True, True),
                    ("A04", "Việc riêng không lương", "Ro", True, False),
                    ("A05", "Nghỉ phép", "P", True, False),
                    ("A06", "Nghỉ phép năm", "F", True, False),
                    ("A07", "Còn ốm", "CO", True, False),
                    ("A08", "Cấp điền", "CD", True, False),
                    ("A09", "Nghỉ hội họp, học tập", "H", True, False),
                    ("A10", "Nghỉ công tác", "CT", True, False),
                    ("A11", "Nghỉ lễ", "Le", True, False),
                ]

                for code, desc, symbol, is_used, is_paid in default_data:
                    conn.execute(
                        """
                        INSERT INTO absence_symbol (code, description, symbol, is_used, is_paid)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        [code, desc, symbol, is_used, is_paid],
                    )
                print("[INFO] Đã chèn dữ liệu mặc định vào bảng absence_symbol.")

            print("[INFO] Đã tạo bảng absence_symbol (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng absence_symbol: {e}")


def create_declare_work_shift_table():
    """
    Tạo bảng declare_work_shift để lưu thông tin ca làm việc
    """
    try:
        con = duckdb.connect(Database.get_db_path(), read_only=False)

        # Tạo sequence nếu chưa có
        try:
            con.execute("CREATE SEQUENCE seq_declare_work_shift START 1")
        except Exception:
            pass

        # Tạo bảng declare_work_shift
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS declare_work_shift (
                id INTEGER PRIMARY KEY DEFAULT nextval('seq_declare_work_shift'),
                shift_code VARCHAR NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                lunch_start TIME,
                lunch_end TIME,
                total_minutes INTEGER DEFAULT 0,
                work_day_count DECIMAL(10, 2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        con.close()
        print("[INFO] Đã tạo bảng declare_work_shift (nếu chưa có).")
    except Exception as e:
        logging.error(f"Lỗi khi tạo bảng declare_work_shift: {e}")


if __name__ == "__main__":
    create_company_table()
    create_job_title_table()
    create_department_table()
    create_employee_table()
    create_holiday_table()
    create_attendance_symbol_table()
    create_weekend_table()
    create_absence_symbol_table()
    create_declare_work_shift_table()

    if os.path.exists(Database.get_db_path()):
        print("✅ Đã tạo file database/app.duckdb")
    else:
        print("❌ Không tạo được file database/app.duckdb")
