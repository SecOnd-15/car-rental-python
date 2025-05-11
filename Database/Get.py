

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