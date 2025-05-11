

class Get:
    @staticmethod
    def get_role_id(conn, cursor, name):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id FROM roles WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    

    @staticmethod
    def get_user_data(conn, cursor, email, password):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT id, first_name, last_name, email, role_id 
            FROM users WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        
        if user:
            cursor.execute("SELECT name FROM roles WHERE id = %s", (user[4],))
            role = cursor.fetchone()[0]
            return {
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "email": user[3],
                "role": role
            }
        return None
    
    @staticmethod
    def get_all_user_ids(cursor, conn):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]
    

    @staticmethod
    def get_all_users_data(cursor, conn):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT 
                users.id, 
                users.first_name, 
                users.last_name, 
                users.email, 
                roles.name AS role
            FROM users
            JOIN roles ON users.role_id = roles.id
        """)
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4]
            } for row in rows
        ]

    @staticmethod
    def get_all_services_data(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price, ss.status_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
            """)

          
            services = cursor.fetchall()

            services_array = [
                {'service_name': service[0], 'price': service[1], 'status_name': service[2]}
                for service in services
            ]
            
            return services_array

        except Exception as e:
            raise Exception(f"Error retrieving services: {str(e)}")

    @staticmethod
    def get_all_cars_data(cursor):
        try:
            cursor.execute("""
                SELECT 
                    c.id, 
                    cp.name AS producer_name, 
                    c.model_name, 
                    c.car_year, 
                    ft.type AS fuel_type, 
                    t.type AS transmission,
                    availability_statuses.status AS availability_status,  -- This will return the availability status name
                    c.daily_rental_price, 
                    c.seats, 
                    c.plate_number, 
                    c.deletion_status
                FROM cars c
                JOIN car_producers cp ON c.producer_id = cp.id
                JOIN fuel_types ft ON c.fuel_type_id = ft.id
                JOIN transmissions t ON c.transmission_id = t.id
                JOIN availability_statuses ON c.availability_id = availability_statuses.id
            """)

            cars_data = cursor.fetchall()

            return cars_data
        except Exception as e:
            raise Exception(f"Error fetching car data: {str(e)}")
        
    @staticmethod
    def get_all_pending_services(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price, ss.status_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Pending'
            """)

            services = cursor.fetchall()

            services_array = [
                {'service_name': service[0], 'price': service[1], 'status_name': service[2]}
                for service in services
            ]
            
            return services_array

        except Exception as e:
            raise Exception(f"Error retrieving pending services: {str(e)}")
        
    @staticmethod
    def get_all_pending_service_names(cursor):
        try:
          
            cursor.execute("""
                SELECT s.service_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Pending'
            """)

            services = cursor.fetchall()

            service_names = [service[0] for service in services]
            
            return service_names

        except Exception as e:
            raise Exception(f"Error retrieving pending service names: {str(e)}")
            
    @staticmethod
    def get_all_cars_data_to_be_deleted(cursor):
        cursor.execute("""
            SELECT 
                c.id, 
                cp.name AS producer_name, 
                c.model_name, 
                c.car_year, 
                ft.type AS fuel_type, 
                t.type AS transmission,
                availability_statuses.status AS availability_status,  
                c.daily_rental_price, 
                c.seats, 
                c.plate_number, 
                c.deletion_status
            FROM cars c
            JOIN car_producers cp ON c.producer_id = cp.id
            JOIN fuel_types ft ON c.fuel_type_id = ft.id
            JOIN transmissions t ON c.transmission_id = t.id
            JOIN availability_statuses ON c.availability_id = availability_statuses.id
            WHERE c.deletion_status = 'To Be Deleted'
        """)
        
        return cursor.fetchall()
    
    @staticmethod
    def get_all_cars_plate_data_to_be_deleted(cursor):
        cursor.execute("""
            SELECT c.plate_number
            FROM cars c
            WHERE c.deletion_status = 'To Be Deleted'
        """)
        
        return cursor.fetchall()



    @staticmethod
    def get_car_data_by_license_plate(cursor, license_plate):
        cursor.execute("""
            SELECT 
                c.id, 
                cp.name AS producer_name, 
                c.model_name, 
                c.car_year, 
                ft.type AS fuel_type, 
                t.type AS transmission,
                availability_statuses.status AS availability_status,  
                c.daily_rental_price, 
                c.seats, 
                c.plate_number, 
                c.deletion_status
            FROM cars c
            JOIN car_producers cp ON c.producer_id = cp.id
            JOIN fuel_types ft ON c.fuel_type_id = ft.id
            JOIN transmissions t ON c.transmission_id = t.id
            JOIN availability_statuses ON c.availability_id = availability_statuses.id
            WHERE c.plate_number = %s
        """, (license_plate,))
        
        result = cursor.fetchone()
        
        return result
        
    @staticmethod
    def get_all_pending_cars_data(cursor):
        try:
            cursor.execute("""
                SELECT 
                    c.id, 
                    cp.name AS producer_name, 
                    c.model_name, 
                    c.car_year, 
                    ft.type AS fuel_type, 
                    t.type AS transmission,
                    availability_statuses.status AS availability_status,  
                    c.daily_rental_price, 
                    c.seats, 
                    c.plate_number, 
                    c.deletion_status
                FROM cars c
                JOIN car_producers cp ON c.producer_id = cp.id
                JOIN fuel_types ft ON c.fuel_type_id = ft.id
                JOIN transmissions t ON c.transmission_id = t.id
                JOIN availability_statuses ON c.availability_id = availability_statuses.id
                WHERE availability_statuses.status = 'Pending'
            """)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching pending car data: {e}")
            return []

        
    @staticmethod
    def get_all_producer_names(cursor):
        try:
            cursor.execute("""
                SELECT name FROM car_producers
            """)
            
            producer_names = cursor.fetchall()
            return [producer[0] for producer in producer_names]
        
        except Exception as e:
            raise Exception(f"Error fetching producer names: {str(e)}")
        
    @staticmethod
    def get_all_transmission_types(cursor):
        try:
            cursor.execute("""
                SELECT type FROM transmissions
            """)
            
            transmission_types = cursor.fetchall()
            
            return [transmission[0] for transmission in transmission_types]
        
        except Exception as e:
            raise Exception(f"Error fetching transmission types: {str(e)}")
        
    @staticmethod
    def get_all_fuel_types(cursor):
        try:
            cursor.execute("""
                SELECT type FROM fuel_types
            """)
            
            fuel_types = cursor.fetchall()
            
            return [fuel_type[0] for fuel_type in fuel_types]
        
        except Exception as e:
            raise Exception(f"Error fetching fuel types: {str(e)}")
        
    @staticmethod
    def get_all_plate_numbers(cursor):
        cursor.execute("""
            SELECT plate_number FROM cars
        """)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_pending_plate(cursor):
        cursor.execute("""
            SELECT c.plate_number
            FROM cars c
            JOIN availability_statuses a ON c.availability_id = a.id
            WHERE a.status = 'Pending'
        """)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_license_plates_for_available_or_maintenance(cursor):
        try:
            cursor.execute("""
                SELECT c.plate_number
                FROM cars c
                JOIN availability_statuses AS status ON c.availability_id = status.id
                WHERE status.status IN ('Available', 'Maintenance')
            """)

            license_plates = cursor.fetchall()

            return [plate[0] for plate in license_plates]
        
        except Exception as e:
            raise Exception(f"Error fetching license plates for available or maintenance cars: {str(e)}")


    @staticmethod
    def get_car_availability_by_plate(cursor, license_plate):
        try:
            cursor.execute("""
                SELECT status.status
                FROM cars c
                JOIN availability_statuses AS status ON c.availability_id = status.id
                WHERE c.plate_number = %s
            """, (license_plate,))

            availability_status = cursor.fetchone()

            if availability_status:
                return availability_status[0]
            else:
                return None

        except Exception as e:
            raise Exception(f"Error fetching availability for car with plate {license_plate}: {str(e)}")
        

    @staticmethod
    def get_all_customer_names(cursor):
        try:
            cursor.execute("""
                SELECT CONCAT(first_name, ' ', last_name) AS full_name
                FROM customers
            """)
            customer_names = cursor.fetchall()

            return [row[0] for row in customer_names] if customer_names else []

        except Exception as e:
            raise Exception(f"Error fetching customer names: {str(e)}")
        
    @staticmethod
    def get_all_service_names_and_prices(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Available'
            """)
            services = cursor.fetchall()

            return {service_name: float(price) for service_name, price in services} if services else {}

        except Exception as e:
            raise Exception(f"Error fetching available services and prices: {str(e)}")
        
    @staticmethod
    def get_car_price_by_plate(cursor, plate_number):
        try:
            cursor.execute("""
                SELECT daily_rental_price
                FROM cars
                WHERE plate_number = %s
            """, (plate_number,))
            
            result = cursor.fetchone()
            return float(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching price for car with plate {plate_number}: {str(e)}")
        
    @staticmethod
    def get_service_price_by_name(cursor, service_name):
        try:
            cursor.execute("""
                SELECT price
                FROM services
                WHERE service_name = %s
            """, (service_name,))
            
            result = cursor.fetchone()
            return float(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching price for service '{service_name}': {str(e)}")
        
    @staticmethod
    def get_user_reputation(cursor, full_name):
        try:
            parts = full_name.rsplit(" ", 1)
            if len(parts) == 2:
                first_name, last_name = parts
            else:
                first_name, last_name = parts[0], None
            
            cursor.execute("""
                SELECT reputation 
                FROM customers 
                WHERE first_name = %s AND last_name = %s
            """, (first_name, last_name))
            
            result = cursor.fetchone()
            return int(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching reputation for customer '{full_name}': {str(e)}")
        

    