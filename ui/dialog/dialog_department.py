import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from core.resource import (
    FONT_WEIGHT_BOLD,
    BUTTON_BG,
    CANCEL_BUTTON_BG,
    DEPARTMENT_SVG,
    APP_ICO_PATH,
    BG_DIALOG,
)
from services.department_services import DepartmentService


class DialogDepartmentBase(QDialog):
    def __init__(self, parent=None, title="Phòng Ban", width=500, height=280):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(width, height)
        self.setContentsMargins(12, 18, 12, 18)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        self.service = DepartmentService()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Group 1: Tên phòng ban
        group_name = QGroupBox("Tên phòng ban")
        group_name.setFixedHeight(80)
        form_name = QFormLayout()
        self.edit_name = QLineEdit()
        self.edit_name.setMaxLength(100)
        self.edit_name.setPlaceholderText("Nhập tên phòng ban...")
        self.edit_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        form_name.addRow(self.edit_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Group 2: Phòng ban cha
        group_parent = QGroupBox("Phòng ban cha")
        group_parent.setFixedHeight(80)
        form_parent = QFormLayout()
        self.combo_parent = QComboBox()
        self.combo_parent.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px;"
        )
        form_parent.addRow(self.combo_parent)
        group_parent.setLayout(form_parent)
        main_layout.addWidget(group_parent)

        # Khoảng cách giữa input và nút
        main_layout.addSpacing(16)

        # Buttons
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

        self.edit_name.textChanged.connect(self._on_name_changed)
        self._load_parent_options()

    def _load_parent_options(self):
        """Load danh sách phòng ban làm cha, có tùy chọn (Không có)"""
        self.combo_parent.clear()
        self.combo_parent.addItem("(Không có)", None)
        try:
            # Lấy dep_id nếu đang ở chế độ edit để loại trừ khỏi danh sách
            exclude_id = getattr(self, "dep_id", None)
            for item in self.service.get_hierarchy():
                # Không cho phép chọn chính nó làm parent
                if exclude_id is not None and item["id"] == exclude_id:
                    continue
                self.combo_parent.addItem(
                    QIcon(DEPARTMENT_SVG), item["display_name"], item["id"]
                )
        except Exception as e:
            log_to_debug(
                f"DialogDepartmentBase: Lỗi load parent options: {e}\n{traceback.format_exc()}"
            )

    def _capitalize_first(self, text):
        """Viết hoa chữ cái đầu của mỗi từ (Xin Chào)"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return
        # Viết hoa chữ cái đầu của mỗi từ
        words = text.split()
        cap = " ".join(word.capitalize() for word in words)
        if text != cap:
            pos = self.edit_name.cursorPosition()
            self.edit_name.blockSignals(True)
            self.edit_name.setText(cap)
            self.edit_name.setCursorPosition(pos)
            self.edit_name.blockSignals(False)

    def _on_name_changed(self, text):
        # Áp dụng viết hoa và reset trạng thái lỗi nếu có
        self._capitalize_first(text)
        self.edit_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; padding: 8px 12px;"
        )


class DialogDepartmentAdd(DialogDepartmentBase):
    def __init__(self, parent=None, default_parent_id=None):
        super().__init__(parent, title="Thêm Phòng Ban Mới")
        log_to_debug("DialogDepartmentAdd: Khởi tạo")
        # Chọn sẵn phòng ban cha nếu truyền vào
        if default_parent_id is not None:
            try:
                for i in range(self.combo_parent.count()):
                    if self.combo_parent.itemData(i) == default_parent_id:
                        self.combo_parent.setCurrentIndex(i)
                        break
            except Exception:
                pass
        self.btn_save.clicked.connect(self._save)

    def _save(self):
        name = self.edit_name.text().strip()
        if not name:
            log_to_debug("DialogDepartmentAdd: Tên trống")
            return
        parent_id = self.combo_parent.currentData()
        if self.service.add_department(name, parent_id):
            log_to_debug(f"DialogDepartmentAdd: Đã lưu '{name}'")
            self.accept()
        else:
            log_to_debug(f"DialogDepartmentAdd: Lưu thất bại '{name}' (trùng?)")
            self.edit_name.setStyleSheet(
                f"font-weight: {FONT_WEIGHT_BOLD}; padding: 8px 12px; border: 1px solid #d32f2f;"
            )


class DialogDepartmentEdit(DialogDepartmentBase):
    def __init__(self, parent=None, dep_id=None, suggested_parent_id=None):
        self.dep_id = dep_id
        self.suggested_parent_id = suggested_parent_id
        super().__init__(parent, title="Sửa Đổi Phòng Ban")
        log_to_debug(f"DialogDepartmentEdit: Khởi tạo (ID: {dep_id})")
        self.btn_save.clicked.connect(self._save)
        self._load_data()

    def _load_data(self):
        try:
            info = self.service.get_department_by_id(self.dep_id)
            if info:
                self.edit_name.setText(info.get("name", ""))
                # set parent selection to current saved parent
                parent_id = info.get("parent_id")
                log_to_debug(
                    f"DialogDepartmentEdit: Loading dep_id={self.dep_id}, parent_id={parent_id}"
                )

                # Debug: in tất cả items trong combo
                for i in range(self.combo_parent.count()):
                    item_text = self.combo_parent.itemText(i)
                    item_data = self.combo_parent.itemData(i)
                    log_to_debug(f"  Combo[{i}]: text='{item_text}', data={item_data}")

                # Tìm và chọn parent_id
                found = False
                for i in range(self.combo_parent.count()):
                    if self.combo_parent.itemData(i) == parent_id:
                        self.combo_parent.setCurrentIndex(i)
                        log_to_debug(f"  -> Chọn index {i} (parent_id={parent_id})")
                        found = True
                        break

                if not found:
                    log_to_debug(
                        f"  -> Không tìm thấy parent_id={parent_id}, giữ mặc định"
                    )

                # if suggested parent provided and not self, prefer it
                if (
                    self.suggested_parent_id is not None
                    and self.suggested_parent_id != self.dep_id
                ):
                    for i in range(self.combo_parent.count()):
                        if self.combo_parent.itemData(i) == self.suggested_parent_id:
                            self.combo_parent.setCurrentIndex(i)
                            log_to_debug(
                                f"  -> Ghi đè bằng suggested_parent_id={self.suggested_parent_id}, index={i}"
                            )
                            break
        except Exception as e:
            log_to_debug(
                f"DialogDepartmentEdit: Lỗi load_data: {e}\n{traceback.format_exc()}"
            )

    def _save(self):
        name = self.edit_name.text().strip()
        if not name:
            log_to_debug("DialogDepartmentEdit: Tên trống")
            return
        parent_id = self.combo_parent.currentData()
        if self.service.update_department(self.dep_id, name, parent_id):
            log_to_debug(f"DialogDepartmentEdit: Đã cập nhật '{name}'")
            self.accept()
        else:
            log_to_debug(f"DialogDepartmentEdit: Cập nhật thất bại '{name}' (trùng?)")
            self.edit_name.setStyleSheet(
                f"font-weight: {FONT_WEIGHT_BOLD}; padding: 8px 12px; border: 1px solid #d32f2f;"
            )


class DialogDepartmentDelete(QDialog):
    def __init__(self, parent=None, dep_id=None, dep_name=""):
        super().__init__(parent)
        self.dep_id = dep_id
        self.dep_name = dep_name
        self.setWindowTitle("Xác Nhận Xóa Phòng Ban")
        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(460, 220)
        self.setContentsMargins(12, 18, 12, 18)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Input hiển thị tên phòng ban cần xóa
        group_name = QGroupBox("Phòng ban cần xóa")
        group_name.setFixedHeight(80)
        form_name = QFormLayout()
        self.edit_delete_name = QLineEdit()
        self.edit_delete_name.setText(dep_name)
        self.edit_delete_name.setReadOnly(True)
        self.edit_delete_name.setStyleSheet(
            "background: #f5f5f5; color: #d32f2f; font-weight: bold; padding: 8px 12px;"
        )
        form_name.addRow(self.edit_delete_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Cảnh báo trên 1 hàng (icon + chữ gần nhau)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        warn_icon = QLabel()
        warn_icon.setPixmap(QIcon(DEPARTMENT_SVG).pixmap(24, 24))
        header_layout.addWidget(warn_icon)
        msg = QLabel("Bạn có chắc chắn muốn xóa? Hành động này không thể khôi phục!")
        msg.setStyleSheet("font-size: 12px; color: #d32f2f; font-weight: bold;")
        msg.setWordWrap(True)
        header_layout.addWidget(msg, 1)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(16)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_delete = QPushButton("Xóa")
        btn_cancel = QPushButton("Hủy")
        btn_delete.setStyleSheet(
            "background: #d32f2f; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        btn_delete.setCursor(Qt.PointingHandCursor)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(btn_delete, 1)
        btn_layout.addWidget(btn_cancel, 1)
        main_layout.addLayout(btn_layout)

        btn_cancel.clicked.connect(self.reject)
        btn_delete.clicked.connect(self._confirm_delete)

    def _confirm_delete(self):
        try:
            service = DepartmentService()
            # Kiểm tra trước xem có phòng ban con không
            if service.repo.has_children(self.dep_id):
                QMessageBox.warning(
                    self,
                    "Không thể xóa",
                    f"Không thể xóa phòng ban '{self.dep_name}' vì còn phòng ban con.\n\nVui lòng xóa hoặc di chuyển các phòng ban con trước!",
                    QMessageBox.Ok,
                )
                log_to_debug(
                    f"DialogDepartmentDelete: Không thể xóa '{self.dep_name}' - còn phòng ban con"
                )
                return

            if service.delete_department(self.dep_id):
                log_to_debug(f"DialogDepartmentDelete: Đã xóa '{self.dep_name}'")
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể xóa phòng ban '{self.dep_name}'.\n\nVui lòng thử lại!",
                    QMessageBox.Ok,
                )
                log_to_debug(f"DialogDepartmentDelete: Xóa thất bại '{self.dep_name}'")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Có lỗi xảy ra khi xóa phòng ban:\n\n{str(e)}",
                QMessageBox.Ok,
            )
            log_to_debug(
                f"DialogDepartmentDelete: Lỗi delete: {e}\n{traceback.format_exc()}"
            )
