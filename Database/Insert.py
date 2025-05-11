from Database.Get import Get

class Insert:
    @staticmethod
    def insert_role_if_not_exists(conn, cursor, name):
        cursor.execute("USE vehicle_management")
        cursor.execute("INSERT IGNORE INTO roles (name) VALUES (%s)", (name,))
        conn.commit()

    @staticmethod
    def insert_user_if_not_exists(conn, cursor, first_name, last_name, password, email, role_name):
        role_id = Get.get_role_id(conn, cursor, role_name)
        if role_id:
            cursor.execute("USE vehicle_management")
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, password, email, role_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, password, email, role_id))
                conn.commit()

    @staticmethod
    def create_hardcoded_users(conn, cursor):

        roles = ['Admin', 'Manager', 'Staff']
        for role in roles:
            Insert.insert_role_if_not_exists(conn, cursor, role)

        users = [
            ("a", "Admin", "a", "a", "Admin"),
            ("b", "Manager", "b", "b", "Manager"),
            ("b", "Staff", "c", "c", "Staff")
        ]
        for first_name, last_name, password, email, role_name in users:
            Insert.insert_user_if_not_exists(conn, cursor, first_name, last_name, password, email, role_name)


    @staticmethod
    def add_user(conn, cursor, first_name, last_name, email, password):
        cursor.execute("USE vehicle_management")
        
        # Default role
        role_name = 'Staff'
        
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, role_id)
            VALUES (%s, %s, %s, %s, (SELECT id FROM roles WHERE name = %s LIMIT 1))
        """, (first_name, last_name, email, password, role_name))
        
        conn.commit()


    def create_car_producers(conn, cursor):
        car_producers = [
            "Toyota", 
            "Ford", 
            "BMW", 
            "Audi", 
            "Mercedes"
        ]

        for producer in car_producers:
            cursor.execute("SELECT COUNT(*) FROM car_producers WHERE name = %s", (producer,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO car_producers (name) VALUES (%s)", (producer,))
            
        conn.commit()

    def create_car_fuel_type(conn, cursor):
        fuel_types = [
            "Petrol",
            "Diesel",
            "Electric",
            "Hybrid",
            "Gas"
        ]

        for fuel_type in fuel_types:
            cursor.execute("SELECT COUNT(*) FROM fuel_types WHERE type = %s", (fuel_type,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO fuel_types (type) VALUES (%s)", (fuel_type,))
        
        conn.commit()

    def create_transmission(conn, cursor):
        transmissions = [
            "Automatic",
            "Manual",
            "CVT",
            "Semi-Automatic"
        ]
        
        for transmission in transmissions:
            cursor.execute("SELECT COUNT(*) FROM transmissions WHERE type = %s", (transmission,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO transmissions (type) VALUES (%s)", (transmission,))
        
           
        conn.commit()

    def create_car_availability_status(conn, cursor):
        availability_statuses = [
            "Unavailable",
            "Available",
            "Pending"
        ]
        
        for status in availability_statuses:
            cursor.execute("SELECT COUNT(*) FROM availability_statuses WHERE status = %s", (status,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO availability_statuses (status) VALUES (%s)", (status,))
            

        conn.commit()


    @staticmethod
    def create_hardcoded_cars(conn, cursor):
        cars = [
            ("Toyota", "Corolla", "2020", "Petrol", "Automatic", "Available", 150, 5, "ABC123"),
            ("Toyota", "Camry", "2021", "Hybrid", "Automatic", "Available", 180, 5, "XYZ987"),
            ("Ford", "Focus", "2019", "Diesel", "Manual", "Unavailable", 130, 5, "DEF456"),
            ("BMW", "3 Series", "2022", "Petrol", "Automatic", "Pending", 250, 5, "LMN789"),
            ("Audi", "A4", "2021", "Diesel", "Semi-Automatic", "Available", 220, 5, "GHI321"),
            ("Mercedes", "C-Class", "2020", "Electric", "Automatic", "Available", 300, 5, "JKL654"),
           
        ]
        
        for producer, model_name, car_year, fuel_type, transmission, availability_status, daily_rental_price, seats, plate_number in cars:
            cursor.execute("""
                SELECT 1 FROM cars WHERE plate_number = %s
            """, (plate_number,))
            existing_car = cursor.fetchone()
            
            if existing_car:
                continue
            
            
            cursor.execute("""
                SELECT id FROM car_producers WHERE name = %s
            """, (producer,))
            producer_id = cursor.fetchone()
            if producer_id:
                producer_id = producer_id[0]
          
            
            cursor.execute("""
                SELECT id FROM fuel_types WHERE type = %s
            """, (fuel_type,))
            fuel_type_id = cursor.fetchone()
            if fuel_type_id:
                fuel_type_id = fuel_type_id[0]
           

            cursor.execute("""
                SELECT id FROM transmissions WHERE type = %s
            """, (transmission,))
            transmission_id = cursor.fetchone()
            if transmission_id:
                transmission_id = transmission_id[0]
           
            cursor.execute("""
                SELECT id FROM availability_statuses WHERE status = %s
            """, (availability_status,))
            availability_id = cursor.fetchone()
            if availability_id:
                availability_id = availability_id[0]
           
            
            cursor.execute("""
                INSERT INTO cars (producer_id, model_name, car_year, fuel_type_id, transmission_id, availability_id, daily_rental_price, seats, plate_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (producer_id, model_name, car_year, fuel_type_id, transmission_id, availability_id, daily_rental_price, seats, plate_number))
           

        conn.commit()

    @staticmethod
    def insert_car(cursor, conn, car_make, model_name, car_year, fuel_type, transmission, daily_rental_price, seats, plate_number):

        availability_status = "Pending"

        try:
            cursor.execute("SELECT id FROM car_producers WHERE name = %s", (car_make,))
            producer_id = cursor.fetchone()

            if not producer_id:
                raise ValueError(f"Producer '{car_make}' not found in the database.")

            producer_id = producer_id[0]

            cursor.execute("SELECT id FROM fuel_types WHERE type = %s", (fuel_type,))
            fuel_type_id = cursor.fetchone()

            if not fuel_type_id:
                raise ValueError(f"Fuel type '{fuel_type}' not found in the database.")

            fuel_type_id = fuel_type_id[0]

            cursor.execute("SELECT id FROM transmissions WHERE type = %s", (transmission,))
            transmission_id = cursor.fetchone()

            if not transmission_id:
                raise ValueError(f"Transmission type '{transmission}' not found in the database.")

            transmission_id = transmission_id[0] 

            cursor.execute("""
                INSERT INTO cars (producer_id, model_name, car_year, fuel_type_id, transmission_id, daily_rental_price, seats, plate_number, availability_id)
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, id
                FROM availability_statuses
                WHERE status = %s
            """, (producer_id, model_name, car_year, fuel_type_id, transmission_id, daily_rental_price, seats, plate_number, availability_status))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error inserting car: {str(e)}")