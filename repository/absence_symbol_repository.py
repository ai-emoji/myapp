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


class AbsenceSymbolRepository:
    def __init__(self):
        self.db_path = Database.get_db_path()

    def get_all(self):
        """Lấy tất cả ký hiệu loại vắng"""
        try:
            log_to_debug("AbsenceSymbolRepository: get_all() called")
            con = duckdb.connect(self.db_path, read_only=True)
            result = con.execute(
                """
                SELECT id, code, description, symbol, is_used, is_paid
                FROM absence_symbol
                ORDER BY code
                """
            ).fetchall()
            con.close()

            symbols = []
            for row in result:
                symbols.append(
                    {
                        "id": row[0],
                        "code": row[1],
                        "description": row[2],
                        "symbol": row[3],
                        "is_used": row[4],
                        "is_paid": row[5],
                    }
                )

            log_to_debug(
                f"AbsenceSymbolRepository: get_all() returned {len(symbols)} symbols"
            )
            return symbols
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolRepository: get_all() error: {e}\n{traceback.format_exc()}"
            )
            return []

    def update(self, symbol_id, code, description, symbol, is_used, is_paid):
        """Cập nhật ký hiệu loại vắng"""
        try:
            log_to_debug(f"AbsenceSymbolRepository: update() called for id={symbol_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                UPDATE absence_symbol
                SET code = ?,
                    description = ?,
                    symbol = ?,
                    is_used = ?,
                    is_paid = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                [code, description, symbol, is_used, is_paid, symbol_id],
            )
            con.commit()
            con.close()
            log_to_debug(
                f"AbsenceSymbolRepository: update() success for id={symbol_id}"
            )
            return True
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolRepository: update() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def add(self, code, description, symbol, is_used, is_paid):
        """Thêm ký hiệu loại vắng mới"""
        try:
            log_to_debug("AbsenceSymbolRepository: add() called")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute(
                """
                INSERT INTO absence_symbol (code, description, symbol, is_used, is_paid)
                VALUES (?, ?, ?, ?, ?)
                """,
                [code, description, symbol, is_used, is_paid],
            )
            con.commit()
            con.close()
            log_to_debug("AbsenceSymbolRepository: add() success")
            return True
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolRepository: add() error: {e}\n{traceback.format_exc()}"
            )
            return False

    def delete(self, symbol_id):
        """Xóa ký hiệu loại vắng"""
        try:
            log_to_debug(f"AbsenceSymbolRepository: delete() called for id={symbol_id}")
            con = duckdb.connect(self.db_path, read_only=False)
            con.execute("DELETE FROM absence_symbol WHERE id = ?", [symbol_id])
            con.commit()
            con.close()
            log_to_debug(
                f"AbsenceSymbolRepository: delete() success for id={symbol_id}"
            )
            return True
        except Exception as e:
            log_to_debug(
                f"AbsenceSymbolRepository: delete() error: {e}\n{traceback.format_exc()}"
            )
            return False
