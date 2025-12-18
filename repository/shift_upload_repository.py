# shift_upload_repository.py
# Repository để quản lý danh sách nhân viên đã tải lên máy chấm công

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


class ShiftUploadRepository:
    """Repository để quản lý dữ liệu nhân viên đã tải lên máy chấm công"""

    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng shift_upload nếu chưa tồn tại"""
        try:
            log_to_debug("ShiftUploadRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_shift_upload START 1")
            except Exception:
                pass  # Sequence đã tồn tại

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS shift_upload (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_shift_upload'),
                    employee_id INTEGER NOT NULL,
                    device_id INTEGER NOT NULL,
                    user_id VARCHAR NOT NULL,
                    attendance_code VARCHAR,
                    attendance_name VARCHAR,
                    card_number VARCHAR,
                    password VARCHAR,
                    privilege INTEGER DEFAULT 0,
                    enabled BOOLEAN DEFAULT TRUE,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(employee_id, device_id),
                    FOREIGN KEY (employee_id) REFERENCES employee(id),
                    FOREIGN KEY (device_id) REFERENCES device(id)
                )
                """
            )

            con.close()
            log_to_debug("ShiftUploadRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def insert(self, employee_id, device_id, user_id, attendance_code, attendance_name, 
               card_number="", password="", privilege=0, enabled=True):
        """
        Thêm bản ghi nhân viên đã tải lên máy
        Args:
            employee_id: ID nhân viên trong DB
            device_id: ID thiết bị
            user_id: User ID trên máy chấm công
            attendance_code: Mã chấm công
            attendance_name: Tên chấm công
            card_number: Mã số thẻ
            password: Mật mã
            privilege: Quyền (0=User, 1=Enroller, 2=Manager, 6=Admin)
            enabled: Cho phép chấm công
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(
                f"ShiftUploadRepository: insert() - employee_id={employee_id}, device_id={device_id}"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            
            con.execute(
                """
                INSERT INTO shift_upload 
                (employee_id, device_id, user_id, attendance_code, attendance_name, 
                 card_number, password, privilege, enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (employee_id, device_id) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    attendance_code = EXCLUDED.attendance_code,
                    attendance_name = EXCLUDED.attendance_name,
                    card_number = EXCLUDED.card_number,
                    password = EXCLUDED.password,
                    privilege = EXCLUDED.privilege,
                    enabled = EXCLUDED.enabled,
                    uploaded_at = CURRENT_TIMESTAMP
                """,
                [employee_id, device_id, user_id, attendance_code, attendance_name, 
                 card_number, password, privilege, enabled],
            )
            con.commit()
            con.close()
            log_to_debug("ShiftUploadRepository: insert() success")
            return True
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: insert() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def bulk_insert(self, records):
        """
        Thêm nhiều bản ghi
        Args:
            records: List of dicts với keys: employee_id, device_id, user_id, attendance_code, attendance_name, card_number, password, privilege, enabled
        Returns:
            tuple: (success_count, total_count)
        """
        try:
            log_to_debug(f"ShiftUploadRepository: bulk_insert() - {len(records)} records")
            con = duckdb.connect(self.db_path, read_only=False)
            
            success_count = 0
            for record in records:
                try:
                    con.execute(
                        """
                        INSERT INTO shift_upload 
                        (employee_id, device_id, user_id, attendance_code, attendance_name, 
                         card_number, password, privilege, enabled)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT (employee_id, device_id) DO UPDATE SET
                            user_id = EXCLUDED.user_id,
                            attendance_code = EXCLUDED.attendance_code,
                            attendance_name = EXCLUDED.attendance_name,
                            card_number = EXCLUDED.card_number,
                            password = EXCLUDED.password,
                            privilege = EXCLUDED.privilege,
                            enabled = EXCLUDED.enabled,
                            uploaded_at = CURRENT_TIMESTAMP
                        """,
                        [
                            record["employee_id"],
                            record["device_id"],
                            record["user_id"],
                            record.get("attendance_code", ""),
                            record.get("attendance_name", ""),
                            record.get("card_number", ""),
                            record.get("password", ""),
                            record.get("privilege", 0),
                            record.get("enabled", True),
                        ],
                    )
                    success_count += 1
                except Exception as e:
                    log_to_debug(f"ShiftUploadRepository: bulk_insert() - record error: {e}")
            
            con.commit()
            con.close()
            log_to_debug(f"ShiftUploadRepository: bulk_insert() - inserted {success_count}/{len(records)}")
            return success_count, len(records)
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: bulk_insert() error: {e}\n{traceback.format_exc()}"
            )
            return 0, len(records) if records else 0

    def get_by_device(self, device_id):
        """
        Lấy danh sách nhân viên đã tải lên máy theo device_id
        Args:
            device_id: ID thiết bị
        Returns:
            list: Danh sách nhân viên
        """
        try:
            log_to_debug(f"ShiftUploadRepository: get_by_device() - device_id={device_id}")
            con = duckdb.connect(self.db_path, read_only=True)
            
            result = con.execute(
                """
                SELECT su.id, su.employee_id, su.device_id, su.user_id, 
                       su.attendance_code, su.attendance_name, su.card_number, 
                       su.password, su.privilege, su.enabled, su.uploaded_at,
                       e.employee_code, e.name
                FROM shift_upload su
                LEFT JOIN employee e ON su.employee_id = e.id
                WHERE su.device_id = ?
                ORDER BY su.uploaded_at DESC
                """,
                [device_id]
            ).fetchall()
            con.close()
            
            records = []
            for row in result:
                records.append({
                    "id": row[0],
                    "employee_id": row[1],
                    "device_id": row[2],
                    "user_id": row[3],
                    "attendance_code": row[4],
                    "attendance_name": row[5],
                    "card_number": row[6],
                    "password": row[7],
                    "privilege": row[8],
                    "enabled": row[9],
                    "uploaded_at": row[10],
                    "employee_code": row[11],
                    "employee_name": row[12],
                })
            
            log_to_debug(f"ShiftUploadRepository: Found {len(records)} records")
            return records
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: get_by_device() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def delete_by_id(self, record_id):
        """
        Xóa bản ghi theo ID
        Args:
            record_id: ID bản ghi
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(f"ShiftUploadRepository: delete_by_id() - id={record_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM shift_upload WHERE id = ?", [record_id])
            con.commit()
            con.close()
            log_to_debug("ShiftUploadRepository: delete_by_id() success")
            return True
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: delete_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_by_employee_device(self, employee_id, device_id):
        """
        Xóa bản ghi theo employee_id và device_id
        Args:
            employee_id: ID nhân viên
            device_id: ID thiết bị
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(
                f"ShiftUploadRepository: delete_by_employee_device() - employee_id={employee_id}, device_id={device_id}"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "DELETE FROM shift_upload WHERE employee_id = ? AND device_id = ?",
                [employee_id, device_id]
            )
            con.commit()
            con.close()
            log_to_debug("ShiftUploadRepository: delete_by_employee_device() success")
            return True
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: delete_by_employee_device() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_all(self):
        """
        Lấy tất cả bản ghi
        Returns:
            list: Danh sách nhân viên đã tải lên
        """
        try:
            log_to_debug("ShiftUploadRepository: get_all() called")
            con = duckdb.connect(self.db_path, read_only=True)
            
            result = con.execute(
                """
                SELECT su.id, su.employee_id, su.device_id, su.user_id, 
                       su.attendance_code, su.attendance_name, su.card_number, 
                       su.password, su.privilege, su.enabled, su.uploaded_at,
                       e.employee_code, e.name, d.device_name
                FROM shift_upload su
                LEFT JOIN employee e ON su.employee_id = e.id
                LEFT JOIN device d ON su.device_id = d.id
                ORDER BY su.uploaded_at DESC
                """
            ).fetchall()
            con.close()
            
            records = []
            for row in result:
                records.append({
                    "id": row[0],
                    "employee_id": row[1],
                    "device_id": row[2],
                    "user_id": row[3],
                    "attendance_code": row[4],
                    "attendance_name": row[5],
                    "card_number": row[6],
                    "password": row[7],
                    "privilege": row[8],
                    "enabled": row[9],
                    "uploaded_at": row[10],
                    "employee_code": row[11],
                    "employee_name": row[12],
                    "device_name": row[13],
                })
            
            log_to_debug(f"ShiftUploadRepository: get_all() returned {len(records)} records")
            return records
        except Exception as e:
            log_to_debug(
                f"ShiftUploadRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []
