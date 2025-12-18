# widgets_device.py
# Widget quản lý thiết bị chấm công

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
logging.info("WidgetsDevice: Initializing widget")


class WidgetsDevice(QWidget):
    """Widget quản lý thiết bị chấm công"""

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
        from ui.controllers.controllers_widgets_device import ControllerWidgetsDevice
        self.controller = ControllerWidgetsDevice(self)

    def _on_ip_field_changed(self, current_field, next_field):
        """Xử lý khi nhập vào trường IP - tự động chuyển sang trường tiếp theo"""
        text = current_field.text()
        
        # Chỉ cho phép nhập số
        if text and not text.isdigit():
            # Loại bỏ ký tự không phải số
            cleaned = ''.join(c for c in text if c.isdigit())
            current_field.blockSignals(True)
            current_field.setText(cleaned)
            current_field.blockSignals(False)
            return
        
        # Kiểm tra nếu nhập dấu chấm hoặc đủ 3 số -> chuyển sang trường tiếp theo
        if len(text) == 3:
            # Kiểm tra giá trị không vượt quá 255
            if int(text) > 255:
                current_field.blockSignals(True)
                current_field.setText("255")
                current_field.blockSignals(False)
            # Tự động focus sang trường tiếp theo
            if next_field:
                next_field.setFocus()
                next_field.selectAll()
    
    def get_ip_address(self):
        """Lấy địa chỉ IP từ 4 trường và ghép lại"""
        ip1 = self.ip_field1.text().strip()
        ip2 = self.ip_field2.text().strip()
        ip3 = self.ip_field3.text().strip()
        ip4 = self.ip_field4.text().strip()
        
        # Chỉ trả về nếu ít nhất có 1 trường được nhập
        if not any([ip1, ip2, ip3, ip4]):
            return ""
        
        # Ghép lại, sử dụng 0 cho trường trống
        parts = [ip1 or "0", ip2 or "0", ip3 or "0", ip4 or "0"]
        return ".".join(parts)
    
    def set_ip_address(self, ip_address):
        """Đặt địa chỉ IP vào 4 trường"""
        if not ip_address:
            self.ip_field1.clear()
            self.ip_field2.clear()
            self.ip_field3.clear()
            self.ip_field4.clear()
            return
        
        parts = ip_address.split(".")
        if len(parts) >= 1:
            self.ip_field1.setText(parts[0])
        if len(parts) >= 2:
            self.ip_field2.setText(parts[1])
        if len(parts) >= 3:
            self.ip_field3.setText(parts[2])
        if len(parts) >= 4:
            self.ip_field4.setText(parts[3])

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
        title_label = QLabel("Quản lý thiết bị chấm công")
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

        # Phần phải: W1000 với form input
        right_panel = self._create_right_panel()
        part2_layout.addWidget(right_panel)

        return part2

    def _create_left_panel(self):
        """Tạo panel trái với bảng 3 cột: Số máy, Tên máy, Địa chỉ IP"""
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
        self.table.setHorizontalHeaderLabels(["Số máy", "Tên máy", "Địa chỉ IP"])
        self.table.horizontalHeader().setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; font-size: 15px;"
        )
        self.table.horizontalHeader().setFixedHeight(40)

        # Cài đặt kích thước cột
        self.table.setColumnWidth(0, 80)   # Số máy
        self.table.setColumnWidth(1, 140)  # Tên máy
        self.table.setColumnWidth(2, 130)  # Địa chỉ IP
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

        # Nút Kết nối
        self.btn_connect = QPushButton("🔗 Kết nối")
        self.btn_connect.setFixedSize(110, 36)
        self.btn_connect.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #2C3E50;
                border-radius: 4px;
                font-size: 14px;
                background: white;
                color: #2C3E50;
            }
            QPushButton:hover {
                background: #2C3E50;
                color: white;
            }
            """
        )
        self.btn_connect.setCursor(Qt.PointingHandCursor)
        self.btn_connect.setFocusPolicy(Qt.NoFocus)

        header_layout.addWidget(self.btn_add)
        header_layout.addWidget(self.btn_save)
        header_layout.addWidget(self.btn_delete)
        header_layout.addSpacing(16)
        header_layout.addWidget(self.btn_connect)
        header_layout.addStretch(1)

        return header

    def _create_right_main(self):
        """Tạo form input cho thông tin thiết bị chấm công"""
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

        # Row 0: Số máy
        lbl_device_number = QLabel("Số máy:")
        lbl_device_number.setStyleSheet(label_style)
        self.input_device_number = QLineEdit()
        self.input_device_number.setFixedHeight(30)
        self.input_device_number.setPlaceholderText("Nhập số máy (VD: 1, 2, 3...)")
        self.input_device_number.setReadOnly(False)
        self.input_device_number.setEnabled(True)
        self.input_device_number.setFocusPolicy(Qt.StrongFocus)
        self.input_device_number.setStyleSheet(input_style)
        form_layout.addWidget(lbl_device_number, 0, 0)
        form_layout.addWidget(self.input_device_number, 0, 1)

        # Row 1: Tên máy
        lbl_device_name = QLabel("Tên máy:")
        lbl_device_name.setStyleSheet(label_style)
        self.input_device_name = QLineEdit()
        self.input_device_name.setFixedHeight(30)
        self.input_device_name.setPlaceholderText("Nhập tên máy (VD: Máy chấm công 1)")
        self.input_device_name.setStyleSheet(input_style)
        form_layout.addWidget(lbl_device_name, 1, 0)
        form_layout.addWidget(self.input_device_name, 1, 1)

        # Row 2: Địa chỉ IP (4 trường riêng biệt)
        lbl_ip_address = QLabel("Địa chỉ IP:")
        lbl_ip_address.setStyleSheet(label_style)
        
        # Tạo container cho 4 trường IP
        ip_container = QWidget()
        ip_layout = QHBoxLayout(ip_container)
        ip_layout.setContentsMargins(0, 0, 0, 0)
        ip_layout.setSpacing(5)
        
        # Style cho các trường IP nhỏ
        ip_input_style = """
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                background: white;
                text-align: center;
            }
            QLineEdit:focus {
                border: 2px solid #2C3E50;
            }
        """
        
        # Tạo 4 trường IP
        self.ip_field1 = QLineEdit()
        self.ip_field1.setFixedSize(50, 30)
        self.ip_field1.setMaxLength(3)
        self.ip_field1.setPlaceholderText("192")
        self.ip_field1.setStyleSheet(ip_input_style)
        self.ip_field1.setAlignment(Qt.AlignCenter)
        
        self.ip_field2 = QLineEdit()
        self.ip_field2.setFixedSize(50, 30)
        self.ip_field2.setMaxLength(3)
        self.ip_field2.setPlaceholderText("168")
        self.ip_field2.setStyleSheet(ip_input_style)
        self.ip_field2.setAlignment(Qt.AlignCenter)
        
        self.ip_field3 = QLineEdit()
        self.ip_field3.setFixedSize(50, 30)
        self.ip_field3.setMaxLength(3)
        self.ip_field3.setPlaceholderText("1")
        self.ip_field3.setStyleSheet(ip_input_style)
        self.ip_field3.setAlignment(Qt.AlignCenter)
        
        self.ip_field4 = QLineEdit()
        self.ip_field4.setFixedSize(50, 30)
        self.ip_field4.setMaxLength(3)
        self.ip_field4.setPlaceholderText("10")
        self.ip_field4.setStyleSheet(ip_input_style)
        self.ip_field4.setAlignment(Qt.AlignCenter)
        
        # Kết nối các event
        self.ip_field1.textChanged.connect(lambda: self._on_ip_field_changed(self.ip_field1, self.ip_field2))
        self.ip_field2.textChanged.connect(lambda: self._on_ip_field_changed(self.ip_field2, self.ip_field3))
        self.ip_field3.textChanged.connect(lambda: self._on_ip_field_changed(self.ip_field3, self.ip_field4))
        
        # Thêm vào layout
        ip_layout.addWidget(self.ip_field1)
        ip_layout.addWidget(QLabel("."))
        ip_layout.addWidget(self.ip_field2)
        ip_layout.addWidget(QLabel("."))
        ip_layout.addWidget(self.ip_field3)
        ip_layout.addWidget(QLabel("."))
        ip_layout.addWidget(self.ip_field4)
        ip_layout.addStretch()
        
        form_layout.addWidget(lbl_ip_address, 2, 0)
        form_layout.addWidget(ip_container, 2, 1)

        # Row 3: Mật mã
        lbl_password = QLabel("Mật mã:")
        lbl_password.setStyleSheet(label_style)
        self.input_password = QLineEdit()
        self.input_password.setFixedHeight(30)
        self.input_password.setPlaceholderText("Nhập mật mã thiết bị (nếu có)")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet(input_style)
        form_layout.addWidget(lbl_password, 3, 0)
        form_layout.addWidget(self.input_password, 3, 1)

        # Row 4: Cổng kết nối
        lbl_port = QLabel("Cổng kết nối:")
        lbl_port.setStyleSheet(label_style)
        self.input_port = QLineEdit()
        self.input_port.setFixedHeight(30)
        self.input_port.setPlaceholderText("Nhập số cổng (VD: 4370)")
        self.input_port.setText("4370")  # Giá trị mặc định
        self.input_port.setStyleSheet(input_style)
        form_layout.addWidget(lbl_port, 4, 0)
        form_layout.addWidget(self.input_port, 4, 1)

        # Row 5: Trạng thái (hiển thị thông tin)
        lbl_status = QLabel("Trạng thái:")
        lbl_status.setStyleSheet(label_style)
        self.lbl_status_value = QLabel("Chưa kết nối")
        self.lbl_status_value.setFixedHeight(30)
        self.lbl_status_value.setStyleSheet(
            """
            QLabel {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                background: #f5f5f5;
                color: #666;
            }
            """
        )
        form_layout.addWidget(lbl_status, 5, 0)
        form_layout.addWidget(self.lbl_status_value, 5, 1)

        # Row 6: Ghi chú
        lbl_note = QLabel("Ghi chú:")
        lbl_note.setStyleSheet(label_style)
        self.input_note = QLineEdit()
        self.input_note.setFixedHeight(30)
        self.input_note.setPlaceholderText("Nhập ghi chú (tùy chọn)")
        self.input_note.setStyleSheet(input_style)
        form_layout.addWidget(lbl_note, 6, 0)
        form_layout.addWidget(self.input_note, 6, 1)

        # Set column stretch để label và input cân đối
        form_layout.setColumnStretch(0, 0)  # Label không stretch
        form_layout.setColumnStretch(1, 1)  # Input stretch để fill space

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)

        # Thêm thông tin hướng dẫn
        info_frame = QFrame()
        info_frame.setStyleSheet(
            """
            QFrame {
                background: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 12px;
            }
            """
        )
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 8, 8, 8)
        info_layout.setSpacing(4)

        info_title = QLabel("💡 Hướng dẫn:")
        info_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #2C3E50;")
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "• Nhập đầy đủ thông tin thiết bị (Số máy, Tên máy, Địa chỉ IP)\n"
            "• Mật mã và Cổng kết nối dùng để kết nối với thiết bị\n"
            "• Nhấn nút 'Kết nối' để kiểm tra kết nối thiết bị\n"
            "• Nhấn 'Lưu' để lưu thông tin thiết bị vào hệ thống"
        )
        info_text.setStyleSheet("font-size: 12px; color: #555; line-height: 1.6;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        main_layout.addWidget(info_frame)
        main_layout.addStretch(1)

        return main
