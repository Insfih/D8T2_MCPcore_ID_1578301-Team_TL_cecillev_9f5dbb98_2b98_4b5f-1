"""Порядок работы с заказом. Правила в domain, SQL в storage."""
from . import domain
from .errors import success, failure

MESSAGES = {
    "OUT_OF_STOCK": "Недостаточно товара этого размера",
    "USER_LIMIT_EXCEEDED": "Превышен лимит этого товара на участника",
    "INSUFFICIENT_COINS": "Недостаточно коинов",
}


def create_order(storage, user_id, product_id, size, quantity):
    'Проверки строго по порядку, запись только после всех проверок.'
    # 1. Пользователь существует
    user = storage.get_user(user_id)
    if user is None:
        return failure("USER_NOT_FOUND", "Пользователь не найден")

    # 2. Товар существует
    product = storage.get_product(product_id)
    if product is None:
        return failure("PRODUCT_NOT_FOUND", "Товар не найден")

    # 3–5. Склад, лимит, коины — правило в domain
    total = domain.calculate_total(product["price_coins"], quantity)
    already_owned = storage.count_owned(user_id, product_id)
    code = domain.purchase_error(product, size, quantity, user["coins"], already_owned, total)
    if code is not None:
        return failure(code, MESSAGES.get(code, "Покупка отклонена"))

    # Заказ, списание коинов и остатка — одной транзакцией в storage
    order = storage.create_order(user_id, product_id, size, quantity, total)
    return success({
        "order_id": order["id"],
        "status": order["status"],
        "total_price": order["total_price"],
    })


def cancel_order(storage, order_id):
    'Отмена только из created; возврат по сохранённой стоимости, ровно один раз.'
    order = storage.get_order(order_id)
    if order is None:
        return failure("ORDER_NOT_FOUND", "Заказ не найден")
    if not domain.can_cancel(order):
        return failure("ORDER_STATUS_ERROR", "Этот заказ нельзя отменить: он уже отменён или выдан")

    refund = domain.refund_amount(order["total_price"])
    storage.cancel_order(order, refund)
    return success({"order_id": order["id"], "status": "cancelled"})


def confirm_pickup(storage, order_id):
    'Выдача только из created; меняется только статус.'
    order = storage.get_order(order_id)
    if order is None:
        return failure("ORDER_NOT_FOUND", "Заказ не найден")
    if not domain.can_pickup(order):
        return failure("ORDER_STATUS_ERROR", "Этот заказ нельзя выдать: он уже выдан или отменён")

    storage.confirm_pickup(order["id"])
    return success({"order_id": order["id"], "status": "picked_up"})
