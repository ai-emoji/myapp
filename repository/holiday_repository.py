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


class HolidayRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng holiday nếu chưa tồn tại"""
        try:
            log_to_debug("HolidayRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_holiday START 1")
            except Exception:
                # Sequence đã tồn tại, bỏ qua im lặng
                pass

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS holiday (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_holiday'),
                    holiday_date DATE NOT NULL,
                    name VARCHAR NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            con.close()
            log_to_debug("HolidayRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_all_holidays(self):
        """Lấy tất cả ngày nghỉ"""
        try:
            log_to_debug("HolidayRepository: get_all_holidays() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, holiday_date, name FROM holiday ORDER BY holiday_date ASC"
            ).fetchall()
            con.close()

            holidays = [
                {"id": row[0], "holiday_date": row[1], "name": row[2]} for row in result
            ]
            log_to_debug(
                f"HolidayRepository: get_all_holidays() returned {len(holidays)} records"
            )
            return holidays
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: get_all_holidays() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_holiday_by_id(self, holiday_id):
        """Lấy ngày nghỉ theo ID"""
        try:
            log_to_debug(f"HolidayRepository: get_holiday_by_id({holiday_id}) called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, holiday_date, name FROM holiday WHERE id=?", [holiday_id]
            ).fetchone()
            con.close()

            if result:
                holiday = {
                    "id": result[0],
                    "holiday_date": result[1],
                    "name": result[2],
                }
                log_to_debug(f"HolidayRepository: get_holiday_by_id() found: {holiday}")
                return holiday

            log_to_debug(f"HolidayRepository: get_holiday_by_id() not found")
            return None
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: get_holiday_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def add_holiday(self, holiday_date, name):
        """Thêm ngày nghỉ mới"""
        try:
            log_to_debug(
                f"HolidayRepository: add_holiday(date={holiday_date}, name={name}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "INSERT INTO holiday (holiday_date, name) VALUES (?, ?)",
                [holiday_date, name],
            )
            con.close()
            log_to_debug(f"HolidayRepository: add_holiday() inserted successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: add_holiday() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update_holiday(self, holiday_id, holiday_date, name):
        """Cập nhật ngày nghỉ"""
        try:
            log_to_debug(
                f"HolidayRepository: update_holiday(id={holiday_id}, date={holiday_date}, name={name}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "UPDATE holiday SET holiday_date=?, name=?, updated_at=now() WHERE id=?",
                [holiday_date, name, holiday_id],
            )
            con.close()
            log_to_debug(f"HolidayRepository: update_holiday() updated successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: update_holiday() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_holiday(self, holiday_id):
        """Xóa ngày nghỉ"""
        try:
            log_to_debug(f"HolidayRepository: delete_holiday(id={holiday_id}) called")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM holiday WHERE id=?", [holiday_id])

            # Kiểm tra xem còn bản ghi nào không
            count_result = con.execute("SELECT COUNT(*) FROM holiday").fetchone()
            record_count = count_result[0] if count_result else 0

            # Nếu không còn bản ghi nào, reset sequence bằng cách drop và tạo lại
            if record_count == 0:
                try:
                    con.execute("DROP SEQUENCE seq_holiday")
                    con.execute("CREATE SEQUENCE seq_holiday START 1")
                    log_to_debug("HolidayRepository: Sequence dropped and recreated")
                except Exception as seq_error:
                    log_to_debug(
                        f"HolidayRepository: Error resetting sequence: {seq_error}"
                    )

            con.close()
            log_to_debug(f"HolidayRepository: delete_holiday() deleted successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: delete_holiday() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_total_count(self):
        """Lấy tổng số ngày nghỉ"""
        try:
            log_to_debug("HolidayRepository: get_total_count() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute("SELECT COUNT(*) FROM holiday").fetchone()
            con.close()

            total = result[0] if result else 0
            log_to_debug(f"HolidayRepository: get_total_count() returned {total}")
            return total
        except Exception as e:
            log_to_debug(
                f"HolidayRepository: get_total_count() error: {e}\n{traceback.format_exc()}"
            )
            return 0
