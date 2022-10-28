import psycopg2

def create_db(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(20),
            lastname VARCHAR(20),
            email VARCHAR(40) NOT NULL);
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            phone VARCHAR(20) NOT NULL);
        """)
    conn.commit()


def add_client(cur, first_name, last_name, email, phone=None):
    if first_name == None or last_name == None or email == None:
        print('Не заполнено основное поле Имя/Фамилия/Почта')
        return

    cur.execute("""
        INSERT INTO clients(firstname, lastname, email) VALUES(%s, %s, %s) RETURNING id, firstname, lastname;
        """, (first_name, last_name, email))
    new_client = cur.fetchone()
    if phone is not None:
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (new_client[0], phone))
        cur.fetchone()
    print(f'Добавили клиента {new_client}')


def get_phone(cur, client_id, phone):
    cur.execute("""
        SELECT phone FROM phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
    found_phone = cur.fetchall()
    return found_phone


def add_phone(conn, cur, client_id, phone):
    # Проверим, есть ли такой телефон в базе
    found_phone = get_phone(cur, client_id, phone)
    if found_phone is None or len(found_phone) == 0:
        print(found_phone, client_id, phone)
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (client_id, phone))
        conn.commit()


def change_client(conn, cur, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cur.execute("""
            UPDATE clients SET firstname=%s WHERE id=%s
            """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
            UPDATE clients SET lastname=%s WHERE id=%s
            """, (last_name, client_id))
    if email is not None:
        cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s
            """, (email, client_id))
    if phone is not None:
        add_phone(conn, cur, client_id, phone)

    cur.execute("""
        SELECT * FROM clients;
        """)
    cur.fetchall()


def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s and phone=%s;
        """, (client_id, phone))
    cur.execute("""
        SELECT * FROM phones WHERE client_id=%s;
        """, (client_id,))
    print(cur.fetchall())


def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
            SELECT cl.id FROM clients cl
            JOIN phones ph ON ph.client_id = cl.id
            WHERE ph.phone=%s;
            """, (phone,))
    else:
        cur.execute("""
            SELECT id FROM clients
            WHERE firstname=%s OR lastname=%s OR email=%s;
            """, (first_name, last_name, email))
    print(cur.fetchall())


def all_clients(cur):
        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())
        cur.execute("""
            SELECT * FROM phones;
            """)
        print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="netology_clients_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            create_db(conn, cur)

            # all_clients(cur)

            # add_client(cur, 'Роман', 'Сизов', 'sizov@gmail.com', '+79118475213')
            # add_client(cur, 'Юлия', 'Иванова', 'ivanova12@gmail.com')
            # add_client(cur, 'Алексей', 'Соколов', 'socol@gmail.com', '+79262521212')
            # add_client(cur, 'Женя', None, None)
            # add_client(cur, 'Валя', 'Семенова', None)
            # add_client(cur, 'Антон', 'Иванов', 'SSS15@gmail.com')
            #
            # all_clients(cur)
            #
            # print(get_phone(cur, '1', '+79118475213'))
            # add_phone(conn, cur, '2', '234-45-45')
            # add_phone(conn, cur, '1', '777-45-34')
            # add_phone(conn, cur, '3', '455-23-33')
            #
            # all_clients(cur)
            #
            # change_client(conn, cur, '1', 'Семен')
            # change_client(conn, cur, '2', None, 'Логозина')
            # change_client(conn, cur, '3', None, None, 'belozub@gmail.com')
            # change_client(conn, cur, '2', None, None, None, '+7-999-345-76-76')
            #
            # all_clients(cur)
            #
            # delete_phone(cur, '1', '777-45-33')
            # delete_phone(cur, '1', '777-45-34')
            #
            # all_clients(cur)
            #
            # find_client(cur, 'Юлия')
            # find_client(cur, None, 'Сизов')
            # find_client(cur, None, None, 'belozub@gmail.com')
            # find_client(cur, None, None, None, '234-45-45')
            #
            # delete_client(cur, 5)
            #
            all_clients(cur)
