import mysql.connector
from Database.Insert import Insert
from Database.Get import Get
from Database.Check import Check
from Database.Delete import Delete
from Database.Edit import Edit

class DatabaseManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.Insert = Insert
        self.Get = Get
        self.Check = Check
        self.Delete = Delete
        self.Edit = Edit


    def bootstrap(self):
        self.create_user_tables()
        self.create_car_tables()
        self.create_service_tables()

        # Users
        Insert.create_hardcoded_users(self.conn, self.cursor)

        # Cars
        Insert.create_car_producers(conn=self.conn, cursor=self.cursor)
        Insert.create_car_fuel_type(conn=self.conn, cursor=self.cursor)
        Insert.create_car_availability_status(conn=self.conn, cursor=self.cursor)
        Insert.create_transmission(conn=self.conn, cursor=self.cursor)
        Insert.create_hardcoded_cars(conn=self.conn, cursor=self.cursor)

        #Service
        
        Insert.create_hardcoded_services_statuses(conn=self.conn, cursor=self.cursor)
        Insert.create_hardcoded_services(conn=self.conn, cursor=self.cursor)

  

    def create_user_tables(self):
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

    
    def create_service_tables(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS vehicle_management")
        self.conn.commit()
        self.cursor.execute("USE vehicle_management")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_statuses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                status_name VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
                status_id INT NOT NULL,
                FOREIGN KEY (status_id) REFERENCES service_statuses(id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE
            )
        """)

        self.conn.commit()

    def create_car_tables(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS vehicle_management")
        self.conn.commit()
        self.cursor.execute("USE vehicle_management")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS car_producers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fuel_types (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transmissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS availability_statuses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                status VARCHAR(20) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                producer_id INT NOT NULL,
                model_name VARCHAR(100) NOT NULL,
                car_year VARCHAR(4) NOT NULL,
                fuel_type_id INT NOT NULL,
                transmission_id INT NOT NULL,
                daily_rental_price DECIMAL(10, 2) NOT NULL CHECK (daily_rental_price > 0),
                seats INT NOT NULL CHECK (seats > 0),
                plate_number VARCHAR(20) NOT NULL UNIQUE,
                availability_id INT NOT NULL,
                deletion_status VARCHAR(20) DEFAULT 'None' NOT NULL,

                FOREIGN KEY (producer_id) REFERENCES car_producers(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (transmission_id) REFERENCES transmissions(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (availability_id) REFERENCES availability_statuses(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,

                UNIQUE (producer_id, model_name, car_year)
            )
        """)
        self.conn.commit()
        
   
