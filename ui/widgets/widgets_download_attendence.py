# widgets_download_attendence.py
# Widget tải dữ liệu chấm công từ máy chấm công

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
    QDateEdit,
    QComboBox,
    QCalendarWidget,
    QLineEdit,
)
from PySide6.QtCore import Qt, QSize, QDate, QLocale
from PySide6.QtGui import QIcon

from core.resource import (
    DECLARE_WORK_SHIFT_MIN_WIDTH,
    DECLARE_WORK_SHIFT_MIN_HEIGHT,
    DECLARE_WORK_SHIFT_HEADER_HEIGHT,
    DECLARE_WORK_SHIFT_BG_HEADER,
    DECLARE_WORK_SHIFT_BG_MAIN,
    DECLARE_WORK_SHIFT_SVG,
    FONT_WEIGHT_SEMIBOLD,
    FONT_WEIGHT_BOLD,
    HOVER_ROW,
    ACTIVE,
    ODD_ROW_BG,
    EVEN_ROW_BG,
)

# Cấu hình logging
logging.basicConfig(
    filename="log/debug.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
logging.info("WidgetsDownloadAttendence: Initializing widget")


class WidgetsDownloadAttendence(QWidget):
    """Widget tải dữ liệu chấm công từ máy chấm công"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(DECLARE_WORK_SHIFT_MIN_WIDTH)
        self.setMinimumHeight(DECLARE_WORK_SHIFT_MIN_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header = self._create_header()
        main_layout.addWidget(self.header, 0)

        # Main content
        self.main = self._create_main()
        main_layout.addWidget(self.main, 1)

        # Khởi tạo controller
        from ui.controllers.controllers_widgets_download_attendence import (
            ControllerWidgetsDownloadAttendence,
        )
        self.controller = ControllerWidgetsDownloadAttendence(self)

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
        title_label = QLabel("Tải dữ liệu chấm công từ máy")
        title_label.setStyleSheet(
            f"font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222;"
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        return header

    def _create_main(self):
        """Tạo phần main content - Layout 2 panel giống widgets_declare_work_shift"""
        main = QFrame()
        main.setAttribute(Qt.WA_StyledBackground, True)
        main.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        main_layout = QHBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel trái: Bảng dữ liệu
        left_panel = self._create_left_panel()
        main_layout.addWidget(left_panel, 1)

        # Panel phải: Filter + chức năng
        right_panel = self._create_right_panel()
        main_layout.addWidget(right_panel, 0)

        return main
    
    def _create_left_panel(self):
        """Tạo panel trái chứa bảng dữ liệu"""
        left_panel = QFrame()
        left_panel.setAttribute(Qt.WA_StyledBackground, True)
        left_panel.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(16, 16, 8, 16)
        left_layout.setSpacing(12)
        
        # Search box
        search_panel = self._create_search_panel()
        left_layout.addWidget(search_panel)

        # Bảng dữ liệu
        table_panel = self._create_table_panel()
        left_layout.addWidget(table_panel, 1)

        return left_panel
    
    def _create_right_panel(self):
        """Tạo panel phải chứa filter và chức năng"""
        right_panel = QFrame()
        right_panel.setFixedWidth(400)
        right_panel.setAttribute(Qt.WA_StyledBackground, True)
        right_panel.setStyleSheet(f"background: {DECLARE_WORK_SHIFT_BG_MAIN};")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 16, 16, 16)
        right_layout.setSpacing(12)

        # Filter panel
        filter_panel = self._create_filter_panel()
        right_layout.addWidget(filter_panel)
        
        right_layout.addStretch(1)

        return right_panel

    def _create_filter_panel(self):
        """Tạo panel lọc dữ liệu - style giống declare_work_shift"""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            """
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Label style
        label_style = "font-size: 14px; color: #333; font-weight: 600;"

        # Tiêu đề panel
        title_label = QLabel("Bộ lọc dữ liệu")
        title_label.setStyleSheet(f"font-size: 16px; font-weight: {FONT_WEIGHT_BOLD}; color: #2C3E50;")
        layout.addWidget(title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: #e0e0e0;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Chọn thiết bị
        lbl_device = QLabel("Thiết bị:")
        lbl_device.setStyleSheet(label_style)
        layout.addWidget(lbl_device)

        self.combo_device = QComboBox()
        self.combo_device.setFixedHeight(36)
        self.combo_device.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 14px;
                background: white;
            }
            QComboBox:focus {
                border: 2px solid #2C3E50;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            """
        )
        layout.addWidget(self.combo_device)

        layout.addSpacing(12)

        # Từ ngày
        lbl_from_date = QLabel("Từ ngày:")
        lbl_from_date.setStyleSheet(label_style)
        layout.addWidget(lbl_from_date)

        self.date_from = QDateEdit()
        self.date_from.setFixedHeight(36)
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd-MM-yyyy")
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        
        # Tạo custom calendar widget tiếng Việt
        calendar_from = QCalendarWidget()
        calendar_from.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_from.setFirstDayOfWeek(Qt.Monday)
        self.date_from.setCalendarWidget(calendar_from)
        
        self.date_from.setStyleSheet(
            """
            QDateEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                font-weight: 600;
                color: #000000;
                background: white;
            }
            QDateEdit:focus {
                border: 2px solid #2C3E50;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #d0d0d0;
            }
            """
        )
        layout.addWidget(self.date_from)

        # Đến ngày
        lbl_to_date = QLabel("Đến ngày:")
        lbl_to_date.setStyleSheet(label_style)
        layout.addWidget(lbl_to_date)

        self.date_to = QDateEdit()
        self.date_to.setFixedHeight(36)
        self.date_to.setFixedHeight(45)
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd-MM-yyyy")
        self.date_to.setDate(QDate.currentDate())
        
        # Tạo custom calendar widget tiếng Việt
        calendar_to = QCalendarWidget()
        calendar_to.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_to.setFirstDayOfWeek(Qt.Monday)
        self.date_to.setCalendarWidget(calendar_to)
        
        self.date_to.setStyleSheet(
            """
            QDateEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                font-weight: 600;
                color: #000000;
                background: white;
            }
            QDateEdit:focus {
                border: 2px solid #2C3E50;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #d0d0d0;
            }
            """
        )
        layout.addWidget(self.date_to)

        layout.addSpacing(12)

        # Nút tải dữ liệu
        self.btn_download = QPushButton("📥 Tải dữ liệu")
        self.btn_download.setFixedHeight(36)
        self.btn_download.setMinimumWidth(130)
        self.btn_download.setStyleSheet(
            """
            QPushButton {
                background: #2C3E50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 16px;
            }
            QPushButton:hover {
                background: #1a252f;
            }
            QPushButton:pressed {
                background: #0d1418;
            }
            """
        )
        self.btn_download.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_download)

        # Nút xóa dữ liệu
        self.btn_clear = QPushButton("🗑️ Xóa dữ liệu")
        self.btn_clear.setFixedHeight(36)
        self.btn_clear.setMinimumWidth(130)
        self.btn_clear.setStyleSheet(
            """
            QPushButton {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 16px;
            }
            QPushButton:hover {
                background: #c82333;
            }
            QPushButton:pressed {
                background: #bd2130;
            }
            """
        )
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_clear)

        layout.addStretch()

        return panel

    def _create_search_panel(self):
        """Tạo panel tìm kiếm"""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
            }
            """
        )

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Icon tìm kiếm
        lbl_search = QLabel("🔍 Tìm kiếm:")
        lbl_search.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        layout.addWidget(lbl_search)

        # Ô tìm kiếm
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập mã NV, tên nhân viên để tìm kiếm...")
        self.txt_search.setFixedHeight(32)
        self.txt_search.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #2C3E50;
            }
            """
        )
        layout.addWidget(self.txt_search)

        return panel

    def _create_table_panel(self):
        """Tạo panel bảng dữ liệu chấm công"""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            """
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Tạo bảng với các cột
        self.table = QTableWidget(0, 11)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Cho phép chọn nhiều rows
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setMouseTracking(True)
        
        # Bật sắp xếp
        self.table.setSortingEnabled(True)

        # Đặt tiêu đề cột
        self.table.setHorizontalHeaderLabels([
            "Mã NV",
            "Tên NV", 
            "Ngày",
            "Giờ vào 1",
            "Giờ ra 1",
            "Giờ vào 2",
            "Giờ ra 2",
            "Giờ vào 3",
            "Giờ ra 3",
            "Vân tay",
            "Mã chấm công"
        ])
        
        self.table.horizontalHeader().setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; font-size: 14px; background: #f8f9fa; padding: 8px;"
        )
        self.table.horizontalHeader().setFixedHeight(40)

        # Cài đặt kích thước cột cố định để căn chỉnh đẹp
        self.table.setColumnWidth(0, 100)   # Mã NV
        self.table.setColumnWidth(1, 200)   # Tên NV
        self.table.setColumnWidth(2, 100)   # Ngày
        self.table.setColumnWidth(3, 90)    # Giờ vào 1
        self.table.setColumnWidth(4, 90)    # Giờ ra 1
        self.table.setColumnWidth(5, 90)    # Giờ vào 2
        self.table.setColumnWidth(6, 90)    # Giờ ra 2
        self.table.setColumnWidth(7, 90)    # Giờ vào 3
        self.table.setColumnWidth(8, 90)    # Giờ ra 3
        self.table.setColumnWidth(9, 100)   # Vân tay
        self.table.setColumnWidth(10, 120)  # Mã chấm công
        
        # Cho phép resize thủ công
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # Cột Tên NV có thể stretch
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)

        # Style cho bảng
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                font-size: 13px;
                gridline-color: #e0e0e0;
                background: {EVEN_ROW_BG};
                alternate-background-color: {ODD_ROW_BG};
                border: none;
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
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

        layout.addWidget(self.table)
        return panel


