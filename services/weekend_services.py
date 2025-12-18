import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.weekend_repository import WeekendRepository


class WeekendService:
    def __init__(self):
        self.repository = WeekendRepository()

    def get_weekend_config(self):
        """Lấy cấu hình ngày cuối tuần"""
        try:
            log_to_debug("WeekendService: get_weekend_config() called")
            return self.repository.get_weekend_config()
        except Exception as e:
            log_to_debug(
                f"WeekendService: get_weekend_config() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def update_weekend_config(
        self, monday, tuesday, wednesday, thursday, friday, saturday, sunday
    ):
        """Cập nhật cấu hình ngày cuối tuần"""
        try:
            log_to_debug("WeekendService: update_weekend_config() called")
            return self.repository.update_weekend_config(
                monday, tuesday, wednesday, thursday, friday, saturday, sunday
            )
        except Exception as e:
            log_to_debug(
                f"WeekendService: update_weekend_config() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_weekend_days(self):
        """Lấy danh sách các ngày được đánh dấu là cuối tuần"""
        try:
            config = self.get_weekend_config()
            if not config:
                return []

            weekend_days = []
            day_names = [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
            day_labels = [
                "Thứ 2",
                "Thứ 3",
                "Thứ 4",
                "Thứ 5",
                "Thứ 6",
                "Thứ 7",
                "Chủ nhật",
            ]

            for i, day in enumerate(day_names):
                if config.get(day, False):
                    weekend_days.append(day_labels[i])

            return weekend_days
        except Exception as e:
            log_to_debug(
                f"WeekendService: get_weekend_days() error: {e}\n{traceback.format_exc()}"
            )
            return []
