# controllers_widgets_device.py
# Controller cho widgets_device.py

import traceback
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


class ControllerWidgetsDevice:
    """Controller xử lý logic cho widgets_device.py"""

    def __init__(self, widget):
        self.widget = widget
        self.current_device_id = None  # ID của thiết bị đang được chọn
        self._connect_signals()
        self._load_devices()

    def _connect_signals(self):
        """Kết nối signals với slots"""
        try:
            # Kết nối các nút chức năng
            self.widget.btn_add.clicked.connect(self._on_add_clicked)
            self.widget.btn_save.clicked.connect(self._on_save_clicked)
            self.widget.btn_delete.clicked.connect(self._on_delete_clicked)
            self.widget.btn_connect.clicked.connect(self._on_connect_clicked)

            # Kết nối sự kiện chọn hàng trong bảng
            self.widget.table.itemSelectionChanged.connect(self._on_selection_changed)

            log_to_debug("ControllerWidgetsDevice: Signals connected")
        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _connect_signals() error: {e}\n{traceback.format_exc()}"
            )

    def _load_devices(self):
        """Load danh sách thiết bị từ database và hiển thị lên bảng"""
        try:
            log_to_debug("ControllerWidgetsDevice: _load_devices() called")
            from services.device_services import DeviceService

            service = DeviceService()
            devices = service.get_all_devices()

            # Clear bảng
            self.widget.table.setRowCount(0)

            # Thêm dữ liệu vào bảng
            for device in devices:
                row = self.widget.table.rowCount()
                self.widget.table.insertRow(row)

                # Cột 0: Số máy
                item_number = QTableWidgetItem(str(device["device_number"]))
                item_number.setData(Qt.UserRole, device["id"])  # Lưu ID vào UserRole
                self.widget.table.setItem(row, 0, item_number)

                # Cột 1: Tên máy
                item_name = QTableWidgetItem(device["device_name"])
                self.widget.table.setItem(row, 1, item_name)

                # Cột 2: Địa chỉ IP
                item_ip = QTableWidgetItem(device["ip_address"])
                self.widget.table.setItem(row, 2, item_ip)

            log_to_debug(f"ControllerWidgetsDevice: Loaded {len(devices)} devices")

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _load_devices() error: {e}\n{traceback.format_exc()}"
            )

    def _on_selection_changed(self):
        """Xử lý khi chọn một hàng trong bảng"""
        try:
            selected_items = self.widget.table.selectedItems()
            if not selected_items:
                self._clear_form()
                return

            # Lấy device_id từ cột đầu tiên
            row = selected_items[0].row()
            device_id = self.widget.table.item(row, 0).data(Qt.UserRole)

            log_to_debug(f"ControllerWidgetsDevice: Selected device_id={device_id}")

            # Load thông tin thiết bị
            from services.device_services import DeviceService

            service = DeviceService()
            device = service.get_device_by_id(device_id)

            if device:
                self.current_device_id = device_id
                self._fill_form(device)

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _on_selection_changed() error: {e}\n{traceback.format_exc()}"
            )

    def _fill_form(self, device):
        """Điền thông tin thiết bị vào form"""
        try:
            self.widget.input_device_number.setText(device["device_number"])
            self.widget.input_device_name.setText(device["device_name"])
            self.widget.set_ip_address(device["ip_address"])
            self.widget.input_password.setText(device.get("password", ""))
            self.widget.input_port.setText(str(device.get("port", 4370)))
            self.widget.input_note.setText(device.get("note", ""))
            self._update_status_display(device.get("status", "Chưa kết nối"))

            log_to_debug("ControllerWidgetsDevice: Form filled successfully")
        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _fill_form() error: {e}\n{traceback.format_exc()}"
            )

    def _clear_form(self):
        """Xóa form"""
        try:
            self.current_device_id = None
            self.widget.input_device_number.clear()
            self.widget.input_device_name.clear()
            self.widget.set_ip_address("")
            self.widget.input_password.clear()
            self.widget.input_port.setText("4370")
            self.widget.input_note.clear()
            self._update_status_display("Chưa kết nối")

            log_to_debug("ControllerWidgetsDevice: Form cleared")
        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _clear_form() error: {e}\n{traceback.format_exc()}"
            )

    def _update_status_display(self, status):
        """Cập nhật hiển thị trạng thái với màu sắc phù hợp"""
        self.widget.lbl_status_value.setText(status)
        
        # Xác định màu dựa trên trạng thái
        if status == "Đã kết nối":
            color = "#28a745"  # Màu xanh lá
            bg_color = "#d4edda"  # Nền xanh nhạt
        elif status in ["Chưa kết nối", "Kết nối thất bại", "Không thể kết nối", "Lỗi kết nối"]:
            color = "#dc3545"  # Màu đỏ
            bg_color = "#f8d7da"  # Nền đỏ nhạt
        else:
            color = "#666"  # Màu xám
            bg_color = "#f5f5f5"  # Nền xám nhạt
        
        # Cập nhật style
        self.widget.lbl_status_value.setStyleSheet(
            f"""
            QLabel {{
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 14px;
                background: {bg_color};
                color: {color};
                font-weight: bold;
            }}
            """
        )

    def _on_add_clicked(self):
        """Xử lý khi click nút Thêm mới"""
        try:
            log_to_debug("ControllerWidgetsDevice: Add button clicked")
            self._clear_form()
            self.widget.table.clearSelection()
            self.widget.input_device_number.setFocus()

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _on_add_clicked() error: {e}\n{traceback.format_exc()}"
            )

    def _on_save_clicked(self):
        """Xử lý khi click nút Lưu"""
        try:
            log_to_debug("ControllerWidgetsDevice: Save button clicked")

            # Lấy dữ liệu từ form
            device_number = self.widget.input_device_number.text().strip()
            device_name = self.widget.input_device_name.text().strip()
            ip_address = self.widget.get_ip_address()
            password = self.widget.input_password.text().strip()
            port = self.widget.input_port.text().strip()
            note = self.widget.input_note.text().strip()

            from services.device_services import DeviceService

            service = DeviceService()

            if self.current_device_id is None:
                # Thêm mới
                success, message = service.add_device(
                    device_number, device_name, ip_address, password, port, note
                )
            else:
                # Cập nhật
                success, message = service.update_device(
                    self.current_device_id,
                    device_number,
                    device_name,
                    ip_address,
                    password,
                    port,
                    note,
                )

            # Hiển thị thông báo
            if success:
                QMessageBox.information(self.widget, "Thành công", message)
                self._load_devices()
                self._clear_form()
            else:
                QMessageBox.warning(self.widget, "Lỗi", message)

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _on_save_clicked() error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self.widget, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def _on_delete_clicked(self):
        """Xử lý khi click nút Xóa"""
        try:
            log_to_debug("ControllerWidgetsDevice: Delete button clicked")

            if self.current_device_id is None:
                QMessageBox.warning(
                    self.widget, "Cảnh báo", "Vui lòng chọn thiết bị cần xóa"
                )
                return

            # Xác nhận xóa
            reply = QMessageBox.question(
                self.widget,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa thiết bị này?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                from services.device_services import DeviceService

                service = DeviceService()
                success, message = service.delete_device(self.current_device_id)

                if success:
                    QMessageBox.information(self.widget, "Thành công", message)
                    self._load_devices()
                    self._clear_form()
                else:
                    QMessageBox.warning(self.widget, "Lỗi", message)

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _on_delete_clicked() error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self.widget, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def _on_connect_clicked(self):
        """Xử lý khi click nút Kết nối - Test kết nối với thiết bị"""
        try:
            log_to_debug("ControllerWidgetsDevice: Connect button clicked")

            # Lấy thông tin kết nối từ form
            ip_address = self.widget.get_ip_address()
            port = self.widget.input_port.text().strip()
            password = self.widget.input_password.text().strip()

            if not ip_address:
                QMessageBox.warning(
                    self.widget, "Cảnh báo", "Vui lòng nhập địa chỉ IP"
                )
                return

            if not port:
                QMessageBox.warning(
                    self.widget, "Cảnh báo", "Vui lòng nhập cổng kết nối"
                )
                return

            # Test kết nối
            from services.device_services import DeviceService

            service = DeviceService()
            
            # Hiển thị thông báo đang kết nối
            self._update_status_display("Đang kết nối...")
            self.widget.lbl_status_value.repaint()

            success, message = service.test_connection(ip_address, int(port), password)

            if success:
                # Không hiển thị MessageBox, chỉ cập nhật trạng thái
                self._update_status_display("Đã kết nối")
                
                # Cập nhật trạng thái vào database nếu đã lưu
                if self.current_device_id:
                    service.update_device_status(self.current_device_id, "Đã kết nối")
                    # Reload lại danh sách để cập nhật trạng thái
                    self._load_devices()
            else:
                # Không hiển thị MessageBox, chỉ cập nhật trạng thái
                self._update_status_display("Không thể kết nối")
                
                # Cập nhật trạng thái vào database nếu đã lưu
                if self.current_device_id:
                    service.update_device_status(self.current_device_id, "Không thể kết nối")
                    # Reload lại danh sách để cập nhật trạng thái
                    self._load_devices()

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDevice: _on_connect_clicked() error: {e}\n{traceback.format_exc()}"
            )
            # Không hiển thị MessageBox, chỉ cập nhật trạng thái
            self._update_status_display("Lỗi kết nối")
