import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


# job_title_services.py
# Service layer cho chức danh
from repository.job_title_repository import JobTitleRepository


class JobTitleService:
    def __init__(self):
        self.repo = JobTitleRepository()

    def get_all_job_titles(self):
        """Lấy tất cả chức danh"""
        log_to_debug("JobTitleService: get_all_job_titles() called")
        result = self.repo.get_all_job_titles()
        log_to_debug(
            f"JobTitleService: get_all_job_titles() returned {len(result)} records"
        )
        return result

    def get_job_title_by_id(self, job_title_id):
        """Lấy chức danh theo ID"""
        log_to_debug(f"JobTitleService: get_job_title_by_id({job_title_id}) called")
        result = self.repo.get_job_title_by_id(job_title_id)
        log_to_debug(f"JobTitleService: get_job_title_by_id() result: {result}")
        return result

    def add_job_title(self, name):
        """Thêm chức danh mới"""
        log_to_debug(f"JobTitleService: add_job_title(name={name}) called")
        result = self.repo.add_job_title(name)
        log_to_debug(f"JobTitleService: add_job_title() result: {result}")
        return result

    def update_job_title(self, job_title_id, name):
        """Cập nhật chức danh"""
        log_to_debug(
            f"JobTitleService: update_job_title(id={job_title_id}, name={name}) called"
        )
        result = self.repo.update_job_title(job_title_id, name)
        log_to_debug(f"JobTitleService: update_job_title() result: {result}")
        return result

    def delete_job_title(self, job_title_id):
        """Xóa chức danh"""
        log_to_debug(f"JobTitleService: delete_job_title(id={job_title_id}) called")
        result = self.repo.delete_job_title(job_title_id)
        log_to_debug(f"JobTitleService: delete_job_title() result: {result}")
        return result

    def get_total_count(self):
        """Lấy tổng số chức danh"""
        log_to_debug("JobTitleService: get_total_count() called")
        result = self.repo.get_total_count()
        log_to_debug(f"JobTitleService: get_total_count() result: {result}")
        return result
