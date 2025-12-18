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


class CompanyRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()

    def get_company_info(self):
        log_to_debug("CompanyRepository: get_company_info() called")
        # Tạo bảng nếu chưa tồn tại (chỉ lần đầu)
        con_write = duckdb.connect(self.db_path, read_only=False)
        con_write.execute(
            """
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                icon_path VARCHAR
            )
            """
        )
        con_write.close()

        # Đọc dữ liệu ở chế độ read_only
        con = duckdb.connect(self.db_path, read_only=True)
        result = con.execute(
            "SELECT name, phone, address, icon_path FROM company WHERE id=1"
        ).fetchone()
        con.close()
        if result:
            log_to_debug(f"CompanyRepository: get_company_info() result: {result}")
            return {
                "name": result[0],
                "phone": result[1],
                "address": result[2],
                "logo_path": result[3],  # vẫn trả về logo_path cho tương thích code cũ
            }
        log_to_debug("CompanyRepository: get_company_info() result: None")
        return {"name": "", "phone": "", "address": "", "logo_path": ""}

    def update_company_info(self, name, phone, address, logo_path):
        log_to_debug(
            f"CompanyRepository: update_company_info(name={name}, phone={phone}, address={address}, logo_path={logo_path}) called"
        )
        con = duckdb.connect(self.db_path)
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                icon_path VARCHAR
            )
            """
        )
        result = con.execute("SELECT id FROM company WHERE id=1").fetchone()
        if result:
            con.execute(
                "UPDATE company SET name=?, phone=?, address=?, icon_path=? WHERE id=1",
                [name, phone, address, logo_path],
            )
            log_to_debug(
                "CompanyRepository: update_company_info() - updated existing row"
            )
        else:
            con.execute(
                "INSERT INTO company (id, name, phone, address, icon_path) VALUES (1, ?, ?, ?, ?)",
                [name, phone, address, logo_path],
            )
            log_to_debug("CompanyRepository: update_company_info() - inserted new row")
        con.close()
        return True

    def delete_all(self):
        """Xóa tất cả dữ liệu công ty (nếu cần)"""
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM company")
            con.close()
            log_to_debug("CompanyRepository: delete_all() deleted successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"CompanyRepository: delete_all() error: {e}\n{traceback.format_exc()}"
            )
            return False
