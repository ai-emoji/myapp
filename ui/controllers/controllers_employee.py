import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


class ControllerEmployee:
    """Controller xử lý logic nhân viên"""

    def __init__(self, main_window=None):
        self.main_window = main_window

    def show_employee_widget(self):
        """Hiển thị widget nhân viên"""
        try:
            from ui.widgets.widgets_employee import WidgetsEmployee

            log_to_debug("ControllerEmployee: show_employee_widget() called")
            self.main_window.set_main_content(WidgetsEmployee(self.main_window))
        except Exception as e:
            log_to_debug(f"ControllerEmployee: Error in show_employee_widget: {e}")


class ControllersEmployee:
    """Controller xử lý sự kiện cho widget employee"""

    def __init__(self, widget):
        self.widget = widget

    def on_add(self):
        """Xử lý thêm nhân viên mới"""
        log_to_debug("ControllersEmployee: Add button clicked")
        from ui.dialog.dialog_employee import DialogEmployeeAdd

        dialog = DialogEmployeeAdd(self.widget)
        if dialog.exec():
            # Reload data và cập nhật tổng số
            self.widget._load_data()
            log_to_debug("ControllersEmployee: Đã thêm nhân viên thành công")

    def on_edit(self):
        """Xử lý sửa nhân viên"""
        log_to_debug("ControllersEmployee: Edit button clicked")

        # Lấy hàng đang chọn từ bảng frozen hoặc scrollable
        selected_rows_frozen = self.widget.table_frozen.selectionModel().selectedRows()
        selected_rows_scrollable = (
            self.widget.table_scrollable.selectionModel().selectedRows()
        )

        if not selected_rows_frozen and not selected_rows_scrollable:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.widget, "Chưa chọn", "Vui lòng chọn một nhân viên để sửa!"
            )
            return

        # Lấy row index
        row = (
            selected_rows_frozen[0].row()
            if selected_rows_frozen
            else selected_rows_scrollable[0].row()
        )

        # Lấy employee_id từ cột ẩn (cột 16 của bảng scrollable)
        emp_id_item = self.widget.table_scrollable.item(row, 16)
        if not emp_id_item:
            log_to_debug("ControllersEmployee: Không tìm thấy ID nhân viên")
            return

        emp_id = int(emp_id_item.text())

        # Lấy thông tin đầy đủ từ service
        try:
            employees = self.widget.employee_service.get_all_employees()
            employee_data = next((e for e in employees if e["id"] == emp_id), None)

            if not employee_data:
                from PySide6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self.widget, "Lỗi", "Không tìm thấy thông tin nhân viên!"
                )
                return

            from ui.dialog.dialog_employee import DialogEmployeeEdit

            dialog = DialogEmployeeEdit(self.widget, employee_data=employee_data)
            if dialog.exec():
                # Reload data
                self.widget._load_data()
                log_to_debug("ControllersEmployee: Đã cập nhật nhân viên thành công")

        except Exception as e:
            log_to_debug(
                f"ControllersEmployee: Lỗi khi edit: {e}\n{traceback.format_exc()}"
            )
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.critical(self.widget, "Lỗi", f"Không thể sửa nhân viên:\n{e}")

    def on_delete(self):
        """Xử lý xóa nhân viên"""
        log_to_debug("ControllersEmployee: Delete button clicked")

        # Lấy hàng đang chọn
        selected_rows_frozen = self.widget.table_frozen.selectionModel().selectedRows()
        selected_rows_scrollable = (
            self.widget.table_scrollable.selectionModel().selectedRows()
        )

        if not selected_rows_frozen and not selected_rows_scrollable:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.widget, "Chưa chọn", "Vui lòng chọn một nhân viên để xóa!"
            )
            return

        # Lấy row index
        row = (
            selected_rows_frozen[0].row()
            if selected_rows_frozen
            else selected_rows_scrollable[0].row()
        )

        # Lấy ID và tên từ bảng
        emp_id_item = self.widget.table_scrollable.item(row, 16)
        emp_name_item = self.widget.table_frozen.item(row, 1)

        if not emp_id_item or not emp_name_item:
            log_to_debug("ControllersEmployee: Không tìm thấy thông tin nhân viên")
            return

        emp_id = int(emp_id_item.text())
        emp_name = emp_name_item.text()

        # Hiển thị dialog xác nhận xóa
        try:
            from ui.dialog.dialog_employee import DialogEmployeeDelete

            dialog = DialogEmployeeDelete(
                self.widget, employee_data={"id": emp_id, "name": emp_name}
            )
            if dialog.exec():
                # Reload data và cập nhật tổng số
                self.widget._load_data()
                log_to_debug("ControllersEmployee: Đã xóa nhân viên thành công")

        except Exception as e:
            log_to_debug(
                f"ControllersEmployee: Lỗi khi delete: {e}\n{traceback.format_exc()}"
            )
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.critical(self.widget, "Lỗi", f"Không thể xóa nhân viên:\n{e}")

    def on_search(self, text):
        """Xử lý tìm kiếm nhân viên theo filter được chọn"""
        search_text = text.lower().strip()
        search_filter = self.widget.search_filter.currentText()

        log_to_debug(
            f"ControllersEmployee: Searching for '{text}' with filter '{search_filter}'"
        )

        if not search_text:
            # Hiển thị lại tất cả hàng
            for row in range(self.widget.table_frozen.rowCount()):
                self.widget.table_frozen.setRowHidden(row, False)
                self.widget.table_scrollable.setRowHidden(row, False)
            return

        # Lọc theo filter được chọn
        for row in range(self.widget.table_frozen.rowCount()):
            match = False

            if search_filter == "Tất cả":
                # Tìm trong tất cả các trường
                # Mã NV (cột 0 frozen)
                emp_code_item = self.widget.table_frozen.item(row, 0)
                emp_code = emp_code_item.text().lower() if emp_code_item else ""

                # Tên NV (cột 1 frozen)
                emp_name_item = self.widget.table_frozen.item(row, 1)
                emp_name = emp_name_item.text().lower() if emp_name_item else ""

                # Phòng ban (cột 0 scrollable)
                dept_item = self.widget.table_scrollable.item(row, 0)
                dept = dept_item.text().lower() if dept_item else ""

                # Chức vụ (cột 1 scrollable)
                job_item = self.widget.table_scrollable.item(row, 1)
                job = job_item.text().lower() if job_item else ""

                match = (
                    search_text in emp_code
                    or search_text in emp_name
                    or search_text in dept
                    or search_text in job
                )

            elif search_filter == "Mã NV":
                # Chỉ tìm trong Mã NV
                emp_code_item = self.widget.table_frozen.item(row, 0)
                emp_code = emp_code_item.text().lower() if emp_code_item else ""
                match = search_text in emp_code

            elif search_filter == "Tên NV":
                # Chỉ tìm trong Tên NV
                emp_name_item = self.widget.table_frozen.item(row, 1)
                emp_name = emp_name_item.text().lower() if emp_name_item else ""
                match = search_text in emp_name

            elif search_filter == "Phòng ban":
                # Chỉ tìm trong Phòng ban
                dept_item = self.widget.table_scrollable.item(row, 0)
                dept = dept_item.text().lower() if dept_item else ""
                match = search_text in dept

            elif search_filter == "Chức vụ":
                # Chỉ tìm trong Chức vụ
                job_item = self.widget.table_scrollable.item(row, 1)
                job = job_item.text().lower() if job_item else ""
                match = search_text in job

            self.widget.table_frozen.setRowHidden(row, not match)
            self.widget.table_scrollable.setRowHidden(row, not match)

    def on_department_clicked(self, item, column):
        """Xử lý khi click vào phòng ban - lọc nhân viên theo phòng ban"""
        log_to_debug(f"ControllersEmployee: Department clicked - {item.text(0)}")

        # Lấy department_id từ item data
        dept_id = item.data(0, 0x0100)  # Qt.UserRole
        if dept_id is None:
            log_to_debug("ControllersEmployee: No department ID found")
            return

        log_to_debug(f"ControllersEmployee: Filtering by department_id={dept_id}")

        # Lọc bảng theo department_id
        for row in range(self.widget.table_frozen.rowCount()):
            # Lấy department_id từ cột ẩn (cột 17 của bảng scrollable)
            dept_id_item = self.widget.table_scrollable.item(row, 17)
            if dept_id_item:
                row_dept_id = dept_id_item.text()
                # So sánh với department_id được chọn
                match = str(row_dept_id) == str(dept_id)
                self.widget.table_frozen.setRowHidden(row, not match)
                self.widget.table_scrollable.setRowHidden(row, not match)

    def on_refresh(self):
        """Xử lý làm mới - bỏ chọn phòng ban và hiển thị lại toàn bộ"""
        log_to_debug("ControllersEmployee: Refresh button clicked")

        # Bỏ chọn phòng ban trong tree
        self.widget.tree_departments.clearSelection()

        # Xóa text tìm kiếm
        self.widget.search_input.clear()

        # Hiển thị lại tất cả hàng
        for row in range(self.widget.table_frozen.rowCount()):
            self.widget.table_frozen.setRowHidden(row, False)
            self.widget.table_scrollable.setRowHidden(row, False)

        log_to_debug("ControllersEmployee: Refreshed - showing all employees")
