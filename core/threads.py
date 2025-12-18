# QThread / Worker cho tác vụ nền
# Tất cả comment, docstring đều bằng tiếng Việt
from PySide6.QtCore import QThread, Signal


class BaseWorker(QThread):
    """
    Mô tả:
            Lớp cơ sở cho các worker chạy nền bằng QThread.
            Có thể kế thừa để xử lý các tác vụ nặng, truy vấn database, v.v.
    Args:
            parent: Đối tượng cha (nếu có)
    """

    finished = Signal(object)
    error = Signal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = None
        self._error = None

    def run(self):
        """
        Mô tả:
                Ghi đè phương thức này để thực thi logic nền.
        Returns:
                None
        """
        try:
            self._result = self.do_work()
            self.finished.emit(self._result)
        except Exception as e:
            self._error = e
            self.error.emit(e)

    def do_work(self):
        """
        Mô tả:
                Ghi đè hàm này để thực hiện tác vụ nền cụ thể.
        Returns:
                object: Kết quả trả về sau khi xử lý
        """
        pass
