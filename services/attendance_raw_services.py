import traceback
from datetime import datetime


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.attendance_raw_repository import AttendanceRawRepository
from repository.device_repository import DeviceRepository


class AttendanceRawService:
    """Service để xử lý business logic cho dữ liệu chấm công"""

    def __init__(self):
        self.repo = AttendanceRawRepository()
        self.device_repo = DeviceRepository()

    def download_from_device(self, device_id, from_date=None, to_date=None, progress_callback=None):
        """
        Tải dữ liệu chấm công từ thiết bị
        Args:
            device_id: ID thiết bị
            from_date: Từ ngày (datetime.date, optional)
            to_date: Đến ngày (datetime.date, optional)
            progress_callback: Callback function(current, total, message) để cập nhật tiến trình
        Returns:
            tuple: (success: bool, message: str, count: int)
        """
        try:
            log_to_debug(
                f"AttendanceRawService: download_from_device() - device_id={device_id}, "
                f"from={from_date}, to={to_date}"
            )

            # Lấy thông tin thiết bị
            device = self.device_repo.get_by_id(device_id)
            if not device:
                return False, "Thiết bị không tồn tại", 0

            # Import thư viện pyzk
            try:
                from zk import ZK
            except ImportError:
                return False, "Chưa cài đặt thư viện pyzk. Vui lòng chạy: pip install pyzk", 0

            # Kết nối với thiết bị
            ip = device["ip_address"]
            port = device.get("port", 4370)
            password = device.get("password", "")

            zk = ZK(ip, port=port, timeout=10, password=password if password else 0)

            try:
                log_to_debug(f"AttendanceRawService: Connecting to {ip}:{port}")
                # Kết nối 1-10%
                for i in range(1, 11):
                    if progress_callback:
                        progress_callback(i, f"Đang kết nối với {ip}...")
                
                conn = zk.connect()

                # Lấy thông tin thiết bị 11-20%
                for i in range(11, 21):
                    if progress_callback:
                        progress_callback(i, "Đang lấy thông tin thiết bị...")
                
                device_sn = conn.get_serialnumber()
                log_to_debug(f"AttendanceRawService: Connected to device SN={device_sn}")

                # Lấy dữ liệu chấm công 21-50%
                log_to_debug("AttendanceRawService: Fetching attendance records...")
                for i in range(21, 41):
                    if progress_callback:
                        progress_callback(i, "Đang tải dữ liệu chấm công...")
                
                attendances = conn.get_attendance()
                log_to_debug(f"AttendanceRawService: Fetched {len(attendances)} records")
                
                for i in range(41, 51):
                    if progress_callback:
                        progress_callback(i, "Đã tải xong dữ liệu chấm công...")

                # Lấy danh sách users 51-65%
                for i in range(51, 61):
                    if progress_callback:
                        progress_callback(i, "Đang tải danh sách nhân viên...")
                
                users = conn.get_users()
                user_dict = {user.user_id: user.name for user in users}
                log_to_debug(f"AttendanceRawService: Loaded {len(users)} users")

                # Ngắt kết nối
                for i in range(61, 66):
                    if progress_callback:
                        progress_callback(i, "Đang ngắt kết nối...")
                        
                conn.disconnect()
                log_to_debug("AttendanceRawService: Disconnected from device")
                
                # Lọc dữ liệu 66-75%
                for i in range(66, 76):
                    if progress_callback:
                        progress_callback(i, "Đang lọc dữ liệu...")

                # Lọc theo khoảng ngày nếu có
                filtered_records = []
                for att in attendances:
                    att_date = att.timestamp.date()
                    
                    # Kiểm tra khoảng ngày
                    if from_date and att_date < from_date:
                        continue
                    if to_date and att_date > to_date:
                        continue
                    
                    filtered_records.append(att)

                log_to_debug(
                    f"AttendanceRawService: Filtered to {len(filtered_records)} records "
                    f"(from {len(attendances)} total)"
                )
                
                # Chuẩn bị dữ liệu 76-85%
                for i in range(76, 86):
                    if progress_callback:
                        progress_callback(i, "Đang chuẩn bị dữ liệu...")

                # Chuẩn bị dữ liệu để insert
                records_to_insert = []
                for att in filtered_records:
                    user_name = user_dict.get(att.user_id, "")
                    
                    record = (
                        str(att.user_id),           # user_id
                        user_name,                  # user_name
                        att.timestamp,              # timestamp
                        att.status,                 # status
                        att.punch,                  # punch
                        att.uid if hasattr(att, 'uid') else 0,  # uid
                        device_sn,                  # device_sn
                        device_id,                  # device_id
                        "",                         # note
                    )
                    records_to_insert.append(record)

                # Bulk insert vào database 86-100%
                if records_to_insert:
                    for i in range(86, 96):
                        if progress_callback:
                            progress_callback(i, "Đang lưu vào cơ sở dữ liệu...")
                    
                    success_count, total = self.repo.bulk_insert(records_to_insert)
                    log_to_debug(
                        f"AttendanceRawService: Inserted {success_count}/{total} records into database"
                    )
                    
                    for i in range(96, 101):
                        if progress_callback:
                            progress_callback(i, "Hoàn tất lưu dữ liệu...")
                    
                    return True, f"Tải thành công {success_count} bản ghi mới (tổng {total} bản ghi)", success_count
                else:
                    return True, "Không có dữ liệu trong khoảng thời gian đã chọn", 0

            except Exception as conn_error:
                log_to_debug(f"AttendanceRawService: Connection error: {conn_error}")
                return False, f"Lỗi kết nối: {str(conn_error)}", 0

        except Exception as e:
            log_to_debug(
                f"AttendanceRawService: download_from_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}", 0

    def get_all_records(self, from_date=None, to_date=None, device_id=None):
        """
        Lấy tất cả dữ liệu chấm công
        Args:
            from_date: Từ ngày (optional)
            to_date: Đến ngày (optional)
            device_id: ID thiết bị (optional)
        Returns:
            list: Danh sách bản ghi
        """
        try:
            log_to_debug("AttendanceRawService: get_all_records() called")
            return self.repo.get_all(from_date, to_date, device_id)
        except Exception as e:
            log_to_debug(
                f"AttendanceRawService: get_all_records() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def delete_all_records(self):
        """
        Xóa toàn bộ dữ liệu chấm công
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            log_to_debug("AttendanceRawService: delete_all_records() called")
            success = self.repo.delete_all()
            
            if success:
                return True, "Đã xóa toàn bộ dữ liệu chấm công"
            else:
                return False, "Lỗi khi xóa dữ liệu"
        except Exception as e:
            log_to_debug(
                f"AttendanceRawService: delete_all_records() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}"

    def delete_record_by_id(self, record_id):
        """
        Xóa một bản ghi theo ID
        Args:
            record_id: ID của bản ghi cần xóa
        Returns:
            bool: True nếu thành công
        """
        try:
            log_to_debug(f"AttendanceRawService: delete_record_by_id() - id={record_id}")
            return self.repo.delete_by_id(record_id)
        except Exception as e:
            log_to_debug(
                f"AttendanceRawService: delete_record_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_record_count(self):
        """
        Đếm số bản ghi
        Returns:
            int: Số lượng bản ghi
        """
        try:
            return self.repo.get_count()
        except Exception as e:
            log_to_debug(
                f"AttendanceRawService: get_record_count() error: {e}\n{traceback.format_exc()}"
            )
            return 0
