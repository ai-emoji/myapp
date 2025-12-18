import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


# company_services.py
# Service layer cho thông tin công ty
from repository.company_repository import CompanyRepository


class CompanyService:
    def __init__(self):
        self.repo = CompanyRepository()

    def get_company_info(self):
        log_to_debug("CompanyService: get_company_info() called")
        result = self.repo.get_company_info()
        log_to_debug(f"CompanyService: get_company_info() result: {result}")
        return result

    def update_company_info(self, name, phone, address, logo_path):
        log_to_debug(
            f"CompanyService: update_company_info(name={name}, phone={phone}, address={address}, logo_path={logo_path}) called"
        )
        result = self.repo.update_company_info(name, phone, address, logo_path)
        log_to_debug(f"CompanyService: update_company_info() result: {result}")
        return result
