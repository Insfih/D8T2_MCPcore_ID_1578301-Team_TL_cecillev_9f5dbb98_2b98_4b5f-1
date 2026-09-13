"""SQLite. Методы записи вызываются после проверки правил."""
import sqlite3
import uuid
from pathlib import Path

class Storage:
    def __init__(self, db_path, seed_path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        is_new = not self.path.exists()
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        if is_new:
            self.connection.executescript(Path(seed_path).read_text(encoding="utf-8"))
            self.connection.commit()

    def close(self):
        self.connection.close()

    def get_product(self, product_id):
        row = self.connection.execute(
            "SELECT id, name, price_coins, user_limit FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        if row is None:
            return None
        product = dict(row)
        rows = self.connection.execute(
            "SELECT size, quantity FROM stock WHERE product_id = ? ORDER BY size",
            (product_id,),
        ).fetchall()
        product["stock"] = {r["size"]: r["quantity"] for r in rows}
        return product

    def list_products(self):
        'Список товаров в порядке id.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("list_products")

    def get_user(self, user_id):
        'Словарь id, coins или None. Чтение не создаёт пользователя.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("get_user")

    def get_order(self, order_id):
        'Словарь со всеми полями orders или None.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("get_order")

    def count_owned(self, user_id, product_id):
        'Число единиц товара в created и picked_up, по всем размерам.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("count_owned")

    def create_order(self, user_id, product_id, size, quantity, total_price):
        'Записать заказ, баланс и остаток одной транзакцией. Вернуть заказ.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("create_order")

    def cancel_order(self, order, refund):
        'Вернуть переданную сумму и товар, поменять статус одной транзакцией.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("cancel_order")

    def confirm_pickup(self, order_id):
        'Изменить только статус. Баланс и остаток уже уменьшены при покупке.'
        # TODO: закончите эту функцию.
        raise NotImplementedError("confirm_pickup")

