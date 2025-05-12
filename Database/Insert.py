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
    def create_hardcoded_customers(conn, cursor):
        # (first_name, last_name, email, address, phone, reputation)
        customers = [
            # Regular customers with good reputation (default 50)
            ("John", "Doe", "john.doe@example.com", "123 Elm Street", "1234567890", 50),
            ("Jane", "Smith", "jane.smith@example.com", "456 Oak Avenue", "9876543210", 50),
            ("Alice", "Johnson", "alice.johnson@example.com", "789 Pine Road", "1122334455", 50),
            ("Bob", "Williams", "bob.williams@example.com", "321 Maple Blvd", "6677889900", 50),
            ("Charlie", "Brown", "charlie.brown@example.com", "101 Birch Lane", "3344556677", 50),
            ("Emily", "Davis", "emily.davis@example.com", "202 Cedar Street", "2233445566", 50),

            # Customers with bad reputation (below 20)
            ("Tom", "Green", "tom.green@example.com", "789 Ash Ave", "5566778899", 15),  # Low reputation
            ("Samantha", "Black", "samantha.black@example.com", "567 Elmwood Drive", "9988776655", 12),  # Low reputation
            ("Michael", "White", "michael.white@example.com", "345 Maple Street", "1122334455", 18),  # Low reputation
            ("Olivia", "Blue", "olivia.blue@example.com", "678 Oakwood Rd", "6677889900", 10),  # Low reputation
            ("David", "Gray", "david.gray@example.com", "432 Pinewood Blvd", "3344556677", 5),   # Very low reputation
            ("Sophia", "Purple", "sophia.purple@example.com", "654 Cedarwood St", "2233445566", 2),   # Very low reputation
        ]
        
        for first_name, last_name, email, address, phone_number, reputation in customers:
            cursor.execute("""
                SELECT COUNT(*) FROM customers WHERE email = %s
            """, (email,))
            customer_exists = cursor.fetchone()[0]
            
            if customer_exists == 0:
                cursor.execute("""
                    INSERT INTO customers (first_name, last_name, email, phone_number, address, reputation)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, email, phone_number, address, reputation))
             

        conn.commit()

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
            "Pending",
            "Maintenance"
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
    def create_hardcoded_services_statuses(cursor, conn):
        try:
            statuses = ['Pending', 'Available']

            for status in statuses:
                cursor.execute("""
                    SELECT 1 FROM service_statuses WHERE status_name = %s
                """, (status,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO service_statuses (status_name)
                        VALUES (%s)
                    """, (status,))
            
            conn.commit()

        except Exception as e:
            raise Exception(f"Error ensuring service statuses: {str(e)}")
        
    @staticmethod
    def create_hardcoded_services(cursor, conn):
        try:
            services = [
                ('GPS Navigation', 5.00, 'Pending'),
                ('Child Seat', 7.50, 'Pending'),
                ('Additional Insurance', 15.00, 'Available'),
                ('Roadside Assistance', 10.00, 'Available'),
                ('Wi-Fi Hotspot', 8.00, 'Available'),
                ('Extended Mileage', 12.00, 'Available')
            ]

            for name, price, status_name in services:
                # Check if the status exists
                cursor.execute("""
                    SELECT id FROM service_statuses WHERE status_name = %s
                """, (status_name,))
                status = cursor.fetchone()

                if not status:
                    raise Exception(f"Status '{status_name}' not found. Run ensure_service_statuses first.")

                status_id = status[0]

                # Check if the service already exists
                cursor.execute("""
                    SELECT 1 FROM services WHERE service_name = %s
                """, (name,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO services (service_name, price, status_id)
                        VALUES (%s, %s, %s)
                    """, (name, price, status_id))

            conn.commit()

        except Exception as e:
            raise Exception(f"Error creating hardcoded services: {str(e)}")

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
        

    @staticmethod
    def insert_service(cursor, conn, service_name, price):
        try:
            cursor.execute("""
                INSERT INTO services (service_name, price, status_id)
                SELECT %s, %s, id FROM service_statuses WHERE status_name = "Pending"
            """, (service_name, price))

            conn.commit()

        except Exception as e:
            raise Exception(f"Error inserting service: {str(e)}")
        
    @staticmethod
    def add_rental(conn, cursor, customer_email, plate_number, rental_date, return_date,
                total_amount, downpayment_amount, selected_services):
        cursor.execute("USE vehicle_management")

        # Get customer ID from email
        cursor.execute("SELECT id FROM customers WHERE email = %s", (customer_email,))
        customer_row = cursor.fetchone()
        if not customer_row:
            raise ValueError("Customer not found.")
        customer_id = customer_row[0]

        # Get car ID from plate number
        cursor.execute("SELECT id FROM cars WHERE plate_number = %s", (plate_number,))
        car_row = cursor.fetchone()
        if not car_row:
            raise ValueError("Car not found.")
        car_id = car_row[0]

        # Insert rental
        cursor.execute("""
            INSERT INTO rentals (customer_id, car_id, rental_date, return_date, total_amount, preliminary_total, downpayment_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (customer_id, car_id, rental_date, return_date, total_amount, total_amount, downpayment_amount))
        rental_id = cursor.lastrowid

        # Link services to rental
        for service_name in selected_services:
            cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
            service_row = cursor.fetchone()
            if service_row:
                service_id = service_row[0]
                cursor.execute("""
                    INSERT INTO rental_services (rental_id, service_id)
                    VALUES (%s, %s)
                """, (rental_id, service_id))

        conn.commit()

    @staticmethod
    def add_customer(conn, cursor, first_name, last_name, email, phone_number, address):
        cursor.execute("USE vehicle_management")

        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone_number, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone_number, address))

        conn.commit()