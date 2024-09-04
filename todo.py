import sqlite3


class DatabaseManager:
    def __init__(self, db_name="todos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN
            );
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("Table created successfully")

    def get_all(self):
        query = "SELECT * FROM todos"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create(self, task, done):
        query = """
            INSERT INTO todos (task, done)
            VALUES (?, ?);
        """
        self.cursor.execute(query, (task, done))
        self.conn.commit()
        print(f"'{task}, {done}' created successfully")

    def update(self, pk, task, done):
        query = """
            UPDATE todos
            SET task = ?, done = ?
            WHERE id = ?;
        """
        self.cursor.execute(query, (task, done, pk))
        self.conn.commit()
        print(f"{pk} updated")

    def delete(self, pk):
        query = """
            DELETE FROM todos
            WHERE id = ?;
        """
        self.cursor.execute(query, (pk,))
        self.conn.commit()
        print(f"{pk} deleted")



