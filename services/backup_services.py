# backup_services.py
# Service xử lý backup và restore database

import shutil
import os
from datetime import datetime
from core.database import Database


class BackupService:
    """
    Mô tả:
        Service xử lý backup và restore database
    """

    @staticmethod
    def backup_database(destination_path: str) -> tuple[bool, str]:
        """
        Mô tả:
            Backup database hiện tại đến đường dẫn chỉ định
        Args:
            destination_path: Đường dẫn đầy đủ đến file backup (bao gồm tên file)
        Returns:
            tuple[bool, str]: (success, message)
        """
        try:
            source_path = Database.get_db_path()

            # Kiểm tra file database có tồn tại không
            if not os.path.exists(source_path):
                return False, "Database không tồn tại"

            # Đảm bảo thư mục đích tồn tại
            dest_dir = os.path.dirname(destination_path)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            # Copy file database
            shutil.copy2(source_path, destination_path)

            # Kiểm tra file đã copy thành công
            if os.path.exists(destination_path):
                file_size = os.path.getsize(destination_path)
                return True, f"Backup thành công! Kích thước: {file_size:,} bytes"
            else:
                return False, "Backup thất bại - file không được tạo"

        except PermissionError:
            return False, "Không có quyền truy cập vào thư mục đích"
        except Exception as e:
            return False, f"Lỗi khi backup: {str(e)}"

    @staticmethod
    def restore_database(source_path: str) -> tuple[bool, str]:
        """
        Mô tả:
            Restore database từ file backup
        Args:
            source_path: Đường dẫn đến file backup
        Returns:
            tuple[bool, str]: (success, message)
        """
        try:
            # Kiểm tra file backup có tồn tại không
            if not os.path.exists(source_path):
                return False, "File backup không tồn tại"

            # Kiểm tra có phải file .duckdb không
            if not source_path.lower().endswith(".duckdb"):
                return False, "File không đúng định dạng (.duckdb)"

            dest_path = Database.get_db_path()

            # Backup file hiện tại trước khi restore (phòng ngừa)
            if os.path.exists(dest_path):
                # Tạo tên file backup: YYYYMMDD_backup_app.duckdb
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_dir = os.path.dirname(dest_path)
                backup_old = os.path.join(dest_dir, f"{timestamp}_backup_app.duckdb")
                shutil.copy2(dest_path, backup_old)

            # Copy file backup vào vị trí database
            shutil.copy2(source_path, dest_path)

            # Kiểm tra restore thành công
            if os.path.exists(dest_path):
                return True, "Restore thành công! Vui lòng khởi động lại ứng dụng."
            else:
                return False, "Restore thất bại - file không được copy"

        except PermissionError:
            return False, "Không có quyền ghi vào thư mục database"
        except Exception as e:
            return False, f"Lỗi khi restore: {str(e)}"

    @staticmethod
    def get_default_backup_filename() -> str:
        """
        Mô tả:
            Tạo tên file backup mặc định với timestamp
        Returns:
            str: Tên file backup (VD: backup_20231217_143025.duckdb)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}.duckdb"
