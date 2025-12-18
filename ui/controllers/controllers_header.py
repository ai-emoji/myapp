from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from core.resource import ACTIVE, FONT_WEIGHT_SEMIBOLD


def show_debug_log_messagebox(parent=None):
    """
    Mô tả:
        Hiển thị nội dung debug.log ra MessageBox.
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """
    log_content = show_debug_log()
    msg = QMessageBox(parent)
    msg.setWindowTitle("Debug Log")
    msg.setTextInteractionFlags(msg.textInteractionFlags() | Qt.TextSelectableByMouse)
    msg.setIcon(QMessageBox.Information)
    msg.setText("Nội dung debug.log:")
    msg.setDetailedText(log_content)
    msg.exec()


from core.resource import resource_path


def show_debug_log():
    """
    Mô tả:
        Đọc và trả về nội dung file log/debug.log để hiển thị debug log.
    Args:
        None
    Returns:
        str: Nội dung log
    """
    import os

    log_path = resource_path(os.path.join("log", "debug.log"))
    if not os.path.exists(log_path):
        return "[Chưa có log]"
    with open(log_path, "r", encoding="utf-8") as f:
        return f.read()


"""
Mô tả:
    Controller cho header UI, xử lý ẩn/hiện nhóm nút chức năng theo nhóm khi click các nút chính.
Args:
    widgets_header2 (WidgetsHeader2): instance header2
Returns:
    None
"""

from PySide6.QtCore import QObject


class HeaderController(QObject):
    def __init__(self, widgets_header1, widgets_header2, main_window):
        super().__init__()
        self.header1 = widgets_header1
        self.header2 = widgets_header2
        self.main_window = (
            main_window  # Tham chiếu main_window để thao tác nội dung chính
        )
        self._connect_signals()
        self.active_btn = None
        self.show_group("khai_bao")

    def _connect_signals(self):
        self.header1.btn_khaibao.clicked.connect(lambda: self.show_group("khai_bao"))
        self.header1.btn_ketnoi.clicked.connect(lambda: self.show_group("ket_noi"))
        self.header1.btn_chamcong.clicked.connect(lambda: self.show_group("cham_cong"))
        self.header1.btn_congcu.clicked.connect(lambda: self.show_group("cong_cu"))
        # Kết nối nút khai báo chức danh để hiển thị widget chức danh
        self.header2.btn_khaibao_chucdanh.clicked.connect(self.show_job_title_widget)
        # Kết nối nút khai báo phòng ban để hiển thị widget phòng ban
        self.header2.btn_khaibao_phongban.clicked.connect(self.show_department_widget)
        # Kết nối nút thông tin nhân viên để hiển thị widget nhân viên
        self.header2.btn_thongtin_nhanvien.clicked.connect(self.show_employee_widget)
        # Kết nối nút khai báo ngày lễ để hiển thị widget ngày lễ
        self.header2.btn_khaibao_ngayle.clicked.connect(self.show_holiday_widget)
        # Kết nối nút khai báo ngày lễ để hiển thị widget ngày lễ
        self.header2.btn_khaibao_ngayle.clicked.connect(self.show_holiday_widget)
        # Kết nối nút khai báo ca để hiển thị widget khai báo ca làm việc
        self.header2.btn_khaibao_ca.clicked.connect(self.show_declare_work_shift_widget)
        # Kết nối nút máy chấm công để hiển thị widget quản lý thiết bị
        self.header2.btn_maychamcong.clicked.connect(self.show_device_widget)
        # Kết nối nút tải máy chấm công để hiển thị widget tải dữ liệu
        self.header2.btn_tai_maychamcong.clicked.connect(self.show_download_attendence_widget)
        # Kết nối nút tải nhân viên lên máy chấm công để hiển thị widget shift
        self.header2.btn_tai_nv_len.clicked.connect(self.show_shift_widget)
        # Kết nối nút ký hiệu chấm công để hiển thị dialog cấu hình
        self.header2.btn_kyhieu_chamcong.clicked.connect(
            self.show_attendance_symbol_dialog
        )
        # Kết nối nút chọn ngày cuối tuần để hiển thị dialog cấu hình
        self.header2.btn_chon_cuoituan.clicked.connect(self.show_weekend_dialog)
        # Kết nối nút ký hiệu các loại vắng để hiển thị dialog
        self.header2.btn_kyhieu_vang.clicked.connect(self.show_absence_symbol_dialog)
        # Kết nối nút sao lưu để hiển thị dialog backup
        self.header2.btn_saoluu.clicked.connect(self.show_backup_dialog)
        # Kết nối nút khôi phục để hiển thị dialog restore
        self.header2.btn_khoiphuc.clicked.connect(self.show_restore_dialog)

    def show_group(self, group):
        # Đặt lại style cho tất cả nút header1 (reset BG)
        btns = [
            self.header1.btn_khaibao,
            self.header1.btn_ketnoi,
            self.header1.btn_chamcong,
            self.header1.btn_congcu,
        ]
        active_style = (
            f"QPushButton {{ background: {ACTIVE}; border: none; padding: 0; }}\n"
            f"QPushButton:hover {{ background: {ACTIVE}; font-weight: {FONT_WEIGHT_SEMIBOLD}; }}"
        )
        default_style = (
            "QPushButton { border: none; padding: 0; }\n"
            f"QPushButton:hover {{ background: {ACTIVE}; font-weight: {FONT_WEIGHT_SEMIBOLD}; }}"
        )
        for btn in btns:
            btn.setStyleSheet(default_style)
        if group == "khai_bao":
            self.header1.btn_khaibao.setStyleSheet(active_style)
        elif group == "ket_noi":
            self.header1.btn_ketnoi.setStyleSheet(active_style)
        elif group == "cham_cong":
            self.header1.btn_chamcong.setStyleSheet(active_style)
        elif group == "cong_cu":
            self.header1.btn_congcu.setStyleSheet(active_style)
        # Ẩn tất cả QToolButton trước
        from PySide6.QtWidgets import QToolButton

        for btn in self.header2.findChildren(QToolButton):
            btn.setVisible(False)
        # Hiện nhóm tương ứng
        if group == "khai_bao":
            show_btns = [
                self.header2.btn_thongtin_cty,
                self.header2.btn_khaibao_chucdanh,
                self.header2.btn_khaibao_phongban,
                self.header2.btn_thongtin_nhanvien,
                self.header2.btn_khaibao_ngayle,
                self.header2.btn_doimatkhau,
                self.header2.btn_thoat,
            ]
        elif group == "ket_noi":
            show_btns = [
                self.header2.btn_maychamcong,
                self.header2.btn_tai_maychamcong,
                self.header2.btn_tai_nv_ve,
                self.header2.btn_tai_nv_len,
            ]
        elif group == "cham_cong":
            show_btns = [
                self.header2.btn_khaibao_ca,
                self.header2.btn_kyhieu_chamcong,
                self.header2.btn_kyhieu_vang,
                self.header2.btn_chon_cuoituan,
                self.header2.btn_chamcong_theoca,
            ]
        elif group == "cong_cu":
            show_btns = [
                self.header2.btn_saoluu,
                self.header2.btn_khoiphuc,
            ]
        else:
            show_btns = []
        for btn in show_btns:
            btn.setVisible(True)
        # Đảm bảo cập nhật layout và giao diện ngay
        hbox = getattr(self.header2, "hbox", None)
        if hbox is not None:
            hbox.activate()  # Ép layout cập nhật lại
        self.header2.updateGeometry()
        self.header2.update()
        self.header2.repaint()
        self.header2.show()

        # Kết nối click Thông tin công ty để mở dialog
        self.header2.btn_thongtin_cty.clicked.connect(self.show_company_dialog)

    def show_company_dialog(self):
        """
        Hiển thị dialog thông tin công ty ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_company import DialogCompany

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogCompany(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_job_title_widget(self):
        """
        Mô tả:
            Hiển thị widget khai báo chức danh vào vùng nội dung chính của main_window.
        Args:
            None
        Returns:
            None
        """
        from ui.widgets.widgets_job_title import WidgetsJobTitle

        # Xóa widget cũ nếu có
        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsJobTitle(self.main_window))

    def show_department_widget(self):
        """
        Mô tả:
            Hiển thị widget khai báo phòng ban vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_department import WidgetsDepartment

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsDepartment(self.main_window))

    def show_employee_widget(self):
        """
        Mô tả:
            Hiển thị widget thông tin nhân viên vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_employee import WidgetsEmployee

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsEmployee(self.main_window))

    def show_holiday_widget(self):
        """
        Mô tả:
            Hiển thị widget khai báo ngày lễ vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_holiday import WidgetsHoliday

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsHoliday(self.main_window))

    def show_attendance_symbol_dialog(self):
        """
        Mô tả:
            Hiển thị dialog cấu hình ký hiệu chấm công ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_attendance_symbol import DialogAttendanceSymbol

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogAttendanceSymbol(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_weekend_dialog(self):
        """
        Mô tả:
            Hiển thị dialog cấu hình ngày cuối tuần ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_weekend import DialogWeekend

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogWeekend(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_absence_symbol_dialog(self):
        """
        Mô tả:
            Hiển thị dialog cấu hình ký hiệu loại vắng ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_absence_symbol import DialogAbsenceSymbol

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogAbsenceSymbol(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_backup_dialog(self):
        """
        Mô tả:
            Hiển thị dialog sao lưu dữ liệu ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_backup import DialogBackup

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogBackup(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_restore_dialog(self):
        """
        Mô tả:
            Hiển thị dialog khôi phục dữ liệu ở giữa cửa sổ chính
        """
        from ui.dialog.dialog_absence_restore import DialogAbsenceRestore

        # Tìm main window cha
        main_window = self.header2.window()
        dlg = DialogAbsenceRestore(parent=main_window)
        # Đặt dialog ra giữa cửa sổ chính
        geo = main_window.geometry()
        dlg.move(
            geo.x() + (geo.width() - dlg.width()) // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.exec()

    def show_declare_work_shift_widget(self):
        """
        Mô tả:
            Hiển thị widget khai báo ca làm việc vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_declare_work_shift import WidgetsDeclareWorkShift

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsDeclareWorkShift(self.main_window))

    def show_device_widget(self):
        """
        Mô tả:
            Hiển thị widget quản lý thiết bị chấm công vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_device import WidgetsDevice

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsDevice(self.main_window))

    def show_download_attendence_widget(self):
        """
        Mô tả:
            Hiển thị widget tải dữ liệu chấm công vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_download_attendence import WidgetsDownloadAttendence

        if hasattr(self.main_window, "set_main_content"):
            self.main_window.set_main_content(WidgetsDownloadAttendence(self.main_window))

    def show_shift_widget(self):
        """
        Mô tả:
            Hiển thị widget tải nhân viên lên máy chấm công vào vùng nội dung chính của main_window.
        """
        from ui.widgets.widgets_shift import WidgetsShift
        from ui.controllers.controllers_shift import ControllerWidgetsShift

        if hasattr(self.main_window, "set_main_content"):
            widget = WidgetsShift(self.main_window)
            # Khởi tạo controller cho widget
            controller = ControllerWidgetsShift(widget)
            widget.set_controller(controller)
            self.main_window.set_main_content(widget)
