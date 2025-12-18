import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


# declare_work_shift_services.py
# Service layer cho khai báo ca làm việc
from repository.declare_work_shift_repository import DeclareWorkShiftRepository


class DeclareWorkShiftService:
    def __init__(self):
        self.repo = DeclareWorkShiftRepository()

    def get_all_work_shifts(self):
        """Lấy tất cả ca làm việc"""
        log_to_debug("DeclareWorkShiftService: get_all_work_shifts() called")
        result = self.repo.get_all_work_shifts()
        log_to_debug(
            f"DeclareWorkShiftService: get_all_work_shifts() returned {len(result)} records"
        )
        return result

    def get_work_shift_by_id(self, work_shift_id):
        """Lấy ca làm việc theo ID"""
        log_to_debug(
            f"DeclareWorkShiftService: get_work_shift_by_id({work_shift_id}) called"
        )
        result = self.repo.get_work_shift_by_id(work_shift_id)
        log_to_debug(
            f"DeclareWorkShiftService: get_work_shift_by_id() result: {result}"
        )
        return result

    def add_work_shift(
        self,
        shift_code,
        start_time,
        end_time,
        lunch_start,
        lunch_end,
        total_minutes,
        work_day_count,
    ):
        """Thêm ca làm việc mới"""
        log_to_debug(
            f"DeclareWorkShiftService: add_work_shift(shift_code={shift_code}) called"
        )
        result = self.repo.add_work_shift(
            shift_code,
            start_time,
            end_time,
            lunch_start,
            lunch_end,
            total_minutes,
            work_day_count,
        )
        log_to_debug(f"DeclareWorkShiftService: add_work_shift() result: {result}")
        return result

    def update_work_shift(
        self,
        work_shift_id,
        shift_code,
        start_time,
        end_time,
        lunch_start,
        lunch_end,
        total_minutes,
        work_day_count,
    ):
        """Cập nhật ca làm việc"""
        log_to_debug(
            f"DeclareWorkShiftService: update_work_shift(id={work_shift_id}) called"
        )
        result = self.repo.update_work_shift(
            work_shift_id,
            shift_code,
            start_time,
            end_time,
            lunch_start,
            lunch_end,
            total_minutes,
            work_day_count,
        )
        log_to_debug(f"DeclareWorkShiftService: update_work_shift() result: {result}")
        return result

    def delete_work_shift(self, work_shift_id):
        """Xóa ca làm việc"""
        log_to_debug(
            f"DeclareWorkShiftService: delete_work_shift(id={work_shift_id}) called"
        )
        result = self.repo.delete_work_shift(work_shift_id)
        log_to_debug(f"DeclareWorkShiftService: delete_work_shift() result: {result}")
        return result

    def get_total_count(self):
        """Lấy tổng số ca làm việc"""
        log_to_debug("DeclareWorkShiftService: get_total_count() called")
        result = self.repo.get_total_count()
        log_to_debug(f"DeclareWorkShiftService: get_total_count() result: {result}")
        return result
