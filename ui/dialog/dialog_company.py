import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        # Nếu ghi log lỗi, in ra stderr
        print(f"[LogError] {e}")


# Dialog thông tin công ty
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QPixmap, QIntValidator, QIcon

from core.resource import (
    DIALOG_COMPANY_WIDTH,
    DIALOG_COMPANY_HEIGHT,
    GROUP_COMPANY_HEIGHT,
    FONT_WEIGHT_BOLD,
    GROUP_4_COMPANY_HEIGHT,
    APP_ICO_PATH,
    BUTTON_BG,
    BG_DIALOG,
)


# Kích thước mặc định cho dialog công ty
class DialogCompany(QDialog):
    """
    Mô tả:
            Dialog hiển thị/thay đổi thông tin công ty
    Args:
            parent: QWidget cha (nếu có)
    Returns:
            None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin công ty")
        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(DIALOG_COMPANY_WIDTH, DIALOG_COMPANY_HEIGHT)
        self.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        main_layout = QVBoxLayout(self)
        from PySide6.QtCore import Qt

        main_layout.setAlignment(Qt.AlignTop)
        # Group 1: Thông tin công ty
        group_company = QGroupBox("Thông tin công ty")
        group_company.setFixedHeight(GROUP_COMPANY_HEIGHT)
        form_company = QFormLayout()
        self.edit_company_name = QLineEdit()
        self.edit_company_name.setMaxLength(50)
        self.edit_company_name.setPlaceholderText("Nhập tên công ty...")
        self.edit_company_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_company.addRow(self.edit_company_name)
        group_company.setLayout(form_company)
        main_layout.addWidget(group_company)

        # Group 2: Số điện thoại
        group_phone = QGroupBox("Số điện thoại")
        group_phone.setFixedHeight(GROUP_COMPANY_HEIGHT)
        form_phone = QFormLayout()
        self.edit_phone = QLineEdit()
        self.edit_phone.setMaxLength(15)
        self.edit_phone.setPlaceholderText("Nhập số điện thoại...")
        self.edit_phone.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        self.edit_phone.setValidator(QIntValidator(0, 999999999))
        form_phone.addRow(self.edit_phone)
        group_phone.setLayout(form_phone)
        main_layout.addWidget(group_phone)

        # Group 3: Địa chỉ
        group_address = QGroupBox("Địa chỉ")
        group_address.setFixedHeight(GROUP_COMPANY_HEIGHT)
        form_address = QFormLayout()
        self.edit_address = QLineEdit()
        self.edit_address.setMaxLength(50)
        self.edit_address.setPlaceholderText("Nhập địa chỉ...")
        self.edit_address.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_address.addRow(self.edit_address)
        group_address.setLayout(form_address)
        main_layout.addWidget(group_address)

        # Group 4: Ảnh logo và nút thao tác
        group_logo = QGroupBox("Logo công ty")
        group_logo.setFixedHeight(GROUP_4_COMPANY_HEIGHT)
        hbox_logo = QHBoxLayout()
        # Logo bên trái
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setStyleSheet("border: 1px solid #ccc; background: #fafafa;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(APP_ICO_PATH)
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.logo_label.setText("No Logo")
        hbox_logo.addWidget(self.logo_label)
        # Bên phải: 2 nút
        vbox_btn = QVBoxLayout()
        self.btn_change_logo = QPushButton("Thay đổi ảnh")
        self.btn_change_logo.setStyleSheet(
            f"background-color: {BUTTON_BG}; color: white; font-weight: bold; padding: 10px 10px; border-radius: 6px;"
        )
        self.btn_change_logo.setCursor(Qt.PointingHandCursor)
        self.btn_change_logo.setFixedWidth(300)
        self.btn_save_close = QPushButton("Lưu và Thoát")
        self.btn_save_close.setStyleSheet(
            f"background-color: {BUTTON_BG}; color: white; font-weight: bold; padding: 10px 10px; border-radius: 6px;"
        )
        self.btn_save_close.setCursor(Qt.PointingHandCursor)
        self.btn_save_close.setFixedWidth(300)
        vbox_btn.addWidget(self.btn_change_logo)
        vbox_btn.addWidget(self.btn_save_close)
        hbox_logo.addLayout(vbox_btn)
        group_logo.setLayout(hbox_logo)
        main_layout.addWidget(group_logo)

        # Ghi log thao tác thay đổi nội dung input
        self.edit_company_name.textChanged.connect(self._capitalize_company_name)
        self.edit_phone.textChanged.connect(
            lambda text: log_to_debug(f"DialogCompany: Thay đổi số điện thoại: {text}")
        )
        self.edit_address.textChanged.connect(self._capitalize_address)

        # Ghi log thao tác nút
        self.btn_change_logo.clicked.connect(
            lambda: log_to_debug("DialogCompany: Click Thay đổi ảnh")
        )
        self.btn_save_close.clicked.connect(
            lambda: log_to_debug("DialogCompany: Click Lưu và Thoát")
        )

        # Khởi tạo controller xử lý logic cho dialog (sau khi đã có self)
        try:
            from ui.controllers.controllers_company import CompanyController

            self.company_controller = CompanyController(self)
            # Kết nối signal cập nhật icon realtime trong dialog
            self.company_controller.icon_changed.connect(self._on_icon_changed)
            # Nếu parent là MainWindow, kết nối signal ra main window
            parent = self.parent()
            try:
                from ui.main_window import MainWindow

                if parent and isinstance(parent, MainWindow):
                    parent.connect_company_icon_signal(self.company_controller)
            except Exception as e:
                print(
                    f"[DialogCompany] Không thể kết nối signal icon_changed ra MainWindow: {e}"
                )
        except Exception as e:
            print(f"[DialogCompany] Không thể khởi tạo CompanyController: {e}")

    def _on_icon_changed(self, icon_path):
        """Cập nhật lại logo_label khi icon thay đổi realtime"""
        from PySide6.QtCore import Qt

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.logo_label.setText("No Logo")

    def _capitalize_company_name(self, text):
        capitalized = self._capitalize_words(text)
        if text != capitalized:
            cursor_pos = self.edit_company_name.cursorPosition()
            self.edit_company_name.blockSignals(True)
            self.edit_company_name.setText(capitalized)
            self.edit_company_name.setCursorPosition(cursor_pos)
            self.edit_company_name.blockSignals(False)
        log_to_debug(f"DialogCompany: Thay đổi tên công ty: {capitalized}")

    def _capitalize_address(self, text):
        # Nếu toàn bộ text là chữ hoa (có thể do Caps Lock), giữ nguyên
        if text.isupper() and any(c.isalpha() for c in text):
            log_to_debug(f"DialogCompany: Thay đổi địa chỉ (Caps Lock): {text}")
            return
        capitalized = self._capitalize_words(text)
        if text != capitalized:
            cursor_pos = self.edit_address.cursorPosition()
            self.edit_address.blockSignals(True)
            self.edit_address.setText(capitalized)
            self.edit_address.setCursorPosition(cursor_pos)
            self.edit_address.blockSignals(False)
        log_to_debug(f"DialogCompany: Thay đổi địa chỉ: {capitalized}")

    def _capitalize_words(self, text):
        return " ".join(word.capitalize() for word in text.split(" "))

    def showEvent(self, event):
        try:
            log_to_debug("DialogCompany: showEvent (Dialog mở)")
            # Load dữ liệu công ty từ DB khi mở dialog
            try:
                from services.company_services import CompanyService

                service = CompanyService()
                info = service.get_company_info()
                self.edit_company_name.setText(info.get("name", ""))
                self.edit_phone.setText(info.get("phone", ""))
                self.edit_address.setText(info.get("address", ""))
                logo_path = info.get("logo_path", "")
                from PySide6.QtCore import Qt

                pixmap = QPixmap(logo_path) if logo_path else QPixmap(APP_ICO_PATH)
                if not pixmap.isNull():
                    self.logo_label.setPixmap(
                        pixmap.scaled(
                            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                    )
                else:
                    self.logo_label.setText("No Logo")
            except Exception as e:
                log_to_debug(
                    f"DialogCompany: Lỗi load dữ liệu công ty: {e}\n{traceback.format_exc()}"
                )
            super().showEvent(event)
        except Exception as e:
            log_to_debug(f"DialogCompany: Lỗi showEvent: {e}\n{traceback.format_exc()}")

    def update_window_icon(self, icon_path):
        """Cập nhật icon cửa sổ realtime"""
        try:
            self.setWindowIcon(QIcon(icon_path))
            log_to_debug(f"DialogCompany: Cập nhật icon thành công: {icon_path}")
        except Exception as e:
            log_to_debug(f"DialogCompany: Lỗi cập nhật icon: {e}")

    def closeEvent(self, event):
        try:
            log_to_debug("DialogCompany: closeEvent (Dialog đóng)")
            super().closeEvent(event)
        except Exception as e:
            log_to_debug(
                f"DialogCompany: Lỗi closeEvent: {e}\n{traceback.format_exc()}"
            )
