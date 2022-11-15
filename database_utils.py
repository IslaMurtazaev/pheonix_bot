import sqlite3
from telegram import User, Message


def connect_to_db():
    con = sqlite3.connect("tasks.db")
    return con, con.cursor()


def setup_database():
    connection, cursor = connect_to_db()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id int UNIQUE NOT NULL,
            first_name varchar(100),
            last_name varchar(100),
            username varchar(100) NOT NULL,
            PRIMARY KEY (id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date int NOT NULL,
            user_id int NOT NULL,
            description varchar(1000) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        );
    """)

    connection.commit()


def create_user(user: User) -> None:
    connection, cursor = connect_to_db()

    res = cursor.execute(f"""
        SELECT 1 from Users WHERE id = {user.id}
    """)

    user_exists = res.fetchone()

    if not user_exists:
        cursor.execute(f"""
            INSERT INTO Users ('id', 'first_name', 'last_name', 'username')
            VALUES ('{user.id}', '{user.first_name}', '{user.last_name}', '{user.username}');
        """)

    connection.commit()


def creat_tasks(message: Message):
    connection, cursor = connect_to_db()

    tasks = message.text.split('\n')
    for task in tasks[1:]:
        cursor.execute(f"""
            INSERT INTO Tasks ('date', 'user_id', 'description')
            VALUES ('{message.date}', '{message.from_user.id}', '{task}');
        """)

    connection.commit()
