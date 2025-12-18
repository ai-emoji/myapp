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


class WeekendRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()

    def get_weekend_config(self):
        """Lấy cấu hình ngày cuối tuần"""
        try:
            log_to_debug("WeekendRepository: get_weekend_config() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday
                FROM weekend 
                WHERE id = 1
                """
            ).fetchone()
            con.close()

            if result:
                config = {
                    "monday": result[0],
                    "tuesday": result[1],
                    "wednesday": result[2],
                    "thursday": result[3],
                    "friday": result[4],
                    "saturday": result[5],
                    "sunday": result[6],
                }
                log_to_debug("WeekendRepository: get_weekend_config() returned config")
                return config
            return None
        except Exception as e:
            log_to_debug(
                f"WeekendRepository: get_weekend_config() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def update_weekend_config(
        self, monday, tuesday, wednesday, thursday, friday, saturday, sunday
    ):
        """Cập nhật cấu hình ngày cuối tuần"""
        try:
            log_to_debug("WeekendRepository: update_weekend_config() called")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE weekend 
                SET monday = ?,
                    tuesday = ?,
                    wednesday = ?,
                    thursday = ?,
                    friday = ?,
                    saturday = ?,
                    sunday = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
                """,
                [monday, tuesday, wednesday, thursday, friday, saturday, sunday],
            )
            con.commit()
            con.close()
            log_to_debug("WeekendRepository: update_weekend_config() success")
            return True
        except Exception as e:
            log_to_debug(
                f"WeekendRepository: update_weekend_config() error: {e}\n{traceback.format_exc()}"
            )
            return False
