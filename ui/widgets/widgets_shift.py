# widgets_shift.py
# Widget quản lý tải nhân viên lên máy chấm công

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QCheckBox,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


class WidgetsShift(QWidget):
    """Widget tải nhân viên lên máy chấm công"""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
        
        # Khởi tạo controller sau khi UI được tạo
        self.controller = None
        
        self._create_ui()

    def _create_ui(self):
        """Tạo giao diện chính"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === PHẦN 1: DANH SÁCH NHÂN VIÊN (Top 50%) ===
        top_section = self._create_employee_section()
        top_section.setMinimumHeight(350)  # Đảm bảo chiều cao tối thiểu
        main_layout.addWidget(top_section, 1)

        # === PHẦN 2: DANH SÁCH ĐÃ TẢI LÊN MÁY (Bottom 50%) ===
        bottom_section = self._create_uploaded_section()
        bottom_section.setMinimumHeight(350)  # Đảm bảo chiều cao tối thiểu
        main_layout.addWidget(bottom_section, 1)

    def _create_employee_section(self):
        """Tạo phần danh sách nhân viên"""
        section = QFrame()
        section.setAttribute(Qt.WA_StyledBackground, True)
        section.setStyleSheet("background: #f5f5f5;")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 16, 16, 8)
        layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title_label = QLabel("Danh sách nhân viên")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Upload button
        self.btn_upload_file = QPushButton("📤 Upload danh sách")
        self.btn_upload_file.setFixedHeight(32)
        self.btn_upload_file.setStyleSheet("""
            QPushButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0056b3;
            }
        """)
        self.btn_upload_file.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.btn_upload_file)

        # Search box
        self.txt_search_employee = QLineEdit()
        self.txt_search_employee.setPlaceholderText("Tìm nhân viên")
        self.txt_search_employee.setFixedHeight(32)
        self.txt_search_employee.setFixedWidth(250)
        self.txt_search_employee.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #2C3E50;
            }
        """)
        header_layout.addWidget(self.txt_search_employee)

        # Icon button (placeholder for search icon)
        btn_search_icon = QPushButton("🔍")
        btn_search_icon.setFixedSize(32, 32)
        btn_search_icon.setStyleSheet("""
            QPushButton {
                background: #2C3E50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1a252f;
            }
        """)
        header_layout.addWidget(btn_search_icon)

        layout.addLayout(header_layout)

        # Stats bar
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        self.lbl_total_employees = QLabel("Tổng số: 0")
        self.lbl_total_employees.setStyleSheet("font-size: 13px; color: #555;")
        stats_layout.addWidget(self.lbl_total_employees)

        stats_layout.addStretch()

        # Download button (tải xuống từ máy)
        self.btn_download_from_device = QPushButton("↓ Chuyển xuống")
        self.btn_download_from_device.setFixedHeight(32)
        self.btn_download_from_device.setStyleSheet("""
            QPushButton {
                background: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #218838;
            }
        """)
        self.btn_download_from_device.setCursor(Qt.PointingHandCursor)
        stats_layout.addWidget(self.btn_download_from_device)

        # Refresh button
        self.btn_refresh_employees = QPushButton("↻ Làm tươi")
        self.btn_refresh_employees.setFixedHeight(32)
        self.btn_refresh_employees.setStyleSheet("""
            QPushButton {
                background: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #138496;
            }
        """)
        self.btn_refresh_employees.setCursor(Qt.PointingHandCursor)
        stats_layout.addWidget(self.btn_refresh_employees)

        layout.addLayout(stats_layout)

        # Table
        self.table_employees = QTableWidget()
        self.table_employees.setColumnCount(9)
        self.table_employees.setHorizontalHeaderLabels([
            "", "Mã nhân viên", "Tên nhân viên", "Mã chấm công", 
            "Tên chấm công", "Mã số thẻ", "Mật mã", "Loại", "Cho phép"
        ])
        
        # Column 0: Checkbox
        self.table_employees.setColumnWidth(0, 40)
        
        # Set other column widths
        header = self.table_employees.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Mã NV
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Tên NV
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Mã CC
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Tên CC
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Mã số thẻ
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Mật mã
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Loại
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Cho phép
        
        self.table_employees.setAlternatingRowColors(True)
        self.table_employees.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_employees.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table_employees.verticalHeader().setVisible(False)
        
        self.table_employees.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background: #e3f2fd;
                color: #000;
            }
            QHeaderView::section {
                background: #2C3E50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        
        layout.addWidget(self.table_employees)

        return section

    def _create_uploaded_section(self):
        """Tạo phần danh sách nhân viên đã tải lên máy"""
        section = QFrame()
        section.setAttribute(Qt.WA_StyledBackground, True)
        section.setStyleSheet("background: #f9f9f9;")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 8, 16, 16)
        layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title_label = QLabel("Danh sách nhân viên được tải lên máy chấm công")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        header_layout.addWidget(title_label)

        layout.addLayout(header_layout)

        # Stats & Action bar
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)

        self.lbl_total_uploaded = QLabel("Tổng số: 0")
        self.lbl_total_uploaded.setStyleSheet("font-size: 13px; color: #555;")
        action_layout.addWidget(self.lbl_total_uploaded)

        action_layout.addStretch()

        # Remove button
        self.btn_remove = QPushButton("❌ Loại bỏ")
        self.btn_remove.setFixedHeight(32)
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #5a6268;
            }
        """)
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        action_layout.addWidget(self.btn_remove)

        # Select device & upload button
        self.btn_select_upload = QPushButton("📤 Chọn máy & Tải lên")
        self.btn_select_upload.setFixedHeight(32)
        self.btn_select_upload.setStyleSheet("""
            QPushButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0056b3;
            }
        """)
        self.btn_select_upload.setCursor(Qt.PointingHandCursor)
        action_layout.addWidget(self.btn_select_upload)

        # Select device & delete employee button
        self.btn_select_delete = QPushButton("❌ Chọn máy & Xóa nhân viên")
        self.btn_select_delete.setFixedHeight(32)
        self.btn_select_delete.setStyleSheet("""
            QPushButton {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #c82333;
            }
        """)
        self.btn_select_delete.setCursor(Qt.PointingHandCursor)
        action_layout.addWidget(self.btn_select_delete)

        # Select device & delete fingerprint button
        self.btn_select_delete_fp = QPushButton("❌ Chọn máy & Xóa vân tay")
        self.btn_select_delete_fp.setFixedHeight(32)
        self.btn_select_delete_fp.setStyleSheet("""
            QPushButton {
                background: #fd7e14;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e8590c;
            }
        """)
        self.btn_select_delete_fp.setCursor(Qt.PointingHandCursor)
        action_layout.addWidget(self.btn_select_delete_fp)

        layout.addLayout(action_layout)

        # Table
        self.table_uploaded = QTableWidget()
        self.table_uploaded.setColumnCount(7)
        self.table_uploaded.setHorizontalHeaderLabels([
            "Mã NV", "Mã CC", "Tên chấm công", "Mã số thẻ", "Mật mã", "Loại", "Cho phép"
        ])
        
        header = self.table_uploaded.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Mã NV
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Mã CC
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Tên CC
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Mã số thẻ
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Mật mã
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Loại
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Cho phép
        
        self.table_uploaded.setAlternatingRowColors(True)
        self.table_uploaded.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_uploaded.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table_uploaded.verticalHeader().setVisible(False)
        
        self.table_uploaded.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background: #fff3cd;
                color: #000;
            }
            QHeaderView::section {
                background: #495057;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        
        layout.addWidget(self.table_uploaded)

        return section

    def set_controller(self, controller):
        """Đặt controller cho widget"""
        self.controller = controller
