# Quản lý kết nối DuckDB
# Tất cả comment, docstring đều bằng tiếng Việt

import duckdb
import os
from core.resource import resource_path, DB_PATH


class Database:
    """
    Mô tả:
        Quản lý kết nối tới cơ sở dữ liệu DuckDB.
        Không giữ connection lâu, mỗi lần gọi sẽ tạo kết nối mới.
    """

    @staticmethod
    def get_db_path() -> str:
        """
        Mô tả:
            Trả về đường dẫn tuyệt đối tới file database DuckDB.
            CHỈ CÓ HÀM NÀY quyết định database nằm ở đâu.
        """
        return DB_PATH

    @staticmethod
    def connect(read_only=False):
        """
        Mô tả:
            Tạo và trả về kết nối DuckDB.
        Args:
            read_only: Nếu True, mở ở chế độ chỉ đọc (cho phép nhiều kết nối đồng thời)
        """
        db_path = Database.get_db_path()

        # Đảm bảo thư mục database tồn tại
        parent_dir = os.path.dirname(db_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        return duckdb.connect(db_path, read_only=read_only)
