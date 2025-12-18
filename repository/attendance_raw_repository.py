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


class AttendanceRawRepository:
    """Repository để quản lý dữ liệu chấm công thô từ máy chấm công"""

    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng attendance_raw nếu chưa tồn tại"""
        try:
            log_to_debug("AttendanceRawRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_attendance_raw START 1")
            except Exception:
                pass  # Sequence đã tồn tại

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance_raw (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_attendance_raw'),
                    user_id VARCHAR NOT NULL,
                    user_name VARCHAR,
                    timestamp TIMESTAMP NOT NULL,
                    status INTEGER,
                    punch INTEGER,
                    uid BIGINT,
                    device_sn VARCHAR,
                    device_id INTEGER,
                    note VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, timestamp, device_sn)
                )
                """
            )
            con.commit()
            con.close()
            log_to_debug("AttendanceRawRepository: Table attendance_raw initialized successfully")
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def insert(self, user_id, user_name, timestamp, status, punch, uid, device_sn, device_id, note=""):
        """
        Thêm bản ghi chấm công
        Args:
            user_id: Mã nhân viên
            user_name: Tên nhân viên
            timestamp: Thời gian chấm công
            status: Trạng thái (0=Check-in, 1=Check-out, etc)
            punch: Loại punch (0=finger, 1=password, etc)
            uid: UID của user
            device_sn: Serial number của thiết bị
            device_id: ID thiết bị trong database
            note: Ghi chú
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            log_to_debug(
                f"AttendanceRawRepository: insert() - user_id={user_id}, timestamp={timestamp}"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            
            # Insert hoặc ignore nếu đã tồn tại (dựa vào UNIQUE constraint)
            con.execute(
                """
                INSERT INTO attendance_raw 
                (user_id, user_name, timestamp, status, punch, uid, device_sn, device_id, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT DO NOTHING
                """,
                [user_id, user_name, timestamp, status, punch, uid, device_sn, device_id, note],
            )
            con.commit()
            con.close()
            log_to_debug("AttendanceRawRepository: insert() success")
            return True
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: insert() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def bulk_insert(self, records):
        """
        Thêm nhiều bản ghi chấm công
        Args:
            records: List of tuples (user_id, user_name, timestamp, status, punch, uid, device_sn, device_id, note)
        Returns:
            tuple: (success_count, total_count)
        """
        try:
            log_to_debug(f"AttendanceRawRepository: bulk_insert() - {len(records)} records")
            con = duckdb.connect(self.db_path, read_only=False)
            
            success_count = 0
            for record in records:
                try:
                    con.execute(
                        """
                        INSERT INTO attendance_raw 
                        (user_id, user_name, timestamp, status, punch, uid, device_sn, device_id, note)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT DO NOTHING
                        """,
                        record,
                    )
                    success_count += 1
                except Exception:
                    pass  # Skip duplicates
            
            con.commit()
            con.close()
            log_to_debug(f"AttendanceRawRepository: bulk_insert() - inserted {success_count}/{len(records)}")
            return success_count, len(records)
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: bulk_insert() error: {e}\n{traceback.format_exc()}"
            )
            return 0, len(records) if records else 0

    def get_all(self, from_date=None, to_date=None, device_id=None):
        """
        Lấy danh sách dữ liệu chấm công
        Args:
            from_date: Từ ngày (optional)
            to_date: Đến ngày (optional)
            device_id: ID thiết bị (optional)
        Returns:
            list: Danh sách bản ghi chấm công
        """
        try:
            log_to_debug(f"AttendanceRawRepository: get_all() - from_date={from_date}, to_date={to_date}, device_id={device_id}")
            con = duckdb.connect(self.db_path, read_only=True)
            
            query = """
                SELECT id, user_id, user_name, timestamp, status, punch, 
                       uid, device_sn, device_id, note, created_at
                FROM attendance_raw
                WHERE 1=1
            """
            params = []
            
            if from_date:
                query += " AND DATE(timestamp) >= ?"
                params.append(from_date)
            
            if to_date:
                query += " AND DATE(timestamp) <= ?"
                params.append(to_date)
            
            if device_id:
                query += " AND device_id = ?"
                params.append(device_id)
            
            query += " ORDER BY timestamp ASC"  # Đổi từ DESC sang ASC để dễ đọc theo thời gian
            
            log_to_debug(f"AttendanceRawRepository: Query={query}, Params={params}")
            result = con.execute(query, params).fetchall()
            con.close()
            log_to_debug(f"AttendanceRawRepository: Found {len(result)} records")

            records = []
            for row in result:
                records.append(
                    {
                        "id": row[0],
                        "user_id": row[1],
                        "user_name": row[2],
                        "timestamp": row[3],
                        "status": row[4],
                        "punch": row[5],
                        "uid": row[6],
                        "device_sn": row[7],
                        "device_id": row[8],
                        "note": row[9],
                        "created_at": row[10],
                    }
                )

            log_to_debug(f"AttendanceRawRepository: get_all() returned {len(records)} records")
            return records
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def delete_all(self):
        """
        Xóa toàn bộ dữ liệu chấm công
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug("AttendanceRawRepository: delete_all() called")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM attendance_raw")
            con.commit()
            con.close()
            log_to_debug("AttendanceRawRepository: delete_all() success")
            return True
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: delete_all() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_by_id(self, record_id):
        """
        Xóa một bản ghi theo ID
        Args:
            record_id: ID của bản ghi
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(f"AttendanceRawRepository: delete_by_id() - id={record_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM attendance_raw WHERE id = ?", [record_id])
            con.commit()
            con.close()
            log_to_debug("AttendanceRawRepository: delete_by_id() success")
            return True
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: delete_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_by_device(self, device_id):
        """
        Xóa dữ liệu chấm công theo thiết bị
        Args:
            device_id: ID thiết bị
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(f"AttendanceRawRepository: delete_by_device() - device_id={device_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM attendance_raw WHERE device_id = ?", [device_id])
            con.commit()
            con.close()
            log_to_debug("AttendanceRawRepository: delete_by_device() success")
            return True
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: delete_by_device() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_count(self):
        """
        Đếm số bản ghi chấm công
        Returns:
            int: Số lượng bản ghi
        """
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute("SELECT COUNT(*) FROM attendance_raw").fetchone()
            con.close()
            return result[0] if result else 0
        except Exception as e:
            log_to_debug(
                f"AttendanceRawRepository: get_count() error: {e}\n{traceback.format_exc()}"
            )
            return 0
