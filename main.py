import csv
import psycopg2
from typing import List, Tuple, Any


def get_connection():
    """Подключение к базе данных north."""
    return psycopg2.connect(
        host="localhost",
        database="north",
        user="postgres",  # Твой пользователь PostgreSQL
        password="postgres",  # Твой пароль от PostgreSQL
        port="5432"
    )


def read_csv_file(filename: str) -> List[Tuple[Any, ...]]:
    """Чтение данных из CSV файла."""
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Пропускаем заголовок
        return [tuple(row) for row in reader]


def insert_employees(
        conn: psycopg2.extensions.connection,
        data: List[Tuple[Any, ...]]
) -> None:
    """Вставка данных в таблицу employees."""
    with conn.cursor() as cur:
        for row in data:
            cur.execute(
                """
                INSERT INTO employees
                (employee_id, first_name, last_name, title, birth_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                row
            )
    conn.commit()


def insert_customers(
        conn: psycopg2.extensions.connection,
        data: List[Tuple[Any, ...]]
) -> None:
    """Вставка данных в таблицу customers."""
    with conn.cursor() as cur:
        for row in data:
            cur.execute(
                """
                INSERT INTO customers
                (customer_id, company_name, contact_name)
                VALUES (%s, %s, %s)
                """,
                row
            )
    conn.commit()


def insert_orders(
        conn: psycopg2.extensions.connection,
        data: List[Tuple[Any, ...]]
) -> None:
    """Вставка данных в таблицу orders."""
    with conn.cursor() as cur:
        for row in data:
            cur.execute(
                """
                INSERT INTO orders
                (order_id, customer_id, employee_id, order_date, ship_city)
                VALUES (%s, %s, %s, %s, %s)
                """,
                row
            )
    conn.commit()


def main() -> None:
    """Основная функция."""
    employees_data = read_csv_file('employees_data.csv')
    customers_data = read_csv_file('customers_data.csv')
    orders_data = read_csv_file('orders_data.csv')

    conn = get_connection()
    try:
        print("Вставляем сотрудников...")
        insert_employees(conn, employees_data)

        print("Вставляем клиентов...")
        insert_customers(conn, customers_data)

        print("Вставляем заказы...")
        insert_orders(conn, orders_data)

        print("Готово! Данные успешно загружены.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
