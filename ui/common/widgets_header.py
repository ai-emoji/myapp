from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QToolButton
from PySide6.QtGui import QCursor, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

from core.resource import (
    COMPANY_SVG,
    JOB_TITLE_SVG,
    DEPARTMENT_SVG,
    EMPLOYEE_SVG,
    HOLIDAY_SVG,
    PASSWORD_SVG,
    EXIT_SVG,
    HEADER_MIN_WIDTH,
    HEADER_HEIGHT,
    HEADER_1_HEIGHT,
    HEADER_2_HEIGHT,
    FUNCTON_1_WIDTH,
    FUNCTON_1_HEIGHT,
    FUNCTON_2_WIDTH,
    FUNCTON_2_HEIGHT,
    HOVER_BG,
    FONT_WEIGHT_BOLD,
    HEADER_1_BG,
    DEVICE_SVG,
    DOWNLOAD_ATTENDANCE_SVG,
    DOWNLOAD_STAFF_SVG,
    UPLOAD_STAFF_SVG,
    SHIFT_SVG,
    DECLARE_WORK_SHIFT_SVG,
    ATTENDANCE_SYMBOL_SVG,
    ABSENCE_SYMBOL_SVG,
    WEEKEND_SVG,
    BACKUP_SVG,
    ABSENCE_RESTORE_SVG,
)


import datetime
import os
import sys


class WidgetsHeader(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Thiết lập kích thước cố định cho header tổng
        self.setMinimumWidth(HEADER_MIN_WIDTH)
        self.setFixedHeight(HEADER_HEIGHT)
        self.setObjectName("WidgetsHeader")
        # Có thể thêm layout, widget con ở đây nếu cần


def log_debug(message):
    from core.resource import resource_path
    import os
    import datetime

    log_path = resource_path(os.path.join("log", "debug.log"))
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}] {message}\n"
        )


class WidgetsHeader1(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Thêm màu nền và border bottom cho header 1
        self.setStyleSheet(
            f"background: {HEADER_1_BG}; border-bottom: 1px solid #000000;"
        )
        btn_style = (
            f"QPushButton {{ border: none; padding: 0; }}\n"
            f"QPushButton:hover {{ background: {HOVER_BG};font-weight: {FONT_WEIGHT_BOLD}; }}"
        )
        # Tạo layout ngang cho các phím chức năng
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.btn_khaibao = QPushButton("Khai báo")
        self.btn_ketnoi = QPushButton("Kết nối")
        self.btn_chamcong = QPushButton("Chấm công")
        self.btn_congcu = QPushButton("Công cụ")

        btns = [
            (self.btn_khaibao, "Khai báo"),
            (self.btn_ketnoi, "Kết nối"),
            (self.btn_chamcong, "Chấm công"),
            (self.btn_congcu, "Công cụ"),
        ]
        for btn, label in btns:
            btn.setFixedSize(FUNCTON_1_WIDTH, FUNCTON_1_HEIGHT)
            btn.setStyleSheet(btn_style)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(
                lambda checked, l=label: log_debug(f"Button clicked: {l}")
            )
            layout.addWidget(btn)
        layout.addStretch(1)  # Đẩy nút về bên trái, không giãn đều


class WidgetsHeader2(QFrame):
    # Thêm border bottom cho header 2
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(HEADER_MIN_WIDTH)
        self.setMinimumHeight(HEADER_2_HEIGHT)  # Đảm bảo luôn có chiều cao
        self.setObjectName("WidgetsHeader2")
        self.setStyleSheet(
            f"background: {HEADER_1_BG}; border-bottom: 1px solid #000000;"
        )
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.hbox.setAlignment(Qt.AlignVCenter)

        self.btn_thongtin_cty = QToolButton(self)
        self.btn_thongtin_cty.setText("Thông tin công ty")
        self.btn_thongtin_cty.setIcon(QIcon(COMPANY_SVG))
        self.btn_khaibao_chucdanh = QToolButton(self)
        self.btn_khaibao_chucdanh.setText("Khai báo chức danh")
        self.btn_khaibao_chucdanh.setIcon(QIcon(JOB_TITLE_SVG))
        self.btn_khaibao_phongban = QToolButton(self)
        self.btn_khaibao_phongban.setText("Khai báo phòng ban")
        self.btn_khaibao_phongban.setIcon(QIcon(DEPARTMENT_SVG))
        self.btn_thongtin_nhanvien = QToolButton(self)
        self.btn_thongtin_nhanvien.setText("Thông tin nhân viên")
        self.btn_thongtin_nhanvien.setIcon(QIcon(EMPLOYEE_SVG))
        self.btn_khaibao_ngayle = QToolButton(self)
        self.btn_khaibao_ngayle.setText("Khai báo ngày lễ")
        self.btn_khaibao_ngayle.setIcon(QIcon(HOLIDAY_SVG))
        self.btn_doimatkhau = QToolButton(self)
        self.btn_doimatkhau.setText("Đổi mật khẩu")
        self.btn_doimatkhau.setIcon(QIcon(PASSWORD_SVG))
        self.btn_maychamcong = QToolButton(self)
        self.btn_maychamcong.setText("Máy chấm công")
        self.btn_maychamcong.setIcon(QIcon(DEVICE_SVG))
        self.btn_tai_maychamcong = QToolButton(self)
        self.btn_tai_maychamcong.setText("Tải máy chấm công")
        self.btn_tai_maychamcong.setIcon(QIcon(DOWNLOAD_ATTENDANCE_SVG))
        self.btn_tai_nv_ve = QToolButton(self)
        self.btn_tai_nv_ve.setText("Tải NV về máy tính")
        self.btn_tai_nv_ve.setIcon(QIcon(DOWNLOAD_STAFF_SVG))
        self.btn_tai_nv_len = QToolButton(self)
        self.btn_tai_nv_len.setText("Tải NV lên máy chấm công")
        self.btn_tai_nv_len.setIcon(QIcon(UPLOAD_STAFF_SVG))
        self.btn_khaibao_ca = QToolButton(self)
        self.btn_khaibao_ca.setText("Khai báo ca làm việc")
        self.btn_khaibao_ca.setIcon(QIcon(DECLARE_WORK_SHIFT_SVG))
        self.btn_kyhieu_chamcong = QToolButton(self)
        self.btn_kyhieu_chamcong.setText("Ký hiệu chấm công")
        self.btn_kyhieu_chamcong.setIcon(QIcon(ATTENDANCE_SYMBOL_SVG))
        self.btn_kyhieu_vang = QToolButton(self)
        self.btn_kyhieu_vang.setText("Ký hiệu các loại vắng")
        self.btn_kyhieu_vang.setIcon(QIcon(ABSENCE_SYMBOL_SVG))
        self.btn_chon_cuoituan = QToolButton(self)
        self.btn_chon_cuoituan.setText("Chọn ngày cuối tuần")
        self.btn_chon_cuoituan.setIcon(QIcon(WEEKEND_SVG))
        self.btn_chamcong_theoca = QToolButton(self)
        self.btn_chamcong_theoca.setText("Chấm công theo ca")
        self.btn_chamcong_theoca.setIcon(QIcon(SHIFT_SVG))
        self.btn_saoluu = QToolButton(self)
        self.btn_saoluu.setText("Sao lưu dữ liệu")
        self.btn_saoluu.setIcon(QIcon(BACKUP_SVG))
        self.btn_khoiphuc = QToolButton(self)
        self.btn_khoiphuc.setText("Khôi phục dữ liệu")
        self.btn_khoiphuc.setIcon(QIcon(ABSENCE_RESTORE_SVG))
        self.btn_thoat = QToolButton(self)
        self.btn_thoat.setText("Thoát ứng dụng")
        self.btn_thoat.setIcon(QIcon(EXIT_SVG))

        # Danh sách nút theo thứ tự, các nút mới nằm dưới nút Thoát ứng dụng
        btns = [
            self.btn_thongtin_cty,
            self.btn_khaibao_chucdanh,
            self.btn_khaibao_phongban,
            self.btn_thongtin_nhanvien,
            self.btn_khaibao_ngayle,
            self.btn_doimatkhau,
            self.btn_thoat,
            self.btn_maychamcong,
            self.btn_tai_maychamcong,
            self.btn_tai_nv_ve,
            self.btn_tai_nv_len,
            self.btn_khaibao_ca,
            self.btn_kyhieu_chamcong,
            self.btn_kyhieu_vang,
            self.btn_chon_cuoituan,
            self.btn_chamcong_theoca,
            self.btn_saoluu,
            self.btn_khoiphuc,
        ]

        for btn in btns:
            # Xử lý text để tất cả đều có 2 dòng
            text = btn.text()
            words = text.split()
            if len(words) >= 2:
                # Text có 2+ từ: chia làm 2 dòng cân bằng
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                btn.setText(f"{line1}\n{line2}")
            else:
                # Text 1 từ: thêm dòng trống phía trên
                btn.setText(f" \n{text}")
            btn.setFixedSize(FUNCTON_2_WIDTH, FUNCTON_2_HEIGHT)
            btn.setIconSize(QSize(32, 32))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet(
                f"""
                QToolButton {{
                    padding-top: 8px;
                    padding-bottom: 4px;
                    padding-left: 2px;
                    padding-right: 2px;
                    border: none;
                    background: none;
                }}
                QToolButton:hover {{
                    background: {HOVER_BG};
                }}
                """
            )
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(
                lambda checked, b=btn: log_debug(
                    f"Button clicked: {b.text().replace(chr(10), ' ')}"
                )
            )
            if btn is self.btn_thoat:
                btn.clicked.connect(lambda checked: sys.exit(0))
            btn.setVisible(False)  # Ẩn tất cả nút khi khởi tạo
            self.hbox.addWidget(btn)
        # self.hbox.addStretch()  # Bỏ stretch để tránh layout chiếm hết không gian khi không có nút
