

class Get:
    @staticmethod
    def get_role_id(conn, cursor, name):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id FROM roles WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None