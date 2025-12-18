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


class JobTitleRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng job_title nếu chưa tồn tại"""
        try:
            log_to_debug("JobTitleRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_job_title START 1")
            except Exception:
                # Sequence đã tồn tại, bỏ qua im lặng
                pass

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS job_title (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_job_title'),
                    name VARCHAR UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            con.close()
            log_to_debug("JobTitleRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_all_job_titles(self):
        """Lấy tất cả chức danh"""
        try:
            log_to_debug("JobTitleRepository: get_all_job_titles() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, name FROM job_title ORDER BY id ASC"
            ).fetchall()
            con.close()

            job_titles = [{"id": row[0], "name": row[1]} for row in result]
            log_to_debug(
                f"JobTitleRepository: get_all_job_titles() returned {len(job_titles)} records"
            )
            return job_titles
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: get_all_job_titles() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_job_title_by_id(self, job_title_id):
        """Lấy chức danh theo ID"""
        try:
            log_to_debug(
                f"JobTitleRepository: get_job_title_by_id({job_title_id}) called"
            )
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, name FROM job_title WHERE id=?", [job_title_id]
            ).fetchone()
            con.close()

            if result:
                job_title = {"id": result[0], "name": result[1]}
                log_to_debug(
                    f"JobTitleRepository: get_job_title_by_id() found: {job_title}"
                )
                return job_title

            log_to_debug(f"JobTitleRepository: get_job_title_by_id() not found")
            return None
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: get_job_title_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def add_job_title(self, name):
        """Thêm chức danh mới"""
        try:
            log_to_debug(f"JobTitleRepository: add_job_title(name={name}) called")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("INSERT INTO job_title (name) VALUES (?)", [name])
            con.close()
            log_to_debug(f"JobTitleRepository: add_job_title() inserted successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: add_job_title() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update_job_title(self, job_title_id, name):
        """Cập nhật chức danh"""
        try:
            log_to_debug(
                f"JobTitleRepository: update_job_title(id={job_title_id}, name={name}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "UPDATE job_title SET name=?, updated_at=now() WHERE id=?",
                [name, job_title_id],
            )
            con.close()
            log_to_debug(f"JobTitleRepository: update_job_title() updated successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: update_job_title() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete_job_title(self, job_title_id):
        """Xóa chức danh"""
        try:
            log_to_debug(
                f"JobTitleRepository: delete_job_title(id={job_title_id}) called"
            )
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM job_title WHERE id=?", [job_title_id])

            # Kiểm tra xem còn bản ghi nào không
            count_result = con.execute("SELECT COUNT(*) FROM job_title").fetchone()
            record_count = count_result[0] if count_result else 0

            # Nếu không còn bản ghi nào, reset sequence bằng cách drop và tạo lại
            if record_count == 0:
                try:
                    con.execute("DROP SEQUENCE seq_job_title")
                    con.execute("CREATE SEQUENCE seq_job_title START 1")
                    log_to_debug("JobTitleRepository: Sequence dropped and recreated")
                except Exception as seq_error:
                    log_to_debug(
                        f"JobTitleRepository: Error resetting sequence: {seq_error}"
                    )

            con.close()
            log_to_debug(f"JobTitleRepository: delete_job_title() deleted successfully")
            return True
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: delete_job_title() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_total_count(self):
        """Lấy tổng số chức danh"""
        try:
            log_to_debug("JobTitleRepository: get_total_count() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute("SELECT COUNT(*) FROM job_title").fetchone()
            con.close()

            total = result[0] if result else 0
            log_to_debug(f"JobTitleRepository: get_total_count() returned {total}")
            return total
        except Exception as e:
            log_to_debug(
                f"JobTitleRepository: get_total_count() error: {e}\n{traceback.format_exc()}"
            )
            return 0
