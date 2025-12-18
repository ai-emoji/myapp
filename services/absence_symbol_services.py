import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.absence_symbol_repository import AbsenceSymbolRepository


class AbsenceSymbolService:
    def __init__(self):
        self.repository = AbsenceSymbolRepository()

    def get_all(self):
        """Lấy tất cả ký hiệu loại vắng"""
        try:
            log_to_debug("AbsenceSymbolService: get_all() called")
            return self.repository.get_all()
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolService: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def update(self, symbol_id, code, description, symbol, is_used, is_paid):
        """Cập nhật ký hiệu loại vắng"""
        try:
            log_to_debug("AbsenceSymbolService: update() called")
            return self.repository.update(
                symbol_id, code, description, symbol, is_used, is_paid
            )
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolService: update() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def add(self, code, description, symbol, is_used, is_paid):
        """Thêm ký hiệu loại vắng mới"""
        try:
            log_to_debug("AbsenceSymbolService: add() called")
            return self.repository.add(code, description, symbol, is_used, is_paid)
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolService: add() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete(self, symbol_id):
        """Xóa ký hiệu loại vắng"""
        try:
            log_to_debug("AbsenceSymbolService: delete() called")
            return self.repository.delete(symbol_id)
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolService: delete() error: {e}\n{traceback.format_exc()}"
            )
            return False
