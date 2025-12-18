import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.device_repository import DeviceRepository


class DeviceService:
    """Service để xử lý business logic cho thiết bị chấm công"""

    def __init__(self):
        self.repo = DeviceRepository()

    def get_all_devices(self):
        """
        Lấy danh sách tất cả thiết bị
        Returns:
            list: Danh sách thiết bị
        """
        try:
            log_to_debug("DeviceService: get_all_devices() called")
            devices = self.repo.get_all()
            log_to_debug(f"DeviceService: get_all_devices() returned {len(devices)} devices")
            return devices
        except Exception as e:
            log_to_debug(
                f"DeviceService: get_all_devices() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def add_device(self, device_number, device_name, ip_address, password="", port=4370, note=""):
        """
        Thêm thiết bị mới
        Args:
            device_number: Số máy
            device_name: Tên máy
            ip_address: Địa chỉ IP
            password: Mật mã
            port: Cổng kết nối
            note: Ghi chú
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            log_to_debug(
                f"DeviceService: add_device() - device_number={device_number}, device_name={device_name}"
            )

            # Validate input
            if not device_number or not device_number.strip():
                return False, "Số máy không được để trống"

            if not device_name or not device_name.strip():
                return False, "Tên máy không được để trống"

            if not ip_address or not ip_address.strip():
                return False, "Địa chỉ IP không được để trống"

            # Validate IP address format
            if not self._validate_ip(ip_address):
                return False, "Địa chỉ IP không hợp lệ"

            # Validate port
            try:
                port = int(port)
                if port < 1 or port > 65535:
                    return False, "Cổng kết nối phải từ 1 đến 65535"
            except ValueError:
                return False, "Cổng kết nối phải là số"

            # Kiểm tra số máy đã tồn tại chưa
            existing = self.repo.get_by_device_number(device_number.strip())
            if existing:
                return False, f"Số máy '{device_number}' đã tồn tại"

            # Insert vào database
            success = self.repo.insert(
                device_number.strip(),
                device_name.strip(),
                ip_address.strip(),
                password.strip() if password else "",
                port,
                note.strip() if note else "",
            )

            if success:
                log_to_debug("DeviceService: add_device() success")
                return True, "Thêm thiết bị thành công"
            else:
                return False, "Lỗi khi thêm thiết bị vào database"

        except Exception as e:
            log_to_debug(
                f"DeviceService: add_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}"

    def update_device(self, device_id, device_number, device_name, ip_address, password, port, note):
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
            tuple: (success: bool, message: str)
        """
        try:
            log_to_debug(f"DeviceService: update_device() - id={device_id}")

            # Validate input
            if not device_number or not device_number.strip():
                return False, "Số máy không được để trống"

            if not device_name or not device_name.strip():
                return False, "Tên máy không được để trống"

            if not ip_address or not ip_address.strip():
                return False, "Địa chỉ IP không được để trống"

            # Validate IP address format
            if not self._validate_ip(ip_address):
                return False, "Địa chỉ IP không hợp lệ"

            # Validate port
            try:
                port = int(port)
                if port < 1 or port > 65535:
                    return False, "Cổng kết nối phải từ 1 đến 65535"
            except ValueError:
                return False, "Cổng kết nối phải là số"

            # Kiểm tra số máy đã tồn tại cho thiết bị khác chưa
            existing = self.repo.get_by_device_number(device_number.strip())
            if existing and existing["id"] != device_id:
                return False, f"Số máy '{device_number}' đã được sử dụng bởi thiết bị khác"

            # Update database
            success = self.repo.update(
                device_id,
                device_number.strip(),
                device_name.strip(),
                ip_address.strip(),
                password.strip() if password else "",
                port,
                note.strip() if note else "",
            )

            if success:
                log_to_debug("DeviceService: update_device() success")
                return True, "Cập nhật thiết bị thành công"
            else:
                return False, "Lỗi khi cập nhật thiết bị"

        except Exception as e:
            log_to_debug(
                f"DeviceService: update_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}"

    def delete_device(self, device_id):
        """
        Xóa thiết bị
        Args:
            device_id: ID thiết bị
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            log_to_debug(f"DeviceService: delete_device() - id={device_id}")

            # Kiểm tra thiết bị có tồn tại không
            device = self.repo.get_by_id(device_id)
            if not device:
                return False, "Thiết bị không tồn tại"

            # Xóa thiết bị
            success = self.repo.delete(device_id)

            if success:
                log_to_debug("DeviceService: delete_device() success")
                return True, "Xóa thiết bị thành công"
            else:
                return False, "Lỗi khi xóa thiết bị"

        except Exception as e:
            log_to_debug(
                f"DeviceService: delete_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}"

    def get_device_by_id(self, device_id):
        """
        Lấy thông tin thiết bị theo ID
        Args:
            device_id: ID thiết bị
        Returns:
            dict: Thông tin thiết bị hoặc None
        """
        try:
            log_to_debug(f"DeviceService: get_device_by_id() - id={device_id}")
            return self.repo.get_by_id(device_id)
        except Exception as e:
            log_to_debug(
                f"DeviceService: get_device_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def test_connection(self, ip_address, port, password=""):
        """
        Test kết nối với thiết bị chấm công
        Args:
            ip_address: Địa chỉ IP
            port: Cổng kết nối
            password: Mật mã
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            log_to_debug(f"DeviceService: test_connection() - ip={ip_address}, port={port}")

            # Import thư viện pyzk để kết nối với máy chấm công
            try:
                from zk import ZK
            except ImportError:
                return False, "Chưa cài đặt thư viện pyzk. Vui lòng chạy: pip install pyzk"

            # Tạo kết nối
            zk = ZK(ip_address, port=port, timeout=5, password=password if password else 0)

            try:
                # Kết nối với thiết bị
                conn = zk.connect()

                # Lấy thông tin thiết bị
                device_name = conn.get_device_name()
                serial_number = conn.get_serialnumber()
                firmware_version = conn.get_firmware_version()
                users_count = len(conn.get_users())

                # Ngắt kết nối
                conn.disconnect()

                message = (
                    f"Kết nối thành công!\n"
                    f"Tên thiết bị: {device_name}\n"
                    f"Serial: {serial_number}\n"
                    f"Firmware: {firmware_version}\n"
                    f"Số người dùng: {users_count}"
                )

                log_to_debug(f"DeviceService: test_connection() success - {message}")
                return True, message

            except Exception as conn_error:
                log_to_debug(f"DeviceService: Connection error: {conn_error}")
                return False, f"Không thể kết nối: {str(conn_error)}"

        except Exception as e:
            log_to_debug(
                f"DeviceService: test_connection() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}"

    def update_device_status(self, device_id, status):
        """
        Cập nhật trạng thái thiết bị
        Args:
            device_id: ID thiết bị
            status: Trạng thái mới
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(f"DeviceService: update_device_status() - id={device_id}, status={status}")
            return self.repo.update_status(device_id, status)
        except Exception as e:
            log_to_debug(
                f"DeviceService: update_device_status() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def _validate_ip(self, ip_address):
        """
        Validate IP address format
        Args:
            ip_address: Địa chỉ IP cần kiểm tra
        Returns:
            bool: True nếu hợp lệ
        """
        try:
            parts = ip_address.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except:
            return False
