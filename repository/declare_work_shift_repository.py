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


class DeclareWorkShiftRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng declare_work_shift nếu chưa tồn tại"""
        try:
            log_to_debug("DeclareWorkShiftRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_declare_work_shift START 1")
            except Exception:
                # Sequence đã tồn tại, bỏ qua im lặng
                pass

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
            log_to_debug("DeclareWorkShiftRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_all_work_shifts(self):
        """Lấy tất cả ca làm việc"""
        try:
            log_to_debug("DeclareWorkShiftRepository: get_all_work_shifts() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, shift_code, start_time, end_time, lunch_start, lunch_end, 
                       total_minutes, work_day_count
                FROM declare_work_shift 
                ORDER BY id ASC
                """
            ).fetchall()
            con.close()

            work_shifts = [
                {
                    "id": row[0],
                    "shift_code": row[1],
                    "start_time": row[2],
                    "end_time": row[3],
                    "lunch_start": row[4],
                    "lunch_end": row[5],
                    "total_minutes": row[6],
                    "work_day_count": row[7],
                }
                for row in result
            ]
            log_to_debug(
                f"DeclareWorkShiftRepository: get_all_work_shifts() returned {len(work_shifts)} records"
            )
            return work_shifts
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: get_all_work_shifts() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_work_shift_by_id(self, work_shift_id):
        """Lấy ca làm việc theo ID"""
        try:
            log_to_debug(
                f"DeclareWorkShiftRepository: get_work_shift_by_id({work_shift_id}) called"
            )
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, shift_code, start_time, end_time, lunch_start, lunch_end, 
                       total_minutes, work_day_count
                FROM declare_work_shift 
                WHERE id=?
                """,
                [work_shift_id],
            ).fetchone()
            con.close()

            if result:
                work_shift = {
                    "id": result[0],
                    "shift_code": result[1],
                    "start_time": result[2],
                    "end_time": result[3],
                    "lunch_start": result[4],
                    "lunch_end": result[5],
                    "total_minutes": result[6],
                    "work_day_count": result[7],
                }
                log_to_debug(
                    f"DeclareWorkShiftRepository: get_work_shift_by_id() found: {work_shift}"
                )
                return work_shift

            log_to_debug(
                f"DeclareWorkShiftRepository: get_work_shift_by_id() not found"
            )
            return None
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: get_work_shift_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def add_work_shift(
        self,
        shift_code,
        start_time,
        end_time,
        lunch_start,
        lunch_end,
        total_minutes,
        work_day_count,
    ):
        """Thêm ca làm việc mới"""
        try:
            log_to_debug(
                f"DeclareWorkShiftRepository: add_work_shift(shift_code={shift_code}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                INSERT INTO declare_work_shift 
                (shift_code, start_time, end_time, lunch_start, lunch_end, total_minutes, work_day_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    shift_code,
                    start_time,
                    end_time,
                    lunch_start,
                    lunch_end,
                    total_minutes,
                    work_day_count,
                ],
            )
            con.close()
            log_to_debug("DeclareWorkShiftRepository: add_work_shift() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: add_work_shift() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update_work_shift(
        self,
        work_shift_id,
        shift_code,
        start_time,
        end_time,
        lunch_start,
        lunch_end,
        total_minutes,
        work_day_count,
    ):
        """Cập nhật ca làm việc"""
        try:
            log_to_debug(
                f"DeclareWorkShiftRepository: update_work_shift(id={work_shift_id}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE declare_work_shift 
                SET shift_code=?, start_time=?, end_time=?, lunch_start=?, lunch_end=?, 
                    total_minutes=?, work_day_count=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                [
                    shift_code,
                    start_time,
                    end_time,
                    lunch_start,
                    lunch_end,
                    total_minutes,
                    work_day_count,
                    work_shift_id,
                ],
            )
            con.close()
            log_to_debug("DeclareWorkShiftRepository: update_work_shift() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: update_work_shift() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_work_shift(self, work_shift_id):
        """Xóa ca làm việc"""
        try:
            log_to_debug(
                f"DeclareWorkShiftRepository: delete_work_shift(id={work_shift_id}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM declare_work_shift WHERE id=?", [work_shift_id])
            con.close()
            log_to_debug("DeclareWorkShiftRepository: delete_work_shift() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: delete_work_shift() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_total_count(self):
        """Lấy tổng số ca làm việc"""
        try:
            log_to_debug("DeclareWorkShiftRepository: get_total_count() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute("SELECT COUNT(*) FROM declare_work_shift").fetchone()
            con.close()
            count = result[0] if result else 0
            log_to_debug(
                f"DeclareWorkShiftRepository: get_total_count() result: {count}"
            )
            return count
        except Exception as e:
            log_to_debug(
                f"DeclareWorkShiftRepository: get_total_count() error: {e}\n{traceback.format_exc()}"
            )
            return 0
