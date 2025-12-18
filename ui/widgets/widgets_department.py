import logging

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QFrame,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from core.resource import (
    DEPARTMENT_SVG,
    FONT_WEIGHT_SEMIBOLD,
    DEPARTMENT_HEADER_BG,
    DEPARTMENT_MAIN_BG,
    TOTAL_SVG,
    DEPARTMENT_MIN_WIDTH,
    DEPARTMENT_MIN_HEIGHT,
    DEPARTMENT_HEADER_HEIGHT,
    DEPARTMENT_MAIN_1_HEIGHT,
    DEPARTMENT_MAIN_2_HEIGHT,
    ADD_SVG,
    EDIT_SVG,
    DELETE_SVG,
    DEPARTMENT_ROW_HEIGHT,
    ACTIVE,
    HOVER_ROW,
)

# Cấu hình logging
logging.basicConfig(
    filename="log/debug.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
logging.info("WidgetsDepartment: Initializing widget")


class WidgetsDepartment(QWidget):
    """Widget khai báo phòng ban gồm 3 phần: header, actions, main split"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Đồng bộ kích thước tối thiểu như Job Title
        self.setMinimumWidth(DEPARTMENT_MIN_WIDTH)
        self.setMinimumHeight(DEPARTMENT_MIN_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Phần 1: Ảnh + tiêu đề (giống WidgetsJobTitleHeader)
        header = QFrame()
        header.setAttribute(Qt.WA_StyledBackground, True)
        header.setStyleSheet(f"background: {DEPARTMENT_HEADER_BG};")
        header.setFixedHeight(DEPARTMENT_HEADER_HEIGHT)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 0, 0)
        header_layout.setSpacing(8)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(DEPARTMENT_SVG).pixmap(20, 20))
        title_label = QLabel("Khai báo phòng ban")
        title_label.setStyleSheet(
            f"font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222;"
        )
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        main_layout.addWidget(header, 0)

        # Phần 2: Thêm/Sửa/Xóa + Tổng
        actions = QFrame()
        actions.setAttribute(Qt.WA_StyledBackground, True)
        actions.setStyleSheet(
            f"""
            background: {DEPARTMENT_MAIN_BG};
            border-bottom: 1px solid #e0e0e0;
            """
        )
        actions.setFixedHeight(DEPARTMENT_MAIN_1_HEIGHT)
        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(16, 0, 0, 0)
        actions_layout.setSpacing(8)

        self.btn_add = QPushButton(QIcon(ADD_SVG), "Thêm mới")
        self.btn_edit = QPushButton(QIcon(EDIT_SVG), "Sửa đổi")
        self.btn_delete = QPushButton(QIcon(DELETE_SVG), "Xóa")
        for b in (self.btn_add, self.btn_edit, self.btn_delete):
            b.setFixedSize(100, 36)
            b.setIconSize(QSize(20, 20))
            b.setStyleSheet("border: none; font-size: 14px;")
            b.setCursor(Qt.PointingHandCursor)

        # Tổng (thêm ảnh giống WidgetsJobTitle)
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

        actions_layout.addWidget(self.btn_add)
        actions_layout.addWidget(self.btn_edit)
        actions_layout.addWidget(self.btn_delete)
        actions_layout.addLayout(total_container)
        actions_layout.addStretch(1)
        main_layout.addWidget(actions, 0)

        # Phần 3: Chia 2 phần (trái cây, phải ghi chú)
        content = QFrame()
        content.setAttribute(Qt.WA_StyledBackground, True)
        content.setStyleSheet(f"background: {DEPARTMENT_MAIN_BG};")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(12, 8, 12, 8)
        content_layout.setSpacing(12)

        # Trái: Filter + cây phòng ban nhiều cấp
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        filter_container = QFrame()
        filter_container.setFrameShape(QFrame.NoFrame)
        filter_container.setStyleSheet(
            "border-bottom: 1px solid #e0e0e0; padding-bottom: 4px;"
        )
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(8)

        filter_label = QLabel("Lọc Phòng Ban")
        filter_label.setStyleSheet("border: none;")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Nhập tên để lọc…")
        self.filter_input.setStyleSheet(
            """
            border: 1px solid #000;
            border-radius: 4px;
            """
        )
        self.filter_input.setFixedWidth(300)
        self.filter_input.setFixedHeight(36)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addStretch(1)

        left_layout.addWidget(filter_container)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)
        self.tree.setAnimated(True)
        self.tree.setIndentation(0)
        self.tree.setRootIsDecorated(False)
        self.tree.setFocusPolicy(Qt.NoFocus)
        self.tree.setIconSize(QSize(16, 16))
        # Tăng chiều cao row, hover/selected theo biến
        self.tree.setStyleSheet(
            f"""
            QTreeView {{
                background: white;
                color: black;
                border: 1px solid #e0e0e0;
            }}
            QTreeView::item {{
                height: {DEPARTMENT_ROW_HEIGHT}px;
                font-family: Consolas, 'Courier New', monospace;
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
        left_layout.addWidget(self.tree, 1)
        content_layout.addWidget(left_panel, 2)

        # Phải: ghi chú hướng dẫn
        self.notes = QLabel(
            "- Chọn phòng ban để sửa hoặc xóa.\n"
            "- Tên phòng ban không được trùng ở bất kỳ cấp nào.\n"
            "- Dấu '------' thể hiện cấp độ (cấp càng sâu càng nhiều dấu)."
        )
        self.notes.setWordWrap(True)
        # Thêm border trái cho notes
        self.notes.setStyleSheet("border-left: 2px solid #e0e0e0; padding-left: 12px;")
        content_layout.addWidget(self.notes, 1)
        main_layout.addWidget(content, 1)

        # Kết nối sự kiện
        self._connect_actions()
        self._load_data()
        self.filter_input.textChanged.connect(self._apply_filter)

    def _connect_actions(self):
        from ui.dialog.dialog_department import (
            DialogDepartmentAdd,
            DialogDepartmentEdit,
            DialogDepartmentDelete,
        )
        from services.department_services import DepartmentService

        self.service = DepartmentService()

        def on_add():
            # Lấy node đang chọn làm phòng ban cha mặc định
            default_parent_id = None
            cur = self.tree.currentItem()
            if cur:
                default_parent_id = cur.data(0, Qt.UserRole)
            dlg = DialogDepartmentAdd(self, default_parent_id=default_parent_id)
            if dlg.exec():
                self._load_data()

        def on_edit():
            item = self.tree.currentItem()
            if not item:
                return
            dep_id = item.data(0, Qt.UserRole)
            suggested_parent_id = item.data(0, Qt.UserRole + 2)
            dlg = DialogDepartmentEdit(
                self, dep_id=dep_id, suggested_parent_id=suggested_parent_id
            )
            if dlg.exec():
                self._load_data()

        def on_delete():
            item = self.tree.currentItem()
            if not item:
                return
            dep_id = item.data(0, Qt.UserRole)
            # Sử dụng tên thuần không có prefix ASCII
            dep_name = item.data(0, Qt.UserRole + 1) or item.text(0)
            dlg = DialogDepartmentDelete(self, dep_id=dep_id, dep_name=dep_name)
            if dlg.exec():
                self._load_data()

        self.btn_add.clicked.connect(on_add)
        self.btn_edit.clicked.connect(on_edit)
        self.btn_delete.clicked.connect(on_delete)

    def _load_data(self):
        try:
            self.tree.clear()
            flat = self.service.get_all_departments()
            # Map cha->con
            by_parent = {}
            for n in flat:
                by_parent.setdefault(n["parent_id"], []).append(n)

            def build(parent_item, parent_id, prefix=""):
                children = sorted(
                    by_parent.get(parent_id, []), key=lambda x: x["name"].lower()
                )
                last_index = len(children) - 1
                for idx, node in enumerate(children):
                    is_last = idx == last_index
                    branch = "└─" if is_last else "├─"
                    connector = "│" if not is_last else " "
                    # Kết hợp ASCII prefix và tên trong 1 cột
                    display_text = f"{prefix}{branch} {node['name']}"
                    item = QTreeWidgetItem([display_text])
                    item.setIcon(0, QIcon(DEPARTMENT_SVG))
                    item.setData(0, Qt.UserRole, node["id"])
                    item.setData(0, Qt.UserRole + 1, node["name"])
                    item.setData(0, Qt.UserRole + 2, parent_id)
                    if parent_item is None:
                        self.tree.addTopLevelItem(item)
                    else:
                        parent_item.addChild(item)
                    # Cập nhật prefix cho con
                    child_prefix = f"{prefix}{connector}   "
                    build(item, node["id"], child_prefix)

            # Hiển thị root cũng theo dạng nhánh
            build(None, None, "")
            self.tree.expandAll()
            self.lbl_total.setText(f"Tổng: {self.service.count()}")
        except Exception:
            pass

    def _apply_filter(self, text: str):
        # Ẩn/hiện node theo từ khóa, giữ lại các nhánh có khớp ở con
        keyword = (text or "").strip().lower()

        def match_or_descendant(item):
            # So sánh theo tên thuần, bỏ prefix ASCII
            raw_name = item.data(0, Qt.UserRole + 1) or item.text(0)
            name = str(raw_name).lower()
            matched = keyword in name if keyword else True
            # Kiểm tra con
            child_match = False
            for i in range(item.childCount()):
                if match_or_descendant(item.child(i)):
                    child_match = True
            item.setHidden(not (matched or child_match))
            if matched or child_match:
                self.tree.expandItem(item)
            return matched or child_match

        for i in range(self.tree.topLevelItemCount()):
            match_or_descendant(self.tree.topLevelItem(i))
