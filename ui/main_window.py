# UI chính – chỉ gọi Service
# Tạm thời để trống, sẽ hoàn thiện sau

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QVBoxLayout
from core.resource import (
    MIN_MAINWINDOW_WIDTH,
    MIN_MAINWINDOW_HEIGHT,
    MAIN_HEIGHT,
    APP_ICO_PATH,
)
from ui.controllers.controllers_header import HeaderController


class MainWindow(QMainWindow):

    def _set_app_icon(self, icon_path):
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(64, 64)
            self.setWindowIcon(QIcon(scaled_pixmap))
        else:
            self.setWindowIcon(QIcon(icon_path))

    # Thiết lập tiêu đề cửa sổ

    def __init__(self, parent=None):
        super().__init__(parent)
        # Thiết lập kích thước cửa sổ chính
        self.setMinimumWidth(MIN_MAINWINDOW_WIDTH)
        self.setMinimumHeight(MIN_MAINWINDOW_HEIGHT)

        # Thiết lập icon cho cửa sổ sắc nét hơn
        self._set_app_icon(APP_ICO_PATH)
        self.setWindowTitle("Quản lý công ty - Ứng dụng PySide6")

        # Tạo widget cho từng phần
        # Widget tổng
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout dọc chia 3 phần
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        from ui.common.widgets_header import (
            WidgetsHeader,
            WidgetsHeader1,
            WidgetsHeader2,
        )

        self.header = WidgetsHeader()
        self.header.setObjectName("Header")
        # Lồng 2 phần header con vào header tổng
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        self.header1 = WidgetsHeader1()
        self.header2 = WidgetsHeader2()
        header_layout.addWidget(self.header1)
        header_layout.addWidget(self.header2)
        main_layout.addWidget(self.header)
        # Khởi tạo controller cho header để điều khiển hiển thị nhóm nút
        self.header_controller = HeaderController(self.header1, self.header2, self)

        # Main content co giãn tự động giữa header và footer
        self.main_content = QFrame()
        self.main_content.setObjectName("MainContent")
        main_layout.addWidget(self.main_content, 1)  # stretch factor 1

        # Footer luôn ở cuối trang
        from ui.common.widgets_footer import WidgetsFooter

        self.footer = WidgetsFooter()
        main_layout.addWidget(self.footer)

    def set_main_content(self, widget):
        """Thay thế nội dung chính bằng widget mới"""
        # Xóa widget cũ trong main_content (nếu có)
        layout = self.main_content.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().setParent(None)
        else:
            from PySide6.QtWidgets import QVBoxLayout

            layout = QVBoxLayout(self.main_content)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        layout.addWidget(widget)

    def connect_company_icon_signal(self, company_controller):
        """Được gọi từ DialogCompany để kết nối signal icon_changed vào MainWindow"""
        try:
            company_controller.icon_changed.connect(self._on_icon_changed)
        except Exception as e:
            print(f"[MainWindow] Không thể kết nối signal icon_changed từ dialog: {e}")

    def _on_icon_changed(self, icon_path):
        """Cập nhật lại icon cửa sổ khi icon thay đổi realtime"""
        self._set_app_icon(icon_path)
