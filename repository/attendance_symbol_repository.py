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


class AttendanceSymbolRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng attendance_symbol nếu chưa tồn tại"""
        try:
            log_to_debug("AttendanceSymbolRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Kiểm tra xem table đã tồn tại chưa
            table_exists = con.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'attendance_symbol'"
            ).fetchone()[0]

            if table_exists > 0:
                log_to_debug(
                    "AttendanceSymbolRepository: Table already exists, skip initialization"
                )
                con.close()
                return

            # Chỉ tạo table nếu chưa tồn tại
            con.execute(
                """
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
                )
                """
            )

            # Chèn dữ liệu mặc định chỉ khi table mới tạo
            con.execute(
                """
                INSERT INTO attendance_symbol (
                    id, late_symbol, early_leave_symbol, on_time_symbol,
                    overtime_symbol, missing_checkout_symbol, missing_checkin_symbol,
                    absent_symbol, on_time_overnight_symbol, no_schedule_symbol,
                    show_late, show_early_leave, show_on_time, show_overtime,
                    show_missing_checkout, show_missing_checkin, show_absent,
                    show_on_time_overnight, show_no_schedule
                ) VALUES (
                    1, 'Tr', 'Sm', 'X', '+', 'KR', 'KV', 'V', 'D', 'Off',
                    TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE
                )
            """
            )

            con.commit()
            con.close()
            log_to_debug(
                "AttendanceSymbolRepository: Table created and initialized successfully"
            )
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_attendance_symbols(self):
        """Lấy cấu hình ký hiệu chấm công"""
        try:
            log_to_debug("AttendanceSymbolRepository: get_attendance_symbols() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT late_symbol, early_leave_symbol, on_time_symbol,
                       overtime_symbol, missing_checkout_symbol, missing_checkin_symbol,
                       absent_symbol, on_time_overnight_symbol, no_schedule_symbol,
                       show_late, show_early_leave, show_on_time, show_overtime,
                       show_missing_checkout, show_missing_checkin, show_absent,
                       show_on_time_overnight, show_no_schedule
                FROM attendance_symbol 
                WHERE id = 1
                """
            ).fetchone()
            con.close()

            if result:
                symbols = {
                    "late_symbol": result[0],
                    "early_leave_symbol": result[1],
                    "on_time_symbol": result[2],
                    "overtime_symbol": result[3],
                    "missing_checkout_symbol": result[4],
                    "missing_checkin_symbol": result[5],
                    "absent_symbol": result[6],
                    "on_time_overnight_symbol": result[7],
                    "no_schedule_symbol": result[8],
                    "show_late": result[9],
                    "show_early_leave": result[10],
                    "show_on_time": result[11],
                    "show_overtime": result[12],
                    "show_missing_checkout": result[13],
                    "show_missing_checkin": result[14],
                    "show_absent": result[15],
                    "show_on_time_overnight": result[16],
                    "show_no_schedule": result[17],
                }
                log_to_debug(
                    f"AttendanceSymbolRepository: get_attendance_symbols() returned symbols"
                )
                return symbols
            return None
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolRepository: get_attendance_symbols() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def update_attendance_symbols(
        self,
        late_symbol,
        early_leave_symbol,
        on_time_symbol,
        overtime_symbol,
        missing_checkout_symbol,
        missing_checkin_symbol,
        absent_symbol,
        on_time_overnight_symbol,
        no_schedule_symbol,
        show_late,
        show_early_leave,
        show_on_time,
        show_overtime,
        show_missing_checkout,
        show_missing_checkin,
        show_absent,
        show_on_time_overnight,
        show_no_schedule,
    ):
        """Cập nhật cấu hình ký hiệu chấm công"""
        try:
            log_to_debug(
                "AttendanceSymbolRepository: update_attendance_symbols() called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE attendance_symbol 
                SET late_symbol = ?,
                    early_leave_symbol = ?,
                    on_time_symbol = ?,
                    overtime_symbol = ?,
                    missing_checkout_symbol = ?,
                    missing_checkin_symbol = ?,
                    absent_symbol = ?,
                    on_time_overnight_symbol = ?,
                    no_schedule_symbol = ?,
                    show_late = ?,
                    show_early_leave = ?,
                    show_on_time = ?,
                    show_overtime = ?,
                    show_missing_checkout = ?,
                    show_missing_checkin = ?,
                    show_absent = ?,
                    show_on_time_overnight = ?,
                    show_no_schedule = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
                """,
                [
                    late_symbol,
                    early_leave_symbol,
                    on_time_symbol,
                    overtime_symbol,
                    missing_checkout_symbol,
                    missing_checkin_symbol,
                    absent_symbol,
                    on_time_overnight_symbol,
                    no_schedule_symbol,
                    show_late,
                    show_early_leave,
                    show_on_time,
                    show_overtime,
                    show_missing_checkout,
                    show_missing_checkin,
                    show_absent,
                    show_on_time_overnight,
                    show_no_schedule,
                ],
            )
            con.commit()
            con.close()
            log_to_debug(
                "AttendanceSymbolRepository: update_attendance_symbols() success"
            )
            return True
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolRepository: update_attendance_symbols() error: {e}\n{traceback.format_exc()}"
            )
            return False
