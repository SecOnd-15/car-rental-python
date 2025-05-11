

class Check:

    @staticmethod
    def check_user_if_exist(conn, cursor, email):
        cursor.execute("USE vehicle_management")
        
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        return True if user else False
    

   