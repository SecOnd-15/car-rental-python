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

