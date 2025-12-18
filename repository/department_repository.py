import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


import duckdb
from core.database import Database


class DepartmentRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()
        self._init_table()

    def _init_table(self):
        """Khởi tạo bảng department nếu chưa tồn tại"""
        try:
            log_to_debug("DepartmentRepository: _init_table() called")
            con = duckdb.connect(self.db_path, read_only=False)

            # Tạo sequence trước
            try:
                con.execute("CREATE SEQUENCE seq_department START 1")
            except Exception:
                pass  # Sequence đã tồn tại

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS department (
                    id INTEGER PRIMARY KEY DEFAULT nextval('seq_department'),
                    name VARCHAR UNIQUE NOT NULL,
                    parent_id INTEGER NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            con.close()
            log_to_debug("DepartmentRepository: Table initialized successfully")
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: _init_table() error: {e}\n{traceback.format_exc()}"
            )

    def get_all(self):
        """Lấy tất cả phòng ban (id, name, parent_id)"""
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                "SELECT id, name, parent_id FROM department ORDER BY id ASC"
            ).fetchall()
            con.close()
            return [{"id": r[0], "name": r[1], "parent_id": r[2]} for r in result]
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def get_by_id(self, dep_id):
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            r = con.execute(
                "SELECT id, name, parent_id FROM department WHERE id=?", [dep_id]
            ).fetchone()
            con.close()
            if r:
                return {"id": r[0], "name": r[1], "parent_id": r[2]}
            return None
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: get_by_id() error: {e}\n{traceback.format_exc()}"
            )
            return None

    def add(self, name, parent_id=None):
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "INSERT INTO department (name, parent_id) VALUES (?, ?)",
                [name, parent_id],
            )
            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: add() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def update(self, dep_id, name, parent_id=None):
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                "UPDATE department SET name=?, parent_id=?, updated_at=now() WHERE id=?",
                [name, parent_id, dep_id],
            )
            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: update() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete(self, dep_id):
        try:
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM department WHERE id=?", [dep_id])

            # Kiểm tra xem còn bản ghi nào không
            count_result = con.execute("SELECT COUNT(*) FROM department").fetchone()
            record_count = count_result[0] if count_result else 0

            # Nếu không còn bản ghi nào, reset sequence bằng cách drop và tạo lại
            if record_count == 0:
                try:
                    con.execute("DROP SEQUENCE seq_department")
                    con.execute("CREATE SEQUENCE seq_department START 1")
                    log_to_debug("DepartmentRepository: Sequence dropped and recreated")
                except Exception as seq_error:
                    log_to_debug(
                        f"DepartmentRepository: Error resetting sequence: {seq_error}"
                    )

            con.close()
            return True
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: delete() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def count(self):
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            r = con.execute("SELECT COUNT(*) FROM department").fetchone()
            con.close()
            return r[0] if r else 0
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: count() error: {e}\n{traceback.format_exc()}"
            )
            return 0

    def has_children(self, dep_id):
        """Kiểm tra phòng ban có phòng ban con không"""
        try:
            con = duckdb.connect(self.db_path, read_only=True)
            r = con.execute(
                "SELECT COUNT(*) FROM department WHERE parent_id = ?",
                [dep_id],
            ).fetchone()
            con.close()
            return (r[0] if r else 0) > 0
        except Exception as e:
            log_to_debug(
                f"DepartmentRepository: has_children() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def get_hierarchy_flat(self):
        """Trả về danh sách phòng ban theo thứ tự cây, có prefix '├─' hoặc '└─' theo cấp"""
        nodes = self.get_all()
        by_parent = {}
        for n in nodes:
            by_parent.setdefault(n["parent_id"], []).append(n)

        result = []

        def dfs(parent_id, level, is_last=False, prefix=""):
            children = sorted(
                by_parent.get(parent_id, []), key=lambda x: x["name"].lower()
            )
            for idx, n in enumerate(children):
                is_last_child = idx == len(children) - 1

                if level == 0:
                    current_prefix = ""
                else:
                    branch = "└─ " if is_last_child else "├─ "
                    current_prefix = prefix + branch

                result.append(
                    {
                        "id": n["id"],
                        "name": n["name"],
                        "display_name": f"{current_prefix}{n['name']}",
                        "parent_id": n["parent_id"],
                        "level": level,
                    }
                )

                if level == 0:
                    next_prefix = ""
                else:
                    next_prefix = prefix + ("    " if is_last_child else "│   ")

                dfs(n["id"], level + 1, is_last_child, next_prefix)

        dfs(None, 0)
        return result
