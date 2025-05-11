

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

            # Fetch all car data
            cars_data = cursor.fetchall()

            return cars_data
        except Exception as e:
            raise Exception(f"Error fetching car data: {str(e)}")
        
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