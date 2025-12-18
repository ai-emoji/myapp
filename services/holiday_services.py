import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


# holiday_services.py
# Service layer cho ngày nghỉ
from repository.holiday_repository import HolidayRepository


class HolidayService:
    def __init__(self):
        self.repo = HolidayRepository()

    def get_all_holidays(self):
        """Lấy tất cả ngày nghỉ"""
        log_to_debug("HolidayService: get_all_holidays() called")
        result = self.repo.get_all_holidays()
        log_to_debug(
            f"HolidayService: get_all_holidays() returned {len(result)} records"
        )
        return result

    def get_holiday_by_id(self, holiday_id):
        """Lấy ngày nghỉ theo ID"""
        log_to_debug(f"HolidayService: get_holiday_by_id({holiday_id}) called")
        result = self.repo.get_holiday_by_id(holiday_id)
        log_to_debug(f"HolidayService: get_holiday_by_id() result: {result}")
        return result

    def add_holiday(self, holiday_date, name):
        """Thêm ngày nghỉ mới"""
        log_to_debug(
            f"HolidayService: add_holiday(date={holiday_date}, name={name}) called"
        )
        result = self.repo.add_holiday(holiday_date, name)
        log_to_debug(f"HolidayService: add_holiday() result: {result}")
        return result

    def update_holiday(self, holiday_id, holiday_date, name):
        """Cập nhật ngày nghỉ"""
        log_to_debug(
            f"HolidayService: update_holiday(id={holiday_id}, date={holiday_date}, name={name}) called"
        )
        result = self.repo.update_holiday(holiday_id, holiday_date, name)
        log_to_debug(f"HolidayService: update_holiday() result: {result}")
        return result

    def delete_holiday(self, holiday_id):
        """Xóa ngày nghỉ"""
        log_to_debug(f"HolidayService: delete_holiday(id={holiday_id}) called")
        result = self.repo.delete_holiday(holiday_id)
        log_to_debug(f"HolidayService: delete_holiday() result: {result}")
        return result

    def get_total_count(self):
        """Lấy tổng số ngày nghỉ"""
        log_to_debug("HolidayService: get_total_count() called")
        result = self.repo.get_total_count()
        log_to_debug(f"HolidayService: get_total_count() result: {result}")
        return result
