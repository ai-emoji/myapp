# Điểm khởi đầu ứng dụng
# Tuân thủ Clean Architecture, PySide6, resource_path, logging
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from core.resource import (
    APP_ICO_PATH,
    MIN_MAINWINDOW_WIDTH,
    MIN_MAINWINDOW_HEIGHT,
    resource_path,
)
from ui.main_window import MainWindow


def setup_logging():
    """
    Mô tả:
            Thiết lập logging ghi vào log/debug.log
    Args:
            None
    Returns:
            None
    """
    log_path = resource_path("log/debug.log")
    logging.basicConfig(
        filename=log_path,
        filemode="a",
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.DEBUG,
        encoding="utf-8",
    )


def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon(APP_ICO_PATH))
    window.setMinimumWidth(MIN_MAINWINDOW_WIDTH)
    window.setMinimumHeight(MIN_MAINWINDOW_HEIGHT)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
