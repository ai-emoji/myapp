from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from core.resource import (
    EMPLOYEE_SVG,
    FONT_WEIGHT_SEMIBOLD,
    EMPLOYEE_HEADER_BG,
    EMPLOYEE_MAIN_BG,
    TOTAL_SVG,
    EMPLOYEE_MIN_WIDTH,
    EMPLOYEE_MIN_HEIGHT,
    EMPLOYEE_HEADER_HEIGHT,
    EMPLOYEE_MAIN_1_HEIGHT,
    EMPLOYEE_MAIN_2_HEIGHT,
    EMPLOYEE_LEFT_PANEL_WIDTH,
    EMPLOYEE_ROW_HEIGHT,
    ADD_SVG,
    EDIT_SVG,
    DELETE_SVG,
    REFRESH_SVG,
    ACTIVE,
    HOVER_ROW,
    DEPARTMENT_SVG,
    EMPLOYEE_SEARCH_HEIGHT,
    ODD_ROW_BG,
    EVEN_ROW_BG,
)


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


class WidgetsEmployee(QWidget):
    """Widget khai báo nhân viên gồm 3 phần: header, left panel (cây phòng ban), right panel"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Đồng bộ kích thước tối thiểu
        self.setMinimumWidth(EMPLOYEE_MIN_WIDTH)
        self.setMinimumHeight(EMPLOYEE_MIN_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Phần 1: Header (Ảnh + tiêu đề)
        header = QFrame()
        header.setAttribute(Qt.WA_StyledBackground, True)
        header.setStyleSheet(f"background: {EMPLOYEE_HEADER_BG};")
        header.setFixedHeight(EMPLOYEE_HEADER_HEIGHT)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 0, 0)
        header_layout.setSpacing(0)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(EMPLOYEE_SVG).pixmap(20, 20))
        title_label = QLabel("Khai báo nhân viên")
        title_label.setStyleSheet(
            f"font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222;"
        )
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        main_layout.addWidget(header, 0)

        # Phần 2 & 3: Content (Left panel + Right panel)
        content = QFrame()
        content.setAttribute(Qt.WA_StyledBackground, True)
        content.setStyleSheet(f"background: {EMPLOYEE_MAIN_BG};")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left Panel: Cây phòng ban nhiều cấp
        left_panel = QFrame()
        left_panel.setAttribute(Qt.WA_StyledBackground, True)
        left_panel.setStyleSheet(
            "border-right: 1px solid #e0e0e0; padding: 0px; margin: 0px;"
        )
        left_panel.setFixedWidth(EMPLOYEE_LEFT_PANEL_WIDTH)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(16, 8, 0, 8)
        left_layout.setSpacing(8)

        left_label = QLabel("Phòng Ban")
        left_label.setStyleSheet(
            f"font-size: 14px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222; border:none; padding:0; margin:0;"
        )
        left_layout.addWidget(left_label)

        self.tree_departments = QTreeWidget()
        self.tree_departments.setHeaderHidden(True)
        self.tree_departments.setColumnCount(1)
        self.tree_departments.setAnimated(True)
        self.tree_departments.setIndentation(0)
        self.tree_departments.setRootIsDecorated(False)
        self.tree_departments.setFocusPolicy(Qt.NoFocus)
        self.tree_departments.setIconSize(QSize(16, 16))
        self.tree_departments.setStyleSheet(
            f"""
            QTreeView {{
                background: white;
                color: black;
                border: 1px solid #e0e0e0;
            }}
            QTreeView::item {{
                height: {EMPLOYEE_ROW_HEIGHT}px;
                font-family: Segoe UI, Inter, Roboto;
                font-size: 13px;
                padding-left: 8px;
            }}
            QTreeView::item:hover {{
                background: {HOVER_ROW};
            }}
            QTreeView::item:selected {{
                background: {ACTIVE};
                color: black;
            }}
            """
        )
        left_layout.addWidget(self.tree_departments, 1)
        content_layout.addWidget(left_panel, 0)

        # Right Panel: Header + Main
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Right Header: Buttons + Search + Total
        right_header = QFrame()
        right_header.setAttribute(Qt.WA_StyledBackground, True)
        right_header.setStyleSheet(
            f"background: {EMPLOYEE_MAIN_BG}; border-bottom: 1px solid #e0e0e0;"
        )
        right_header.setFixedHeight(EMPLOYEE_MAIN_1_HEIGHT)
        right_header_layout = QHBoxLayout(right_header)
        right_header_layout.setContentsMargins(8, 0, 8, 0)
        right_header_layout.setSpacing(8)

        self.btn_add = QPushButton(QIcon(ADD_SVG), "Thêm mới")
        self.btn_edit = QPushButton(QIcon(EDIT_SVG), "Sửa đổi")
        self.btn_delete = QPushButton(QIcon(DELETE_SVG), "Xóa")
        self.btn_refresh = QPushButton(QIcon(REFRESH_SVG), "Làm mới")
        for b in (self.btn_add, self.btn_edit, self.btn_delete, self.btn_refresh):
            b.setFixedSize(100, 36)
            b.setIconSize(QSize(20, 20))
            b.setStyleSheet("border: none; font-size: 14px;")
            b.setCursor(Qt.PointingHandCursor)

        # Search Input with Filter
        search_container = QHBoxLayout()
        search_container.setContentsMargins(0, 0, 0, 0)
        search_container.setSpacing(4)

        self.search_filter = QComboBox()
        self.search_filter.addItems(
            ["Tất cả", "Mã NV", "Tên NV", "Phòng ban", "Chức vụ"]
        )
        self.search_filter.setFixedHeight(30)
        self.search_filter.setFixedWidth(120)
        self.search_filter.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                background: white;
            }
            QComboBox:focus {
                border: 1px solid #2C3E50;
            }
        """
        )

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm nhân viên…")
        self.search_input.setFixedHeight(EMPLOYEE_SEARCH_HEIGHT)
        self.search_input.setMinimumWidth(280)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 0 8px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #2C3E50;
            }
        """
        )

        search_container.addWidget(self.search_filter)
        search_container.addWidget(self.search_input)

        # Total
        total_container = QHBoxLayout()
        total_container.setContentsMargins(0, 0, 0, 0)
        total_container.setSpacing(4)
        total_icon_label = QLabel()
        total_icon = QIcon(TOTAL_SVG)
        total_icon_label.setPixmap(total_icon.pixmap(16, 16))
        total_container.addWidget(total_icon_label)
        self.lbl_total = QLabel("Tổng: 0")
        self.lbl_total.setStyleSheet(
            "font-size: 14px; color: #1976d2; font-weight: bold;"
        )
        total_container.addWidget(self.lbl_total)

        right_header_layout.addWidget(self.btn_add)
        right_header_layout.addWidget(self.btn_edit)
        right_header_layout.addWidget(self.btn_delete)
        right_header_layout.addWidget(self.btn_refresh)
        right_header_layout.addLayout(search_container)
        right_header_layout.addLayout(total_container)
        right_header_layout.addStretch(1)
        right_layout.addWidget(right_header, 0)

        # Right Main: Bảng nhân viên
        right_main = QFrame()
        right_main.setAttribute(Qt.WA_StyledBackground, True)
        right_main.setStyleSheet(f"background: white;")
        right_main_layout = QVBoxLayout(right_main)
        right_main_layout.setContentsMargins(8, 8, 8, 8)
        right_main_layout.setSpacing(8)

        # Container cho bảng (2 bảng side by side)
        table_container = QFrame()
        table_container.setStyleSheet("background: white;")
        table_container_layout = QHBoxLayout(table_container)
        table_container_layout.setContentsMargins(0, 0, 0, 0)
        table_container_layout.setSpacing(0)

        # Bảng 1: 2 cột đầu (Mã NV, Tên Nhân Viên) - FROZEN
        self.table_frozen = QTableWidget()
        self.table_frozen.setColumnCount(2)
        self.table_frozen.setHorizontalHeaderLabels(["Mã NV", "Tên Nhân Viên"])
        self.table_frozen.setStyleSheet(
            f"""
            QTableWidget {{
                background: {EVEN_ROW_BG};
                gridline-color: #d0d0d0;
                alternate-background-color: {ODD_ROW_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
            QTableWidget::item {{
                padding: 4px;
                border-bottom: 1px solid #d0d0d0;
                margin: 0px;
            }}
            QTableWidget::item:selected {{
                background: {ACTIVE};
                color: #000;
                font-weight: {FONT_WEIGHT_SEMIBOLD};
            }}
            QHeaderView::section {{
                background: {EMPLOYEE_HEADER_BG};
                color: #222;
                padding: 4px;
                margin: 0px;
                border: none;
                border-bottom: 1px solid #999;
                font-weight: bold;
            }}
            """
        )
        self.table_frozen.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_frozen.setSelectionMode(QTableWidget.SingleSelection)
        self.table_frozen.setAlternatingRowColors(True)
        self.table_frozen.setShowGrid(True)
        self.table_frozen.setFocusPolicy(Qt.NoFocus)
        self.table_frozen.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_frozen.verticalHeader().setVisible(False)
        self.table_frozen.setColumnWidth(0, 80)
        self.table_frozen.setColumnWidth(1, 150)
        self.table_frozen.horizontalHeader().setStretchLastSection(False)
        self.table_frozen.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_frozen.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_frozen.setContentsMargins(0, 0, 0, 0)
        self.table_frozen.setFrameStyle(QTableWidget.NoFrame)
        # Giữ kích thước cố định khớp 2 cột để sát bảng bên cạnh
        self.table_frozen.setFixedWidth(230)
        self.table_frozen.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        table_container_layout.addWidget(self.table_frozen, 0)

        # Bảng 2: Các cột còn lại (scrollable)
        self.table_scrollable = QTableWidget()
        self.table_scrollable.setColumnCount(18)  # 20 - 2 frozen columns
        self.table_scrollable.setHorizontalHeaderLabels(
            [
                "Phòng Ban",
                "Chức Vụ",
                "Giới Tính",
                "Ngày Vào",
                "Mã Chấm Công",
                "Tên Chấm Công",
                "Ngày Sinh",
                "Nơi Sinh",
                "Nguyên Quán",
                "Số CMND/CCCD",
                "Nơi Cấp",
                "Dân Tộc",
                "Quốc Tịch",
                "Địa Chỉ Hiện Tại",
                "Số ĐT",
                "Người Liên Hệ",
                "ID",
                "Dept ID",
            ]
        )
        self.table_scrollable.setStyleSheet(
            f"""
            QTableWidget {{
                background: {EVEN_ROW_BG};
                gridline-color: #d0d0d0;
                alternate-background-color: {ODD_ROW_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
            QTableWidget::item {{
                padding: 4px;
                border-bottom: 1px solid #d0d0d0;
                margin: 0px;
            }}
            QTableWidget::item:selected {{
                background: {ACTIVE};
                color: #000;
                font-weight: {FONT_WEIGHT_SEMIBOLD};
            }}
            QHeaderView::section {{
                background: {EMPLOYEE_HEADER_BG};
                color: #222;
                padding: 4px;
                margin: 0px;
                border: none;
                border-bottom: 1px solid #999;
                font-weight: bold;
            }}
            """
        )
        self.table_scrollable.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_scrollable.setSelectionMode(QTableWidget.SingleSelection)
        self.table_scrollable.setAlternatingRowColors(True)
        self.table_scrollable.setShowGrid(True)
        self.table_scrollable.setFocusPolicy(Qt.NoFocus)
        self.table_scrollable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_scrollable.verticalHeader().setVisible(False)
        self.table_scrollable.setContentsMargins(0, 0, 0, 0)
        self.table_scrollable.setFrameStyle(QTableWidget.NoFrame)
        self.table_scrollable.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        # Set column widths (cố định) để khi cửa sổ hẹp sẽ xuất hiện thanh cuộn ngang, tránh dồn chữ
        col_widths_scrollable = {
            0: 120,  # Phòng Ban
            1: 100,  # Chức Vụ
            2: 90,  # Giới Tính
            3: 100,  # Ngày Vào
            4: 100,  # Mã Chấm Công
            5: 120,  # Tên Chấm Công
            6: 100,  # Ngày Sinh
            7: 100,  # Nơi Sinh
            8: 100,  # Nguyên Quán
            9: 110,  # Số CMND/CCCD
            10: 100,  # Nơi Cấp
            11: 80,  # Dân Tộc
            12: 90,  # Quốc Tịch
            13: 150,  # Địa Chỉ Hiện Tại
            14: 100,  # Số ĐT
            15: 120,  # Người Liên Hệ
            16: 50,  # ID
        }

        header_scrollable = self.table_scrollable.horizontalHeader()
        header_scrollable.setStretchLastSection(True)
        header_scrollable.setSectionsMovable(False)

        for col, width in col_widths_scrollable.items():
            self.table_scrollable.setColumnWidth(col, width)
            # Cho phép người dùng kéo giãn các cột (tránh ríu chữ, vẫn có scrollbar khi hẹp)
            header_scrollable.setSectionResizeMode(col, QHeaderView.Interactive)

        # Ẩn cột ID
        self.table_scrollable.setColumnHidden(16, True)  # Ẩn cột ID
        self.table_scrollable.setColumnHidden(17, True)  # Ẩn cột Dept ID
        header_scrollable.setSectionResizeMode(16, QHeaderView.Fixed)

        # Hiển thị thanh cuộn ngang khi thu nhỏ cửa sổ
        self.table_scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_container_layout.addWidget(self.table_scrollable, 1)

        # Tạo 50 dòng trống ban đầu cho cả 2 bảng
        self.table_frozen.setRowCount(50)
        self.table_scrollable.setRowCount(50)
        for i in range(50):
            # Bảng frozen: 2 cột
            self.table_frozen.setItem(i, 0, QTableWidgetItem(""))
            self.table_frozen.setItem(i, 1, QTableWidgetItem(""))

            # Bảng scrollable: 17 cột
            for col in range(17):
                self.table_scrollable.setItem(i, col, QTableWidgetItem(""))

        right_main_layout.addWidget(table_container, 1)
        right_layout.addWidget(right_main, 1)

        content_layout.addWidget(right_panel, 1)
        main_layout.addWidget(content, 1)

        # Kết nối scroll horizontal để freeze 2 cột đầu
        self.table_scrollable.horizontalScrollBar().valueChanged.connect(
            self._on_horizontal_scroll
        )
        # Đồng bộ selection giữa 2 bảng
        self.table_frozen.selectionModel().selectionChanged.connect(
            self._sync_selection_to_scrollable
        )
        self.table_scrollable.selectionModel().selectionChanged.connect(
            self._sync_selection_to_frozen
        )
        # Double-click để mở dialog sửa
        self.table_frozen.cellDoubleClicked.connect(self._on_row_double_clicked)
        self.table_scrollable.cellDoubleClicked.connect(self._on_row_double_clicked)

        # Kết nối sự kiện
        self._connect_actions()
        self._load_data()

    def _sync_selection_to_scrollable(self):
        """Đồng bộ selection từ bảng frozen sang bảng scrollable"""
        frozen_selection = self.table_frozen.selectionModel().selectedRows()
        if frozen_selection:
            row = frozen_selection[0].row()
            self.table_scrollable.selectRow(row)

    def _sync_selection_to_frozen(self):
        """Đồng bộ selection từ bảng scrollable sang bảng frozen"""
        scrollable_selection = self.table_scrollable.selectionModel().selectedRows()
        if scrollable_selection:
            row = scrollable_selection[0].row()
            self.table_frozen.selectRow(row)

    def _sync_vertical_scroll(self, value):
        """Đồng bộ scroll ngang giữa 2 bảng"""
        self.table_frozen.verticalScrollBar().setValue(value)
        self.table_scrollable.verticalScrollBar().setValue(value)

    def _connect_actions(self):
        """Kết nối các sự kiện nút bấm"""
        from services.employee_services import EmployeeService
        from services.department_services import DepartmentService
        from services.job_title_services import JobTitleService
        from ui.controllers.controllers_employee import ControllersEmployee

        self.employee_service = EmployeeService()
        self.department_service = DepartmentService()
        self.job_title_service = JobTitleService()

        # Khởi tạo controller
        self.controller = ControllersEmployee(self)

        self.btn_add.clicked.connect(self.controller.on_add)
        self.btn_edit.clicked.connect(self.controller.on_edit)
        self.btn_delete.clicked.connect(self.controller.on_delete)
        self.btn_refresh.clicked.connect(self.controller.on_refresh)
        self.search_input.textChanged.connect(self.controller.on_search)
        self.search_filter.currentTextChanged.connect(
            lambda: self.controller.on_search(self.search_input.text())
        )
        self.tree_departments.itemClicked.connect(self.controller.on_department_clicked)

        # Đồng bộ vertical scroll giữa 2 bảng
        self.table_frozen.verticalScrollBar().valueChanged.connect(
            self._sync_vertical_scroll
        )
        self.table_scrollable.verticalScrollBar().valueChanged.connect(
            self._sync_vertical_scroll
        )

    def _load_data(self):
        """Load dữ liệu phòng ban từ database"""
        try:
            self.tree_departments.clear()
            self.table_frozen.setRowCount(0)
            self.table_scrollable.setRowCount(0)

            # Load cây phòng ban
            hierarchy = self.department_service.get_hierarchy()

            def build(parent_item, parent_id, prefix=""):
                children = [h for h in hierarchy if h.get("parent_id") == parent_id]
                children_sorted = sorted(children, key=lambda x: x["name"].lower())

                last_index = len(children_sorted) - 1
                for idx, node in enumerate(children_sorted):
                    is_last = idx == last_index
                    branch = "└─" if is_last else "├─"
                    connector = "│" if not is_last else " "

                    display_text = f"{prefix}{branch} {node['name']}"
                    item = QTreeWidgetItem([display_text])
                    item.setIcon(0, QIcon(DEPARTMENT_SVG))
                    item.setData(0, Qt.UserRole, node["id"])
                    item.setData(0, Qt.UserRole + 1, node["name"])

                    if parent_item is None:
                        self.tree_departments.addTopLevelItem(item)
                    else:
                        parent_item.addChild(item)

                    child_prefix = f"{prefix}{connector}   "
                    build(item, node["id"], child_prefix)

            build(None, None, "")
            self.tree_departments.expandAll()

            # Load bảng nhân viên
            employees = self.employee_service.get_all_employees()

            # Lấy thông tin phòng ban và chức vụ
            departments_map = {h["id"]: h["name"] for h in hierarchy}
            job_titles = self.job_title_service.get_all_job_titles()
            job_titles_map = {jt["id"]: jt["name"] for jt in job_titles}

            # Đảm bảo luôn có tối thiểu 50 dòng
            row_count = max(50, len(employees))
            self.table_frozen.setRowCount(row_count)
            self.table_scrollable.setRowCount(row_count)

            # Xóa toàn bộ dữ liệu cũ
            for i in range(row_count):
                self.table_frozen.setItem(i, 0, QTableWidgetItem(""))
                self.table_frozen.setItem(i, 1, QTableWidgetItem(""))
                for col in range(18):
                    self.table_scrollable.setItem(i, col, QTableWidgetItem(""))

            for row, emp in enumerate(employees):
                # === BẢNG FROZEN (2 cột đầu) ===
                # Mã NV
                self.table_frozen.setItem(
                    row, 0, QTableWidgetItem(emp.get("employee_code", "") or "")
                )
                # Tên Nhân Viên
                self.table_frozen.setItem(row, 1, QTableWidgetItem(emp.get("name", "")))

                # === BẢNG SCROLLABLE (17 cột còn lại) ===
                # Phòng Ban
                dept_name = departments_map.get(emp.get("department_id"), "")
                self.table_scrollable.setItem(row, 0, QTableWidgetItem(dept_name or ""))
                # Chức Vụ
                job_title_name = job_titles_map.get(emp.get("job_title_id"), "")
                self.table_scrollable.setItem(
                    row, 1, QTableWidgetItem(job_title_name or "")
                )
                # Giới Tính
                self.table_scrollable.setItem(
                    row, 2, QTableWidgetItem(str(emp.get("gender", "") or ""))
                )
                # Ngày Vào
                hire_date = emp.get("hire_date", "")
                self.table_scrollable.setItem(
                    row, 3, QTableWidgetItem(str(hire_date) if hire_date else "")
                )
                # Mã Chấm Công
                self.table_scrollable.setItem(
                    row, 4, QTableWidgetItem(str(emp.get("attendance_code", "") or ""))
                )
                # Tên Chấm Công
                self.table_scrollable.setItem(
                    row, 5, QTableWidgetItem(str(emp.get("attendance_name", "") or ""))
                )
                # Ngày Sinh
                date_of_birth = emp.get("date_of_birth", "")
                self.table_scrollable.setItem(
                    row,
                    6,
                    QTableWidgetItem(str(date_of_birth) if date_of_birth else ""),
                )
                # Nơi Sinh
                self.table_scrollable.setItem(
                    row, 7, QTableWidgetItem(str(emp.get("birthplace", "") or ""))
                )
                # Nguyên Quán
                self.table_scrollable.setItem(
                    row, 8, QTableWidgetItem(str(emp.get("hometown", "") or ""))
                )
                # Số CMND/CCCD
                self.table_scrollable.setItem(
                    row, 9, QTableWidgetItem(str(emp.get("id_number", "") or ""))
                )
                # Nơi Cấp
                self.table_scrollable.setItem(
                    row, 10, QTableWidgetItem(str(emp.get("id_place_issued", "") or ""))
                )
                # Dân Tộc
                self.table_scrollable.setItem(
                    row, 11, QTableWidgetItem(str(emp.get("ethnicity", "") or ""))
                )
                # Quốc Tịch
                self.table_scrollable.setItem(
                    row, 12, QTableWidgetItem(str(emp.get("nationality", "") or ""))
                )
                # Địa Chỉ Hiện Tại
                self.table_scrollable.setItem(
                    row, 13, QTableWidgetItem(str(emp.get("current_address", "") or ""))
                )
                # Số ĐT
                self.table_scrollable.setItem(
                    row, 14, QTableWidgetItem(str(emp.get("phone_number", "") or ""))
                )
                # Người Liên Hệ
                self.table_scrollable.setItem(
                    row,
                    15,
                    QTableWidgetItem(str(emp.get("emergency_contact", "") or "")),
                )
                # ID (ẩn nhưng phải có data)
                emp_id = emp.get("id", "")
                self.table_scrollable.setItem(
                    row, 16, QTableWidgetItem(str(emp_id) if emp_id else "")
                )
                # Department ID (ẩn - để lọc)
                dept_id = emp.get("department_id", "")
                self.table_scrollable.setItem(
                    row, 17, QTableWidgetItem(str(dept_id) if dept_id else "")
                )

            # Update total
            total = self.employee_service.count()
            self.lbl_total.setText(f"Tổng: {total}")
        except Exception as e:
            log_to_debug(f"WidgetsEmployee: Error in _load_data: {e}")

    def _apply_search(self, text: str):
        """Tìm kiếm nhân viên (đã được xử lý bởi controller)"""
        pass

    def _on_row_double_clicked(self, row, col):
        """Đúp chuột 2 lần vào hàng để mở dialog sửa"""
        if hasattr(self, "controller"):
            self.controller.on_edit()

    def _on_horizontal_scroll(self, value):
        """Xử lý scroll ngang - bảng frozen vẫn giữ cố định"""
        # Bảng frozen không scroll ngang (setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff))
        # Nên không cần xử lý gì ở đây, scroll được kiểm soát riêng trên table_scrollable
        pass
