import psycopg2
from psycopg2 import sql



# Функция для подключения к базе данных
def connect_db():
    return psycopg2.connect(
        dbname="maxim_db",
        user="postgres",
        password="postgres",
        host="localhost"
    )


# Функция для создания таблиц
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()


# Функция для добавления нового клиента
def add_client(first_name, last_name, email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s)
    ''', (first_name, last_name, email))

    conn.commit()
    cursor.close()
    conn.close()


# Функция для добавления телефона
def add_phone(client_id, phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO phones (client_id, phone_number)
        VALUES (%s, %s)
    ''', (client_id, phone_number))

    conn.commit()
    cursor.close()
    conn.close()


# Функция для изменения данных клиента
def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = connect_db()
    cursor = conn.cursor()

    if first_name:
        cursor.execute('''
            UPDATE clients
            SET first_name = %s
            WHERE id = %s
        ''', (first_name, client_id))

    if last_name:
        cursor.execute('''
            UPDATE clients
            SET last_name = %s
            WHERE id = %s
        ''', (last_name, client_id))

    if email:
        cursor.execute('''
            UPDATE clients
            SET email = %s
            WHERE id = %s
        ''', (email, client_id))

    conn.commit()
    cursor.close()
    conn.close()


# Функция для удаления телефона
def delete_phone(phone_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM phones
        WHERE id = %s
    ''', (phone_id,))

    conn.commit()
    cursor.close()
    conn.close()


# Функция для удаления клиента
def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM clients
        WHERE id = %s
    ''', (client_id,))

    conn.commit()
    cursor.close()
    conn.close()


# Функция для поиска клиента
def find_client(search_term):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(sql.SQL('''
        SELECT * FROM clients
        WHERE first_name ILIKE %s OR last_name ILIKE %s OR email ILIKE %s
    ''').format(sql.Identifier('clients')), (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    return clients


# Пример демонстрации работы функций
if __name__ == "__main__":
    create_tables()

    # Добавление нового клиента
    add_client("John", "Doe", "john.doe@example.com")

    # Добавление телефона
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM clients WHERE email = %s', ("john.doe@example.com",))
    client_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    add_phone(client_id, "+1234567890")

    # Поиск клиента
    clients = find_client("Doe")
    print("Clients found:", clients)

    # Обновление клиента
    update_client(client_id, email="john.new@example.com")

    # Удаление телефона
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM phones WHERE phone_number = %s', ("+1234567890",))
    phone_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    delete_phone(phone_id)

    # Удаление клиента
    delete_client(client_id)
