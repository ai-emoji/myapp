import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from repository.department_repository import DepartmentRepository


class DepartmentService:
    def __init__(self):
        self.repo = DepartmentRepository()

    def get_all_departments(self):
        return self.repo.get_all()

    def get_hierarchy(self):
        return self.repo.get_hierarchy_flat()

    def get_department_by_id(self, dep_id):
        return self.repo.get_by_id(dep_id)

    def add_department(self, name, parent_id=None):
        # Không cho phép trùng tên ở mọi cấp
        all_items = self.repo.get_all()
        for it in all_items:
            if it["name"].strip().lower() == name.strip().lower():
                log_to_debug(f"DepartmentService: Trùng tên phòng ban '{name}'")
                return False
        return self.repo.add(name, parent_id)

    def update_department(self, dep_id, name, parent_id=None):
        # Không cho phép trùng tên ở mọi cấp (trừ chính nó)
        all_items = self.repo.get_all()
        for it in all_items:
            if (
                it["id"] != dep_id
                and it["name"].strip().lower() == name.strip().lower()
            ):
                log_to_debug(f"DepartmentService: Trùng tên phòng ban '{name}'")
                return False
        return self.repo.update(dep_id, name, parent_id)

    def delete_department(self, dep_id):
        # Không cho phép xóa nếu có phòng ban con
        try:
            if self.repo.has_children(dep_id):
                log_to_debug(
                    f"DepartmentService: Không cho phép xóa ID {dep_id} vì có phòng ban con"
                )
                return False
            return self.repo.delete(dep_id)
        except Exception as e:
            log_to_debug(
                f"DepartmentService: delete_department() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def count(self):
        return self.repo.count()
