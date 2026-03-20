import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database.json")


def load_data():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            clients = data["clients"]
            orders = data["orders"]
    else:
        clients = []
        orders = []
        data = {"clients": clients, "orders": orders}
    return clients, orders, data


def save_data(clients, orders):
    data = {"clients": clients, "orders": orders}
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def generate_id(items):
    if len(items) == 0:
        return 1
    else:
        return max(item["id"] for item in items) + 1


def add_client(clients, orders):
    print("Добавление клиента.")
    name = input("Имя: ")
    phone = input("Номер: ")
    email = input("Почта: ")
    client_id = generate_id(clients)
    clients.append({
        "id": client_id,
        "name": name,
        "phone": phone,
        "email": email,
        "orders": []
    })
    save_data(clients, orders)
    print("Клиент добавлен.")


def show_clients(clients):
    if not clients:
        print("Список клиентов пуст.")
        return
    print("-" * 20)
    for client in clients:
        print(f"ID: {client['id']}")
        print(f"Имя: {client['name']}")
        print(f"Телефон: {client['phone']}")
        print(f"Почта: {client['email']}")
        print("-" * 20)


def delete_client(clients, orders):
    if not clients:
        print("Список клиентов пуст.")
        return
    try:
        client_id = int(input("Введите ID клиента для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    client_exists = False
    for client in clients:
        if client["id"] == client_id:
            client_exists = True
            clients.remove(client)
            break
    if not client_exists:
        print(f"Клиент с ID {client_id} не найден.")
        return
    orders[:] = [order for order in orders if order["client_id"] != client_id]
    save_data(clients, orders)
    print("Клиент удален.")


def print_order(order, show_priority=True):
    print(f"ID заказа: {order['id']}")
    print(f"Описание: {order['description']}")
    print(f"Цена: {order['amount']}")
    if show_priority:
        print(f"Приоритет: {order['priority']}")
    print(f"Статус: {order['status']}")
    print(f"Срок выполнения: {order['deadline']}")
    print("-" * 20)


def show_client_orders(clients, orders):
    if not clients:
        print("Список клиентов пуст.")
        return
    try:
        client_id = int(input("Введите ID клиента: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    client = next((client for client in clients if client["id"] == client_id), None)
    if not client:
        print("Клиент не найден.")
        return
    client_orders = [
        order for order in orders if order["client_id"] == client_id and order["status"] not in ["Завершён", "Отменён"]
    ]
    if not client_orders:
        print("У клиента нет активных заказов.")
        return
    client_orders.sort(key=lambda order: order["amount"], reverse=True)
    print(f"\nАктивные заказы клиента {client['name']}:")
    print("-" * 20)
    for order in client_orders:
        print_order(order)


def show_client_order_history(clients, orders):
    if not clients:
        print("Список клиентов пуст.")
        return
    try:
        client_id = int(input("Введите ID клиента: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    client = next((client for client in clients if client["id"] == client_id), None)
    if not client:
        print("Клиент не найден.")
        return
    history_orders = [
        order for order in orders if order["client_id"] == client_id and order["status"] in ["Завершён", "Отменён"]
    ]
    if not history_orders:
        print("История заказов пуста.")
        return
    print(f"\nИстория заказов клиента {client['name']}:")
    print("-" * 20)
    for order in history_orders:
        print_order(order, show_priority=False)


def add_order(clients, orders):
    print("Добавление заказа.")
    try:
        client_id = int(input("Введите ID клиента: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    client = next((client for client in clients if client["id"] == client_id), None)
    if not client:
        print(f"Клиент с ID {client_id} не найден.")
        return
    order_id = generate_id(orders)
    description = input("Описание заказа: ")
    try:
        amount = float(input("Сумма заказа: "))
    except ValueError:
        print("Ошибка: сумма должна быть числом.")
        return
    print("Приоритет: 1 - Низкий, 2 - Средний, 3 - Высокий")
    priority_dict = {"1": "Низкий", "2": "Средний", "3": "Высокий"}
    priority = priority_dict.get(input("Приоритет: "))
    if not priority:
        print("Неверный выбор приоритета.")
        return
    status = "Новый"
    while True:
        deadline = input("Срок выполнения (YYYY-MM-DD): ")
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
            break
        except ValueError:
            print("Ошибка: введите дату в формате YYYY-MM-DD.")
    orders.append({
        "id": order_id,
        "client_id": client_id,
        "description": description,
        "amount": amount,
        "priority": priority,
        "status": status,
        "deadline": deadline
    })
    client['orders'].append(order_id)
    save_data(clients, orders)
    print("Заказ добавлен.")


def show_orders(clients, orders):
    if not orders:
        print("Список заказов пуст.")
        return
    print("-" * 20)
    for order in orders:
        client_name = next((client["name"] for client in clients if client["id"] == order["client_id"]), "Неизвестен")
        print(f"Клиент: {client_name} (ID: {order['client_id']})")
        print_order(order)


def update_order_status(clients, orders):
    if not orders:
        print("Список заказов пуст.")
        return
    try:
        order_id = int(input("Введите ID заказа: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        print(f"Заказ с ID {order_id} не найден.")
        return
    print("Выберите новый статус заказа:")
    print("1. Новый")
    print("2. В работе")
    print("3. Завершён")
    print("4. Отменён")
    choice = input("Выберите Статус: ")
    status_dict = {"1": "Новый", "2": "В работе", "3": "Завершён", "4": "Отменён"}
    new_status = status_dict.get(choice)
    if not new_status:
        print("Неверный выбор статуса.")
        return
    order["status"] = new_status
    save_data(clients, orders)
    print(f"Статус заказа обновлён на '{new_status}'.")


def delete_order(clients, orders):
    if not orders:
        print("Список заказов пуст.")
        return
    try:
        order_id = int(input("Введите ID заказа для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        print(f"Заказ с ID {order_id} не найден.")
        return
    client = next((client for client in clients if client["id"] == order["client_id"]), None)
    if client and "orders" in client:
        if order_id in client["orders"]:
            client["orders"].remove(order_id)
    orders.remove(order)
    save_data(clients, orders)
    print(f"Заказ удалён.")


def main_menu(clients, orders):
    actions = {
        "1": lambda: add_client(clients, orders),
        "2": lambda: show_clients(clients),
        "3": lambda: delete_client(clients, orders),
        "4": lambda: show_client_orders(clients, orders),
        "5": lambda: show_client_order_history(clients, orders),
        "6": lambda: add_order(clients, orders),
        "7": lambda: show_orders(clients, orders),
        "8": lambda: update_order_status(clients, orders),
        "9": lambda: delete_order(clients, orders),
        "0": lambda: exit()
    }
    while True:
        print("\n=== Главное меню ===")
        print("1. Добавить клиента")
        print("2. Показать клиентов")
        print("3. Удалить клиента")
        print("4. Показать активные заказы клиента")
        print("5. Показать историю заказов клиента")
        print("6. Добавить заказ")
        print("7. Показать все заказы")
        print("8. Изменить статус заказа")
        print("9. Удалить заказ")
        print("0. Выход")
        choice = input("Выберите действие: ")
        print()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор, попробуйте снова.")


# MAIN
clients, orders, data = load_data()
main_menu(clients, orders)