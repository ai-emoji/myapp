import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.attendance_symbol_repository import AttendanceSymbolRepository


class AttendanceSymbolService:
    def __init__(self):
        self.repository = AttendanceSymbolRepository()

    def get_attendance_symbols(self):
        """Lấy cấu hình ký hiệu chấm công"""
        try:
            log_to_debug("AttendanceSymbolService: get_attendance_symbols() called")
            return self.repository.get_attendance_symbols()
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolService: get_attendance_symbols() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def get_enabled_symbols(self):
        """Lấy danh sách ký hiệu chỉ những cái được bật (tích checkbox)"""
        try:
            log_to_debug("AttendanceSymbolService: get_enabled_symbols() called")
            symbols = self.repository.get_attendance_symbols()
            if not symbols:
                return {}

            enabled = {}
            # Chỉ thêm ký hiệu nếu checkbox tương ứng được tích
            if symbols.get("show_late"):
                enabled["late"] = symbols.get("late_symbol", "Tr")
            if symbols.get("show_early_leave"):
                enabled["early_leave"] = symbols.get("early_leave_symbol", "Sm")
            if symbols.get("show_on_time"):
                enabled["on_time"] = symbols.get("on_time_symbol", "X")
            if symbols.get("show_overtime"):
                enabled["overtime"] = symbols.get("overtime_symbol", "+")
            if symbols.get("show_missing_checkout"):
                enabled["missing_checkout"] = symbols.get(
                    "missing_checkout_symbol", "KR"
                )
            if symbols.get("show_missing_checkin"):
                enabled["missing_checkin"] = symbols.get("missing_checkin_symbol", "KV")
            if symbols.get("show_absent"):
                enabled["absent"] = symbols.get("absent_symbol", "V")
            if symbols.get("show_on_time_overnight"):
                enabled["on_time_overnight"] = symbols.get(
                    "on_time_overnight_symbol", "D"
                )
            if symbols.get("show_no_schedule"):
                enabled["no_schedule"] = symbols.get("no_schedule_symbol", "Off")

            log_to_debug(
                f"AttendanceSymbolService: get_enabled_symbols() returned {len(enabled)} enabled symbols"
            )
            return enabled
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolService: get_enabled_symbols() error: {e}\n{traceback.format_exc()}"
            )
            return {}

    def update_attendance_symbols(
        self,
        late_symbol,
        early_leave_symbol,
        on_time_symbol,
        overtime_symbol,
        missing_checkout_symbol,
        missing_checkin_symbol,
        absent_symbol,
        on_time_overnight_symbol,
        no_schedule_symbol,
        show_late,
        show_early_leave,
        show_on_time,
        show_overtime,
        show_missing_checkout,
        show_missing_checkin,
        show_absent,
        show_on_time_overnight,
        show_no_schedule,
    ):
        """Cập nhật cấu hình ký hiệu chấm công"""
        try:
            log_to_debug("AttendanceSymbolService: update_attendance_symbols() called")
            return self.repository.update_attendance_symbols(
                late_symbol,
                early_leave_symbol,
                on_time_symbol,
                overtime_symbol,
                missing_checkout_symbol,
                missing_checkin_symbol,
                absent_symbol,
                on_time_overnight_symbol,
                no_schedule_symbol,
                show_late,
                show_early_leave,
                show_on_time,
                show_overtime,
                show_missing_checkout,
                show_missing_checkin,
                show_absent,
                show_on_time_overnight,
                show_no_schedule,
            )
        except Exception as e:
            log_to_debug(
                f"AttendanceSymbolService: update_attendance_symbols() error: {e}\n{traceback.format_exc()}"
            )
            return False
