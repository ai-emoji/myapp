# Footer dùng chung
# Tất cả comment, docstring đều bằng tiếng Việt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from core.resource import (
    FOOTER_MIN_WIDTH,
    FOOTER_HEIGHT,
    FOOTER_MIN_WIDTH,
    FOOTER_BG,
    FONT_WEIGHT_BOLD,
)
from PySide6.QtCore import QTimer, QDateTime


class WidgetsFooter(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(FOOTER_HEIGHT)
        self.setMinimumWidth(FOOTER_MIN_WIDTH)
        # Thiết lập màu nền
        self.setStyleSheet(f"background: {FOOTER_BG};")

        # Tách riêng phần nội dung footer

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)
        # Label hiển thị thời gian
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"font-weight: {FONT_WEIGHT_BOLD};")
        layout.addWidget(self.time_label)
        layout.addStretch()
        # Label nội dung khác (bên phải)
        # Hiển thị nội dung bản quyền và version
        try:
            from core.resource import VERSION
        except ImportError:
            VERSION = "v1.0.0"
        self.info_label = QLabel(f"© 2025 Công ty của bạn | Phiên bản: {VERSION}")
        self.info_label.setStyleSheet(f"font-weight: {FONT_WEIGHT_BOLD};")
        layout.addWidget(self.info_label)

        # Timer cập nhật thời gian thực
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        """
        Mô tả:
            Cập nhật label thời gian thực, hiển thị thứ (tiếng Việt), ngày/tháng/năm giờ:phút:giây
        """
        thu_vn = [
            "Chủ nhật",
            "Thứ hai",
            "Thứ ba",
            "Thứ tư",
            "Thứ năm",
            "Thứ sáu",
            "Thứ bảy",
        ]
        now = QDateTime.currentDateTime()
        weekday = thu_vn[now.date().dayOfWeek() % 7]
        time_str = now.toString("dd/MM/yyyy HH:mm:ss")
        # Áp dụng in đậm cho toàn bộ chuỗi thời gian
        self.time_label.setText(
            f'<span style="font-weight:{FONT_WEIGHT_BOLD}">{weekday}, {time_str}</span>'
        )
