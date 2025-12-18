from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal
import os


class CompanyController(QObject):
    icon_changed = Signal(str)  # signal truyền path icon mới

    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog
        self.dialog.btn_change_logo.clicked.connect(self.handle_change_logo)
        self.dialog.btn_save_close.clicked.connect(self.handle_save_close)

    def handle_change_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.dialog,
            "Chọn ảnh logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.ico)",
        )
        if file_path:
            import shutil

            icons_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../assets/icons")
            )
            if not os.path.exists(icons_dir):
                os.makedirs(icons_dir)
            dest_path = os.path.join(icons_dir, "app.ico")
            try:
                shutil.copyfile(file_path, dest_path)
            except Exception as e:
                return
            pixmap = QPixmap(dest_path)
            if not pixmap.isNull():
                from PySide6.QtCore import Qt

                self.dialog.logo_label.setPixmap(
                    pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                # Cập nhật vào DB qua service và phát signal cập nhật icon
                try:
                    from services.company_services import CompanyService
                    from core import resource

                    service = CompanyService()
                    info = service.get_company_info()
                    service.update_company_info(
                        info.get("name", ""),
                        info.get("phone", ""),
                        info.get("address", ""),
                        dest_path,
                    )
                    # Sử dụng set_app_ico_path để cập nhật với resource_path
                    resource.set_app_ico_path(dest_path)
                    # Cập nhật icon cho chính dialog này
                    if hasattr(self.dialog, "update_window_icon"):
                        self.dialog.update_window_icon(dest_path)
                    self.icon_changed.emit(
                        dest_path
                    )  # Phát signal cập nhật icon cho các cửa sổ khác
                except Exception as e:
                    pass
            else:
                pass

    def handle_save_close(self):
        # Lưu thông tin công ty vào DB qua service
        try:
            from services.company_services import CompanyService

            service = CompanyService()
            name = self.dialog.edit_company_name.text()
            phone = self.dialog.edit_phone.text()
            address = self.dialog.edit_address.text()
            # Lấy logo_path hiện tại từ DB (nếu có)
            info = service.get_company_info()
            logo_path = info.get("logo_path", "")
            service.update_company_info(name, phone, address, logo_path)
        except Exception as e:
            pass
        self.dialog.accept()
