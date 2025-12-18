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


# Dialog chức danh
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
)
from PySide6.QtGui import QIcon

from core.resource import (
    FONT_WEIGHT_BOLD,
    BUTTON_BG,
    CANCEL_BUTTON_BG,
    DELETE_SVG,
    BG_DIALOG,
)


class DialogJobTitleBase(QDialog):
    """
    Mô tả:
            Dialog cơ bản cho chức danh
    Args:
            parent: QWidget cha (nếu có)
    Returns:
            None
    """

    def __init__(self, parent=None, title="Dialog Chức Danh", width=400, height=200):
        super().__init__(parent)
        self.setWindowTitle(title)
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(width, height)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        main_layout = QVBoxLayout(self)
        from PySide6.QtCore import Qt

        main_layout.setAlignment(Qt.AlignTop)

        # Group: Tên chức danh
        group_job_title = QGroupBox("Tên chức danh")
        group_job_title.setFixedHeight(80)
        form_job_title = QFormLayout()
        self.edit_job_title_name = QLineEdit()
        self.edit_job_title_name.setMaxLength(50)
        self.edit_job_title_name.setPlaceholderText("Nhập tên chức danh...")
        self.edit_job_title_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_job_title.addRow(self.edit_job_title_name)
        group_job_title.setLayout(form_job_title)

        main_layout.addWidget(group_job_title)
        # Tăng khoảng cách giữa input và button
        main_layout.addSpacing(16)

        # Nút lưu và hủy - nằm trên 1 dòng, mỗi nút 50% chiều rộng
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.setStyleSheet(
            f"background: {BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.btn_save, 1)  # 50% chiều rộng
        btn_layout.addWidget(self.btn_cancel, 1)  # 50% chiều rộng
        main_layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)


class DialogJobTitleAdd(DialogJobTitleBase):
    """
    Mô tả:
            Dialog thêm mới chức danh
    Args:
            parent: QWidget cha (nếu có)
    Returns:
            None
    """

    def __init__(self, parent=None):
        super().__init__(parent, title="Thêm Chức Danh Mới", width=400, height=200)
        log_to_debug("DialogJobTitleAdd: Khởi tạo")

        # Kết nối signal lưu
        self.btn_save.clicked.connect(self.save_job_title)
        self.edit_job_title_name.textChanged.connect(self._on_text_changed)

    def save_job_title(self):
        try:
            job_title_name = self.edit_job_title_name.text().strip()
            if not job_title_name:
                log_to_debug("DialogJobTitleAdd: Tên chức danh trống")
                return

            log_to_debug(f"DialogJobTitleAdd: Lưu chức danh mới: {job_title_name}")

            # Gọi service để lưu vào DB
            try:
                from services.job_title_services import JobTitleService

                service = JobTitleService()
                # Kiểm tra trùng tên
                existing_titles = service.get_all_job_titles()
                for title in existing_titles:
                    if title["name"].lower() == job_title_name.lower():
                        log_to_debug(
                            f"DialogJobTitleAdd: Chức danh '{job_title_name}' đã tồn tại"
                        )
                        return

                if service.add_job_title(job_title_name):
                    log_to_debug(
                        f"DialogJobTitleAdd: Chức danh '{job_title_name}' đã được lưu"
                    )
                else:
                    log_to_debug(
                        f"DialogJobTitleAdd: Lỗi lưu chức danh '{job_title_name}'"
                    )
            except Exception as e:
                log_to_debug(
                    f"DialogJobTitleAdd: Lỗi lưu chức danh: {e}\n{traceback.format_exc()}"
                )

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogJobTitleAdd: Lỗi save_job_title: {e}\n{traceback.format_exc()}"
            )

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu của mỗi từ (Xin Chào)"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu của mỗi từ
        words = text.split()
        capitalized = " ".join(word.capitalize() for word in words)
        if text != capitalized:
            cursor_pos = self.edit_job_title_name.cursorPosition()
            self.edit_job_title_name.blockSignals(True)
            self.edit_job_title_name.setText(capitalized)
            self.edit_job_title_name.setCursorPosition(cursor_pos)
            self.edit_job_title_name.blockSignals(False)


class DialogJobTitleEdit(QDialog):
    """
    Mô tả:
            Dialog sửa đổi chức danh
    Args:
            parent: QWidget cha (nếu có)
            job_title_id: ID của chức danh cần sửa
    Returns:
            None
    """

    def __init__(self, parent=None, job_title_id=None):
        super().__init__(parent)
        self.job_title_id = job_title_id
        self.setWindowTitle("Sửa Đổi Chức Danh")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(500, 200)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        log_to_debug(f"DialogJobTitleEdit: Khởi tạo (ID: {job_title_id})")

        from PySide6.QtCore import Qt

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Group: Tên chức danh
        group_job_title = QGroupBox("Tên chức danh")
        group_job_title.setFixedHeight(80)
        form_job_title = QFormLayout()
        self.edit_job_title_name = QLineEdit()
        self.edit_job_title_name.setMaxLength(50)
        self.edit_job_title_name.setPlaceholderText("Nhập tên chức danh...")
        self.edit_job_title_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_job_title.addRow(self.edit_job_title_name)
        group_job_title.setLayout(form_job_title)

        main_layout.addWidget(group_job_title)
        # Tăng khoảng cách giữa input và button
        main_layout.addSpacing(16)

        # Nút lưu và hủy
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.setStyleSheet(
            f"background: {BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.btn_save, 1)
        btn_layout.addWidget(self.btn_cancel, 1)
        main_layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)

        # Kết nối signal lưu
        self.btn_save.clicked.connect(self.save_job_title)
        self.edit_job_title_name.textChanged.connect(self._on_text_changed)

        # Load dữ liệu chức danh
        self.load_job_title_data()

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu của mỗi từ (Xin Chào)"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu của mỗi từ
        words = text.split()
        capitalized = " ".join(word.capitalize() for word in words)
        if text != capitalized:
            cursor_pos = self.edit_job_title_name.cursorPosition()
            self.edit_job_title_name.blockSignals(True)
            self.edit_job_title_name.setText(capitalized)
            self.edit_job_title_name.setCursorPosition(cursor_pos)
            self.edit_job_title_name.blockSignals(False)

    def load_job_title_data(self):
        try:
            if self.job_title_id:
                log_to_debug(
                    f"DialogJobTitleEdit: Load dữ liệu chức danh ID {self.job_title_id}"
                )
                # Gọi service để load dữ liệu từ DB
                try:
                    from services.job_title_services import JobTitleService

                    service = JobTitleService()
                    job_title_info = service.get_job_title_by_id(self.job_title_id)
                    if job_title_info:
                        self.edit_job_title_name.setText(job_title_info.get("name", ""))
                        log_to_debug(
                            f"DialogJobTitleEdit: Loaded job title: {job_title_info.get('name')}"
                        )
                except Exception as e:
                    log_to_debug(
                        f"DialogJobTitleEdit: Lỗi load dữ liệu: {e}\n{traceback.format_exc()}"
                    )
        except Exception as e:
            log_to_debug(
                f"DialogJobTitleEdit: Lỗi load_job_title_data: {e}\n{traceback.format_exc()}"
            )

    def save_job_title(self):
        try:
            job_title_name = self.edit_job_title_name.text().strip()
            if not job_title_name:
                log_to_debug("DialogJobTitleEdit: Tên chức danh trống")
                return

            log_to_debug(f"DialogJobTitleEdit: Lưu chức danh: {job_title_name}")

            # Gọi service để lưu vào DB
            try:
                from services.job_title_services import JobTitleService

                service = JobTitleService()
                if service.update_job_title(self.job_title_id, job_title_name):
                    log_to_debug(
                        f"DialogJobTitleEdit: Chức danh '{job_title_name}' đã được cập nhật"
                    )
                else:
                    log_to_debug(
                        f"DialogJobTitleEdit: Lỗi cập nhật chức danh '{job_title_name}'"
                    )
            except Exception as e:
                log_to_debug(
                    f"DialogJobTitleEdit: Lỗi lưu chức danh: {e}\n{traceback.format_exc()}"
                )

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogJobTitleEdit: Lỗi save_job_title: {e}\n{traceback.format_exc()}"
            )

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu tiên"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu tiên, giữ nguyên phần còn lại
        capitalized = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        if text != capitalized:
            cursor_pos = self.edit_job_title_name.cursorPosition()
            self.edit_job_title_name.blockSignals(True)
            self.edit_job_title_name.setText(capitalized)
            self.edit_job_title_name.setCursorPosition(cursor_pos)
            self.edit_job_title_name.blockSignals(False)


class DialogJobTitleDelete(QDialog):
    """
    Mô tả:
            Dialog xác nhận xóa chức danh
    Args:
            parent: QWidget cha (nếu có)
            job_title_name: Tên chức danh cần xóa
            job_title_id: ID của chức danh cần xóa
    Returns:
            None
    """

    def __init__(self, parent=None, job_title_name="", job_title_id=None):
        super().__init__(parent)
        self.job_title_name = job_title_name
        self.job_title_id = job_title_id

        self.setWindowTitle("Xác Nhận Xóa")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(450, 220)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        log_to_debug(
            f"DialogJobTitleDelete: Khởi tạo (ID: {job_title_id}, Tên: {job_title_name})"
        )

        main_layout = QVBoxLayout(self)
        from PySide6.QtCore import Qt

        main_layout.setAlignment(Qt.AlignTop)

        # Input hiển thị tên chức danh
        group_name = QGroupBox("Chức danh cần xóa")
        group_name.setFixedHeight(70)
        form_name = QFormLayout()
        self.edit_delete_name = QLineEdit()
        self.edit_delete_name.setText(job_title_name)
        self.edit_delete_name.setReadOnly(True)
        self.edit_delete_name.setStyleSheet(
            "background: #f5f5f5; color: #d32f2f; font-weight: bold; padding: 8px 12px;"
        )
        form_name.addRow(self.edit_delete_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Icon cảnh báo + thông báo
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)  # Giảm khoảng cách giữa icon và text
        delete_icon = QLabel()
        delete_qicon = QIcon(DELETE_SVG)
        delete_icon.setPixmap(delete_qicon.pixmap(24, 24))  # Icon nhỏ hơn
        header_layout.addWidget(delete_icon)

        message_label = QLabel(
            "Bạn có chắc chắn muốn xóa? Hành động này không thể khôi phục!"
        )
        message_label.setStyleSheet(
            "font-size: 12px; color: #d32f2f; font-weight: bold;"
        )
        message_label.setWordWrap(True)
        header_layout.addWidget(message_label, 1)
        header_layout.addStretch()  # Đẩy về bên trái
        main_layout.addLayout(header_layout)

        # Tăng khoảng cách giữa cảnh báo và button
        main_layout.addSpacing(16)

        # Nút xóa và hủy - nằm trên 1 dòng, mỗi nút 50% chiều rộng
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_confirm = QPushButton("Xóa")
        btn_cancel = QPushButton("Hủy")
        btn_confirm.setStyleSheet(
            f"background: #d32f2f; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        btn_confirm.setCursor(Qt.PointingHandCursor)
        btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(btn_confirm, 1)  # 50% chiều rộng
        btn_layout.addWidget(btn_cancel, 1)  # 50% chiều rộng
        main_layout.addLayout(btn_layout)

        btn_confirm.clicked.connect(self.confirm_delete)
        btn_cancel.clicked.connect(self.reject)

    def confirm_delete(self):
        try:
            log_to_debug(f"DialogJobTitleDelete: Xóa chức danh ID {self.job_title_id}")

            # Gọi service để xóa từ DB
            try:
                from services.job_title_services import JobTitleService

                service = JobTitleService()
                if service.delete_job_title(self.job_title_id):
                    log_to_debug(
                        f"DialogJobTitleDelete: Chức danh '{self.job_title_name}' đã được xóa"
                    )
                else:
                    log_to_debug(
                        f"DialogJobTitleDelete: Lỗi xóa chức danh '{self.job_title_name}'"
                    )
            except Exception as e:
                log_to_debug(
                    f"DialogJobTitleDelete: Lỗi xóa chức danh: {e}\n{traceback.format_exc()}"
                )

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogJobTitleDelete: Lỗi confirm_delete: {e}\n{traceback.format_exc()}"
            )
