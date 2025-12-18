# widgets_declare_work_shift.py
# Widget khai báo ca làm việc

import logging

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QAbstractItemView,
    QFrame,
    QPushButton,
    QLineEdit,
    QGridLayout,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from core.resource import (
    DECLARE_WORK_SHIFT_MIN_WIDTH,
    DECLARE_WORK_SHIFT_MIN_HEIGHT,
    DECLARE_WORK_SHIFT_HEADER_HEIGHT,
    DECLARE_WORK_SHIFT_BG_HEADER,
    DECLARE_WORK_SHIFT_BG_MAIN,
    DECLARE_WORK_SHIFT_SVG,
    FONT_WEIGHT_SEMIBOLD,
    DECLARE_WORK_SHIFT_MAIN_2_HEIGHT,
    DECLARE_WORK_SHIFT_ROW_HEIGHT,
    FONT_WEIGHT_BOLD,
    HOVER_ROW,
    ACTIVE,
    ODD_ROW_BG,
    EVEN_ROW_BG,
    DECLARE_WORK_SHIFT_LEFT_WIDTH,
    DECLARE_WORK_SHIFT_RIGHT_WIDTH,
    ADD_SVG,
    SAVE_SVG,
    DELETE_SVG,
)

# Cấu hình logging
logging.basicConfig(
    filename="log/debug.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
logging.info("WidgetsDeclareWorkShift: Initializing widget")


class WidgetsDeclareWorkShift(QWidget):
    """Widget khai báo ca làm việc"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(DECLARE_WORK_SHIFT_MIN_WIDTH)
        self.setMinimumHeight(DECLARE_WORK_SHIFT_MIN_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Phần 1: Ảnh + tiêu đề
        self.header = self._create_header()
        main_layout.addWidget(self.header, 0)

        # Phần 2: Main content (chia làm 2 phần: trái và phải)
        self.main = self._create_main()
        main_layout.addWidget(self.main, 1)

        # Khởi tạo controller
        from ui.controllers.controllers_widgets_declare_work_shift import (
            ControllerWidgetsDeclareWorkShift,
        )

        self.controller = ControllerWidgetsDeclareWorkShift(self)

    def _format_time_input(self, line_edit):
        """Auto format time input: 1111 -> 11:11"""
        text = line_edit.text().replace(":", "")  # Xóa dấu : cũ

        # Chỉ chấp nhận số
        if not text.isdigit():
            return

        # Giới hạn 4 số
        if len(text) > 4:
            text = text[:4]

        # Auto format khi có 4 số
        if len(text) == 4:
            formatted = f"{text[:2]}:{text[2:]}"
            line_edit.blockSignals(True)  # Tạm tắt signal để không loop
            line_edit.setText(formatted)
            line_edit.blockSignals(False)

    def _create_header(self):
        """Tạo header với icon và tiêu đề"""
        header = QFrame()
        header.setAttribute(Qt.WA_StyledBackground, True)
        header.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_HEADER};")
        header.setFixedHeight(DECLARE_WORK_SHIFT_HEADER_HEIGHT)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 0, 0, 0)
        header_layout.setSpacing(8)

        # Icon
        icon_label = QLabel()
        icon = QIcon(DECLARE_WORK_SHIFT_SVG)
        pixmap = icon.pixmap(20, 20)
        icon_label.setPixmap(pixmap)
        header_layout.addWidget(icon_label)

        # Tiêu đề
        title_label = QLabel("Khai báo ca làm việc")
        title_label.setStyleSheet(
            f"font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222;"
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        return header

    def _create_main(self):
        """Tạo phần main content"""
        main = QFrame()
        main.setAttribute(Qt.WA_StyledBackground, True)
        main.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Content (chia 2 phần trái phải)
        part2 = self._create_part2()
        main_layout.addWidget(part2)

        return main

    def _create_part2(self):
        """Tạo phần 2: chia làm 2 phần trái (W360) và phải (W1000)"""
        part2 = QWidget()
        part2.setMinimumHeight(DECLARE_WORK_SHIFT_MAIN_2_HEIGHT)

        part2_layout = QHBoxLayout(part2)
        part2_layout.setContentsMargins(0, 0, 0, 0)
        part2_layout.setSpacing(0)

        # Phần trái: W360 với bảng 3 cột
        left_panel = self._create_left_panel()
        part2_layout.addWidget(left_panel)

        # Phần phải: W1000 để trống
        right_panel = self._create_right_panel()
        part2_layout.addWidget(right_panel)

        return part2

    def _create_left_panel(self):
        """Tạo panel trái với bảng 3 cột: Mã ca, Giờ vào, Giờ ra"""
        left_panel = QFrame()
        left_panel.setFixedWidth(DECLARE_WORK_SHIFT_LEFT_WIDTH)
        left_panel.setAttribute(Qt.WA_StyledBackground, True)
        left_panel.setStyleSheet("border-right: 1px solid #e0e0e0;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 0, 0, 0)
        left_layout.setSpacing(0)

        # Tạo bảng với 3 cột, 0 hàng ban đầu
        self.table = QTableWidget(0, 3, left_panel)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)  # Theo quy tắc .copilot_instructions
        self.table.setMouseTracking(True)

        # Đặt tiêu đề cột
        self.table.setHorizontalHeaderLabels(["Mã ca", "Giờ vào", "Giờ ra"])
        self.table.horizontalHeader().setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; font-size: 15px;"
        )
        self.table.horizontalHeader().setFixedHeight(40)

        # Cài đặt kích thước cột
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)

        # Cài đặt chiều cao hàng
        self.table.verticalHeader().setDefaultSectionSize(DECLARE_WORK_SHIFT_ROW_HEIGHT)
        self.table.verticalHeader().setVisible(False)

        # Style cho bảng
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                font-size: 14px;
                gridline-color: #e0e0e0;
                background: {EVEN_ROW_BG};
                alternate-background-color: {ODD_ROW_BG};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:hover {{
                background: {HOVER_ROW};
            }}
            QTableWidget::item:selected {{
                background: {ACTIVE};
                color: black;
            }}
            """
        )
        self.table.setAlternatingRowColors(True)

        left_layout.addWidget(self.table)
        return left_panel

    def _create_right_panel(self):
        """Tạo panel phải W1000 với header và form input"""
        right_panel = QFrame()
        right_panel.setMinimumWidth(DECLARE_WORK_SHIFT_RIGHT_WIDTH)
        right_panel.setAttribute(Qt.WA_StyledBackground, True)
        right_panel.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Header: 4 nút chức năng
        right_header = self._create_right_header()
        right_layout.addWidget(right_header)

        # Main: Form input
        right_main = self._create_right_main()
        right_layout.addWidget(right_main)

        return right_panel

    def _create_right_header(self):
        """Tạo header phải với 4 nút chức năng"""
        header = QFrame()
        header.setAttribute(Qt.WA_StyledBackground, True)
        header.setStyleSheet(
            f"background: {DECLARE_WORK_SHIFT_BG_MAIN}; border-bottom: 1px solid #e0e0e0;"
        )
        header.setFixedHeight(40)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 0, 8, 0)
        header_layout.setSpacing(8)

        # Nút Thêm mới
        self.btn_add = QPushButton(QIcon(ADD_SVG), "Thêm mới")
        self.btn_add.setFixedSize(100, 36)
        self.btn_add.setIconSize(QSize(20, 20))
        self.btn_add.setStyleSheet("border: none; font-size: 14px;")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setFocusPolicy(Qt.NoFocus)

        # Nút Lưu
        self.btn_save = QPushButton(QIcon(SAVE_SVG), "Lưu")
        self.btn_save.setFixedSize(100, 36)
        self.btn_save.setIconSize(QSize(20, 20))
        self.btn_save.setStyleSheet("border: none; font-size: 14px;")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setFocusPolicy(Qt.NoFocus)

        # Nút Xóa
        self.btn_delete = QPushButton(QIcon(DELETE_SVG), "Xóa")
        self.btn_delete.setFixedSize(100, 36)
        self.btn_delete.setIconSize(QSize(20, 20))
        self.btn_delete.setStyleSheet("border: none; font-size: 14px;")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setFocusPolicy(Qt.NoFocus)

        header_layout.addWidget(self.btn_add)
        header_layout.addWidget(self.btn_save)
        header_layout.addWidget(self.btn_delete)
        header_layout.addStretch(1)

        return header

    def _create_right_main(self):
        """Tạo form input cho thông tin ca làm việc"""
        main = QFrame()
        main.setAttribute(Qt.WA_StyledBackground, True)
        main.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(0)

        # Form grid
        form_layout = QGridLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setHorizontalSpacing(16)
        form_layout.setVerticalSpacing(12)

        # Style cho label
        label_style = "font-size: 14px; color: #333; font-weight: 500;"

        # Style cho input
        input_style = """
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #2C3E50;
            }
        """

        # Style cho time edit
        time_style = """
            QTimeEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                background: white;
            }
            QTimeEdit:focus {
                border: 1px solid #2C3E50;
            }
        """

        # Row 0: Mã ca làm việc
        lbl_shift_code = QLabel("Mã ca làm việc:")
        lbl_shift_code.setStyleSheet(label_style)
        self.input_shift_code = QLineEdit()
        self.input_shift_code.setFixedHeight(30)
        self.input_shift_code.setPlaceholderText("Nhập mã ca (VD: CA1, CA2...)")
        self.input_shift_code.setReadOnly(False)  # Đảm bảo không readonly
        self.input_shift_code.setEnabled(True)  # Đảm bảo enabled
        self.input_shift_code.setFocusPolicy(Qt.StrongFocus)  # Cho phép focus
        self.input_shift_code.setStyleSheet(input_style)
        form_layout.addWidget(lbl_shift_code, 0, 0)
        form_layout.addWidget(self.input_shift_code, 0, 1)

        # Row 1: Giờ vào làm việc
        lbl_start_time = QLabel("Giờ vào làm việc:")
        lbl_start_time.setStyleSheet(label_style)
        self.input_start_time = QLineEdit()
        self.input_start_time.setFixedHeight(30)
        self.input_start_time.setPlaceholderText("HH:mm hoặc HHmm (VD: 0800)")
        self.input_start_time.setText("08:00")
        self.input_start_time.setMaxLength(5)  # Giới hạn 5 ký tự (HH:mm)
        self.input_start_time.setStyleSheet(input_style)
        self.input_start_time.textChanged.connect(
            lambda: self._format_time_input(self.input_start_time)
        )
        form_layout.addWidget(lbl_start_time, 1, 0)
        form_layout.addWidget(self.input_start_time, 1, 1)

        # Row 2: Giờ kết thúc làm việc
        lbl_end_time = QLabel("Giờ kết thúc làm việc:")
        lbl_end_time.setStyleSheet(label_style)
        self.input_end_time = QLineEdit()
        self.input_end_time.setFixedHeight(30)
        self.input_end_time.setPlaceholderText("HH:mm hoặc HHmm (VD: 1730)")
        self.input_end_time.setText("17:00")
        self.input_end_time.setMaxLength(5)
        self.input_end_time.setStyleSheet(input_style)
        self.input_end_time.textChanged.connect(
            lambda: self._format_time_input(self.input_end_time)
        )
        form_layout.addWidget(lbl_end_time, 2, 0)
        form_layout.addWidget(self.input_end_time, 2, 1)

        # Row 3: Giờ bắt đầu ăn trưa
        lbl_lunch_start = QLabel("Giờ bắt đầu ăn trưa:")
        lbl_lunch_start.setStyleSheet(label_style)
        self.input_lunch_start = QLineEdit()
        self.input_lunch_start.setFixedHeight(30)
        self.input_lunch_start.setPlaceholderText("HH:mm hoặc HHmm (VD: 1200)")
        self.input_lunch_start.setText("12:00")
        self.input_lunch_start.setMaxLength(5)
        self.input_lunch_start.setStyleSheet(input_style)
        self.input_lunch_start.textChanged.connect(
            lambda: self._format_time_input(self.input_lunch_start)
        )
        form_layout.addWidget(lbl_lunch_start, 3, 0)
        form_layout.addWidget(self.input_lunch_start, 3, 1)

        # Row 4: Giờ kết thúc ăn trưa
        lbl_lunch_end = QLabel("Giờ kết thúc ăn trưa:")
        lbl_lunch_end.setStyleSheet(label_style)
        self.input_lunch_end = QLineEdit()
        self.input_lunch_end.setFixedHeight(30)
        self.input_lunch_end.setPlaceholderText("HH:mm hoặc HHmm (VD: 1300)")
        self.input_lunch_end.setText("13:00")
        self.input_lunch_end.setMaxLength(5)
        self.input_lunch_end.setStyleSheet(input_style)
        self.input_lunch_end.textChanged.connect(
            lambda: self._format_time_input(self.input_lunch_end)
        )
        form_layout.addWidget(lbl_lunch_end, 4, 0)
        form_layout.addWidget(self.input_lunch_end, 4, 1)

        # Row 5: Tổng giờ (phút)
        lbl_total_minutes = QLabel("Tổng giờ (phút):")
        lbl_total_minutes.setStyleSheet(label_style)
        self.input_total_minutes = QLineEdit()
        self.input_total_minutes.setFixedHeight(30)
        self.input_total_minutes.setPlaceholderText("Nhập số phút")
        self.input_total_minutes.setStyleSheet(input_style)
        form_layout.addWidget(lbl_total_minutes, 5, 0)
        form_layout.addWidget(self.input_total_minutes, 5, 1)

        # Row 6: Đếm công (công)
        lbl_work_day_count = QLabel("Đếm công (công):")
        lbl_work_day_count.setStyleSheet(label_style)
        self.input_work_day_count = QLineEdit()
        self.input_work_day_count.setFixedHeight(30)
        self.input_work_day_count.setPlaceholderText("Nhập số công")
        self.input_work_day_count.setStyleSheet(input_style)
        form_layout.addWidget(lbl_work_day_count, 6, 0)
        form_layout.addWidget(self.input_work_day_count, 6, 1)

        # Set column stretch để label và input cân đối
        form_layout.setColumnStretch(0, 0)  # Label không stretch
        form_layout.setColumnStretch(1, 1)  # Input stretch để fill space

        main_layout.addLayout(form_layout)
        main_layout.addStretch(1)

        return main
