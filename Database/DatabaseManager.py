import mysql.connector
from Database.Insert import Insert
from Database.Get import Get
from Database.Check import Check

class DatabaseManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.Insert = Insert
        self.Get = Get
        self.Check = Check

    def bootstrap(self):
        self.create_tables()
        Insert.create_hardcoded_users(self.conn, self.cursor)

  

    def create_tables(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS vehicle_management")
        self.conn.commit()
        self.cursor.execute("USE vehicle_management")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                password TEXT NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                role_id INT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE
            )
        """)

        self.conn.commit()

   
