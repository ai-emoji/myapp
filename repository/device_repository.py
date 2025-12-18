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


class DeviceRepository:
    """Repository để quản lý thiết bị chấm công trong database"""

    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng device nếu chưa tồn tại"""
        try:
            log_to_debug("DeviceRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_device START 1")
            except Exception:
                pass  # Sequence đã tồn tại

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS device (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_device'),
                    device_number VARCHAR UNIQUE NOT NULL,
                    device_name VARCHAR NOT NULL,
                    ip_address VARCHAR NOT NULL,
                    password VARCHAR,
                    port INTEGER DEFAULT 4370,
                    status VARCHAR DEFAULT 'Chưa kết nối',
                    note VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            con.commit()
            con.close()
            log_to_debug("DeviceRepository: Table device initialized successfully")
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def insert(self, device_number, device_name, ip_address, password="", port=4370, note=""):
        """
        Thêm thiết bị mới
        Args:
            device_number: Số máy
            device_name: Tên máy
            ip_address: Địa chỉ IP
            password: Mật mã thiết bị
            port: Cổng kết nối
            note: Ghi chú
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            log_to_debug(
                f"DeviceRepository: insert() - device_number={device_number}, device_name={device_name}, ip={ip_address}"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                INSERT INTO device (device_number, device_name, ip_address, password, port, note, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Chưa kết nối')
                """,
                [device_number, device_name, ip_address, password, port, note],
            )
            con.commit()
            con.close()
            log_to_debug("DeviceRepository: insert() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: insert() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update(self, device_id, device_number, device_name, ip_address, password, port, note):
        """
        Cập nhật thông tin thiết bị
        Args:
            device_id: ID thiết bị
            device_number: Số máy
            device_name: Tên máy
            ip_address: Địa chỉ IP
            password: Mật mã
            port: Cổng kết nối
            note: Ghi chú
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            log_to_debug(
                f"DeviceRepository: update() - id={device_id}, device_number={device_number}"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE device
                SET device_number = ?, device_name = ?, ip_address = ?, 
                    password = ?, port = ?, note = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                [device_number, device_name, ip_address, password, port, note, device_id],
            )
            con.commit()
            con.close()
            log_to_debug("DeviceRepository: update() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: update() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update_status(self, device_id, status):
        """
        Cập nhật trạng thái thiết bị
        Args:
            device_id: ID thiết bị
            status: Trạng thái mới
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            log_to_debug(f"DeviceRepository: update_status() - id={device_id}, status={status}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE device
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                [status, device_id],
            )
            con.commit()
            con.close()
            log_to_debug("DeviceRepository: update_status() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: update_status() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete(self, device_id):
        """
        Xóa thiết bị
        Args:
            device_id: ID thiết bị cần xóa
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            log_to_debug(f"DeviceRepository: delete() - id={device_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM device WHERE id = ?", [device_id])
            con.commit()
            con.close()
            log_to_debug("DeviceRepository: delete() success")
            return True
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: delete() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_all(self):
        """
        Lấy danh sách tất cả thiết bị
        Returns:
            list: Danh sách thiết bị dưới dạng dict
        """
        try:
            log_to_debug("DeviceRepository: get_all() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, device_number, device_name, ip_address, password, 
                       port, status, note, created_at, updated_at
                FROM device
                ORDER BY device_number
                """
            ).fetchall()
            con.close()

            devices = []
            for row in result:
                devices.append(
                    {
                        "id": row[0],
                        "device_number": row[1],
                        "device_name": row[2],
                        "ip_address": row[3],
                        "password": row[4],
                        "port": row[5],
                        "status": row[6],
                        "note": row[7],
                        "created_at": row[8],
                        "updated_at": row[9],
                    }
                )

            log_to_debug(f"DeviceRepository: get_all() returned {len(devices)} devices")
            return devices
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_by_id(self, device_id):
        """
        Lấy thông tin thiết bị theo ID
        Args:
            device_id: ID thiết bị
        Returns:
            dict: Thông tin thiết bị hoặc None
        """
        try:
            log_to_debug(f"DeviceRepository: get_by_id() - id={device_id}")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, device_number, device_name, ip_address, password, 
                       port, status, note, created_at, updated_at
                FROM device
                WHERE id = ?
                """,
                [device_id],
            ).fetchone()
            con.close()

            if result:
                device = {
                    "id": result[0],
                    "device_number": result[1],
                    "device_name": result[2],
                    "ip_address": result[3],
                    "password": result[4],
                    "port": result[5],
                    "status": result[6],
                    "note": result[7],
                    "created_at": result[8],
                    "updated_at": result[9],
                }
                log_to_debug("DeviceRepository: get_by_id() success")
                return device
            else:
                log_to_debug("DeviceRepository: get_by_id() - device not found")
                return None
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: get_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def get_by_device_number(self, device_number):
        """
        Lấy thông tin thiết bị theo số máy
        Args:
            device_number: Số máy
        Returns:
            dict: Thông tin thiết bị hoặc None
        """
        try:
            log_to_debug(f"DeviceRepository: get_by_device_number() - device_number={device_number}")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, device_number, device_name, ip_address, password, 
                       port, status, note, created_at, updated_at
                FROM device
                WHERE device_number = ?
                """,
                [device_number],
            ).fetchone()
            con.close()

            if result:
                device = {
                    "id": result[0],
                    "device_number": result[1],
                    "device_name": result[2],
                    "ip_address": result[3],
                    "password": result[4],
                    "port": result[5],
                    "status": result[6],
                    "note": result[7],
                    "created_at": result[8],
                    "updated_at": result[9],
                }
                log_to_debug("DeviceRepository: get_by_device_number() success")
                return device
            else:
                log_to_debug("DeviceRepository: get_by_device_number() - device not found")
                return None
        except Exception as e:
            log_to_debug(
                f"DeviceRepository: get_by_device_number() error: {e}\n{traceback.format_exc()}"
            )
            return None
