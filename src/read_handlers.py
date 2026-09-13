"""Инструменты чтения. Здесь нет SQL."""
from .errors import success, failure

def get_product(storage, product_id):
    product = storage.get_product(product_id)
    if product is None:
        return failure("PRODUCT_NOT_FOUND", "Товар не найден")
    return success(product)

def list_products(storage):
    'Реализуйте по правилам Лавки и согласованным методам.'
    # TODO: закончите эту функцию.
    raise NotImplementedError("list_products")

def get_coin_balance(storage, user_id):
    'Реализуйте по правилам Лавки и согласованным методам.'
    # TODO: закончите эту функцию.
    raise NotImplementedError("get_coin_balance")

def get_order_status(storage, order_id):
    'Реализуйте по правилам Лавки и согласованным методам.'
    # TODO: закончите эту функцию.
    raise NotImplementedError("get_order_status")

