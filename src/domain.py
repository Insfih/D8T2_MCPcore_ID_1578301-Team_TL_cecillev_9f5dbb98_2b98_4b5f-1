"""Правила без SQL и MCP. Вся арифметика в целых коинах."""

def calculate_total(price: int, quantity: int) -> int:
    'Стоимость заказа.'
    iTotalPrice = price * quantity
    return iTotalPrice

def purchase_error(product: dict, size: str, quantity: int, balance: int, already_owned: int, total: int):
    """Код отказа или None. Пользователь и товар уже найдены.

    product       — товар из storage.get_product: price_coins, user_limit, stock {размер: остаток}
    size          — размер: "S", "M", "L", "XL" или "one_size"
    quantity      — сколько единиц в этом заказе
    balance       — коины участника
    already_owned — сколько единиц товара у участника уже есть (created и picked_up, все размеры)
    total         — стоимость этого заказа из calculate_total
    """
    dStock = product["stock"]
    # 3. Размер есть и остатка хватает
    if size not in dStock or dStock[size] < quantity:
        return "OUT_OF_STOCK"
    # 4. Лимит на участника с учётом прежних заказов
    if already_owned + quantity > product["user_limit"]:
        return "USER_LIMIT_EXCEEDED"
    # 5. Коинов хватает на всю стоимость
    if balance < total:
        return "INSUFFICIENT_COINS"
    return None

def refund_amount(total_price: int) -> int:
    'Сумма возврата по сохранённой стоимости заказа.'
    return total_price

def can_cancel(order: dict) -> bool:
    'Можно ли отменить найденный заказ.'
    sStatus = order["status"]
    return sStatus == 'created'

def can_pickup(order: dict) -> bool:
    'Можно ли выдать найденный заказ.'
    sStatus = order["status"]
    return sStatus == 'created'