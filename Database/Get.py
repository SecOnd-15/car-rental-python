

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