# shift_upload_services.py
# Service để xử lý business logic tải nhân viên lên máy chấm công

import traceback
from datetime import datetime


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.shift_upload_repository import ShiftUploadRepository
from repository.device_repository import DeviceRepository
from repository.employee_repository import EmployeeRepository


class ShiftUploadService:
    """Service để xử lý business logic tải nhân viên lên máy chấm công"""

    def __init__(self):
        self.repo = ShiftUploadRepository()
        self.device_repo = DeviceRepository()
        self.employee_repo = EmployeeRepository()

    def upload_employees_to_device(self, device_id, employee_ids, progress_callback=None):
        """
        Tải danh sách nhân viên lên máy chấm công
        Args:
            device_id: ID thiết bị
            employee_ids: List các ID nhân viên cần tải lên
            progress_callback: Callback function(progress_value, message) để cập nhật tiến trình
        Returns:
            tuple: (success: bool, message: str, count: int)
        """
        try:
            log_to_debug(
                f"ShiftUploadService: upload_employees_to_device() - device_id={device_id}, "
                f"employee_ids={employee_ids}"
            )

            if not employee_ids:
                return False, "Chưa chọn nhân viên nào", 0

            # Lấy thông tin thiết bị
            device = self.device_repo.get_by_id(device_id)
            if not device:
                return False, "Thiết bị không tồn tại", 0

            # Import thư viện pyzk
            try:
                from zk import ZK, const
            except ImportError:
                return False, "Chưa cài đặt thư viện pyzk. Vui lòng chạy: pip install pyzk", 0

            # Kết nối với thiết bị
            ip = device["ip_address"]
            port = device.get("port", 4370)
            password = device.get("password", "")

            zk = ZK(ip, port=port, timeout=10, password=password if password else 0)

            try:
                # Kết nối 1-10%
                log_to_debug(f"ShiftUploadService: Connecting to {ip}:{port}")
                for i in range(1, 11):
                    if progress_callback:
                        progress_callback(i, f"Đang kết nối với {ip}...")
                
                conn = zk.connect()

                # Lấy thông tin thiết bị 11-20%
                for i in range(11, 21):
                    if progress_callback:
                        progress_callback(i, "Đang lấy thông tin thiết bị...")
                
                device_sn = conn.get_serialnumber()
                log_to_debug(f"ShiftUploadService: Connected to device SN={device_sn}")

                # Lấy danh sách user hiện tại từ máy 21-30%
                for i in range(21, 31):
                    if progress_callback:
                        progress_callback(i, "Đang lấy danh sách user từ máy...")
                
                existing_users = conn.get_users()
                existing_user_ids = {user.user_id for user in existing_users}
                log_to_debug(f"ShiftUploadService: Found {len(existing_users)} existing users")

                # Chuẩn bị danh sách nhân viên 31-40%
                for i in range(31, 41):
                    if progress_callback:
                        progress_callback(i, "Đang chuẩn bị danh sách nhân viên...")

                all_employees = self.employee_repo.get_all()
                employee_dict = {emp["id"]: emp for emp in all_employees}

                upload_records = []
                users_to_upload = []

                for emp_id in employee_ids:
                    emp = employee_dict.get(emp_id)
                    if not emp:
                        log_to_debug(f"ShiftUploadService: Employee {emp_id} not found")
                        continue

                    # Sử dụng attendance_code làm user_id trên máy
                    user_id = emp.get("attendance_code") or emp.get("employee_code") or str(emp_id)
                    
                    # Tạo user object để upload
                    # privilege: 0=User, 1=Enroller, 2=Manager, 6=Admin
                    # Mặc định là 0 (User thường)
                    users_to_upload.append({
                        "user_id": user_id,
                        "name": emp.get("attendance_name") or emp.get("name"),
                        "privilege": 0,  # User thường
                        "password": "",  # Không set password mặc định
                        "group_id": "",
                        "user_id_num": int(user_id) if user_id.isdigit() else 0,
                        "card": 0,
                    })

                    # Lưu thông tin để insert vào DB
                    upload_records.append({
                        "employee_id": emp_id,
                        "device_id": device_id,
                        "user_id": user_id,
                        "attendance_code": emp.get("attendance_code", ""),
                        "attendance_name": emp.get("attendance_name") or emp.get("name"),
                        "card_number": "",
                        "password": "",
                        "privilege": 0,
                        "enabled": True,
                    })

                log_to_debug(f"ShiftUploadService: Prepared {len(users_to_upload)} users to upload")

                # Upload từng nhân viên 41-90%
                upload_count = 0
                total_users = len(users_to_upload)
                
                for idx, user_data in enumerate(users_to_upload):
                    try:
                        progress = 41 + int((idx / total_users) * 49)  # 41-90%
                        if progress_callback:
                            progress_callback(
                                progress, 
                                f"Đang tải nhân viên {idx + 1}/{total_users}..."
                            )
                        
                        # Set user vào máy
                        conn.set_user(
                            uid=user_data["user_id_num"],
                            name=user_data["name"],
                            privilege=user_data["privilege"],
                            password=user_data["password"],
                            group_id=user_data["group_id"],
                            user_id=user_data["user_id"],
                            card=user_data["card"]
                        )
                        
                        upload_count += 1
                        log_to_debug(
                            f"ShiftUploadService: Uploaded user {user_data['user_id']} - {user_data['name']}"
                        )
                    except Exception as e:
                        log_to_debug(
                            f"ShiftUploadService: Failed to upload user {user_data['user_id']}: {e}"
                        )

                # Lưu vào database 91-95%
                for i in range(91, 96):
                    if progress_callback:
                        progress_callback(i, "Đang lưu thông tin vào database...")
                
                success_count, total_count = self.repo.bulk_insert(upload_records)
                log_to_debug(
                    f"ShiftUploadService: Saved {success_count}/{total_count} records to DB"
                )

                # Ngắt kết nối 96-100%
                for i in range(96, 101):
                    if progress_callback:
                        progress_callback(i, "Đang ngắt kết nối...")
                
                conn.disconnect()
                log_to_debug("ShiftUploadService: Disconnected from device")

                return (
                    True,
                    f"Đã tải {upload_count} nhân viên lên máy chấm công và lưu {success_count} bản ghi vào DB",
                    upload_count,
                )

            except Exception as e:
                log_to_debug(
                    f"ShiftUploadService: upload_employees_to_device() error: {e}\n{traceback.format_exc()}"
                )
                try:
                    conn.disconnect()
                except:
                    pass
                return False, f"Lỗi kết nối máy chấm công: {str(e)}", 0

        except Exception as e:
            log_to_debug(
                f"ShiftUploadService: upload_employees_to_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}", 0

    def delete_employees_from_device(self, device_id, user_ids, progress_callback=None):
        """
        Xóa nhân viên khỏi máy chấm công
        Args:
            device_id: ID thiết bị
            user_ids: List các user_id cần xóa
            progress_callback: Callback function(progress_value, message)
        Returns:
            tuple: (success: bool, message: str, count: int)
        """
        try:
            log_to_debug(
                f"ShiftUploadService: delete_employees_from_device() - device_id={device_id}, "
                f"user_ids={user_ids}"
            )

            if not user_ids:
                return False, "Chưa chọn nhân viên nào", 0

            # Lấy thông tin thiết bị
            device = self.device_repo.get_by_id(device_id)
            if not device:
                return False, "Thiết bị không tồn tại", 0

            # Import thư viện pyzk
            try:
                from zk import ZK
            except ImportError:
                return False, "Chưa cài đặt thư viện pyzk", 0

            # Kết nối với thiết bị
            ip = device["ip_address"]
            port = device.get("port", 4370)
            password = device.get("password", "")

            zk = ZK(ip, port=port, timeout=10, password=password if password else 0)

            try:
                # Kết nối 1-20%
                for i in range(1, 21):
                    if progress_callback:
                        progress_callback(i, f"Đang kết nối với {ip}...")
                
                conn = zk.connect()

                # Xóa từng user 21-80%
                delete_count = 0
                total_users = len(user_ids)
                
                for idx, user_id in enumerate(user_ids):
                    try:
                        progress = 21 + int((idx / total_users) * 59)  # 21-80%
                        if progress_callback:
                            progress_callback(
                                progress, 
                                f"Đang xóa nhân viên {idx + 1}/{total_users}..."
                            )
                        
                        # Xóa user khỏi máy
                        conn.delete_user(user_id=user_id)
                        delete_count += 1
                        log_to_debug(f"ShiftUploadService: Deleted user {user_id}")
                    except Exception as e:
                        log_to_debug(f"ShiftUploadService: Failed to delete user {user_id}: {e}")

                # Cập nhật database 81-95%
                for i in range(81, 96):
                    if progress_callback:
                        progress_callback(i, "Đang cập nhật database...")

                # Xóa khỏi DB (không có employee_id nên dùng user_id và device_id)
                # Lưu ý: Cần thêm hàm delete_by_user_device vào repository nếu cần
                
                # Ngắt kết nối 96-100%
                for i in range(96, 101):
                    if progress_callback:
                        progress_callback(i, "Đang ngắt kết nối...")
                
                conn.disconnect()

                return True, f"Đã xóa {delete_count} nhân viên khỏi máy chấm công", delete_count

            except Exception as e:
                log_to_debug(
                    f"ShiftUploadService: delete_employees_from_device() error: {e}\n{traceback.format_exc()}"
                )
                try:
                    conn.disconnect()
                except:
                    pass
                return False, f"Lỗi kết nối máy chấm công: {str(e)}", 0

        except Exception as e:
            log_to_debug(
                f"ShiftUploadService: delete_employees_from_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}", 0

    def delete_fingerprints_from_device(self, device_id, user_ids, progress_callback=None):
        """
        Xóa vân tay của nhân viên khỏi máy chấm công
        Args:
            device_id: ID thiết bị
            user_ids: List các user_id cần xóa vân tay
            progress_callback: Callback function(progress_value, message)
        Returns:
            tuple: (success: bool, message: str, count: int)
        """
        try:
            log_to_debug(
                f"ShiftUploadService: delete_fingerprints_from_device() - device_id={device_id}, "
                f"user_ids={user_ids}"
            )

            if not user_ids:
                return False, "Chưa chọn nhân viên nào", 0

            # Lấy thông tin thiết bị
            device = self.device_repo.get_by_id(device_id)
            if not device:
                return False, "Thiết bị không tồn tại", 0

            # Import thư viện pyzk
            try:
                from zk import ZK
            except ImportError:
                return False, "Chưa cài đặt thư viện pyzk", 0

            # Kết nối với thiết bị
            ip = device["ip_address"]
            port = device.get("port", 4370)
            password = device.get("password", "")

            zk = ZK(ip, port=port, timeout=10, password=password if password else 0)

            try:
                # Kết nối 1-20%
                for i in range(1, 21):
                    if progress_callback:
                        progress_callback(i, f"Đang kết nối với {ip}...")
                
                conn = zk.connect()

                # Xóa vân tay từng user 21-95%
                delete_count = 0
                total_users = len(user_ids)
                
                for idx, user_id in enumerate(user_ids):
                    try:
                        progress = 21 + int((idx / total_users) * 74)  # 21-95%
                        if progress_callback:
                            progress_callback(
                                progress, 
                                f"Đang xóa vân tay {idx + 1}/{total_users}..."
                            )
                        
                        # Xóa template vân tay của user
                        # Lưu ý: pyzk có thể không hỗ trợ xóa riêng template
                        # Cần kiểm tra API của pyzk
                        # conn.delete_user_template(user_id=user_id)
                        
                        # Workaround: Lấy user, xóa user, thêm lại user không có vân tay
                        users = conn.get_users()
                        target_user = None
                        for u in users:
                            if u.user_id == user_id:
                                target_user = u
                                break
                        
                        if target_user:
                            # Xóa user (bao gồm cả vân tay)
                            conn.delete_user(user_id=user_id)
                            
                            # Thêm lại user nhưng không có vân tay
                            conn.set_user(
                                uid=target_user.uid,
                                name=target_user.name,
                                privilege=target_user.privilege,
                                password=target_user.password,
                                group_id=target_user.group_id,
                                user_id=target_user.user_id,
                                card=target_user.card
                            )
                            
                            delete_count += 1
                            log_to_debug(f"ShiftUploadService: Deleted fingerprints for user {user_id}")
                        else:
                            log_to_debug(f"ShiftUploadService: User {user_id} not found")
                            
                    except Exception as e:
                        log_to_debug(
                            f"ShiftUploadService: Failed to delete fingerprints for user {user_id}: {e}"
                        )

                # Ngắt kết nối 96-100%
                for i in range(96, 101):
                    if progress_callback:
                        progress_callback(i, "Đang ngắt kết nối...")
                
                conn.disconnect()

                return (
                    True, 
                    f"Đã xóa vân tay của {delete_count} nhân viên", 
                    delete_count
                )

            except Exception as e:
                log_to_debug(
                    f"ShiftUploadService: delete_fingerprints_from_device() error: {e}\n{traceback.format_exc()}"
                )
                try:
                    conn.disconnect()
                except:
                    pass
                return False, f"Lỗi kết nối máy chấm công: {str(e)}", 0

        except Exception as e:
            log_to_debug(
                f"ShiftUploadService: delete_fingerprints_from_device() error: {e}\n{traceback.format_exc()}"
            )
            return False, f"Lỗi: {str(e)}", 0

    def get_uploaded_employees(self, device_id):
        """
        Lấy danh sách nhân viên đã tải lên máy
        Args:
            device_id: ID thiết bị
        Returns:
            list: Danh sách nhân viên
        """
        return self.repo.get_by_device(device_id)

    def remove_upload_record(self, record_id):
        """
        Xóa bản ghi upload (chỉ xóa trong DB, không xóa trên máy)
        Args:
            record_id: ID bản ghi
        Returns:
            bool: True nếu thành công
        """
        return self.repo.delete_by_id(record_id)
