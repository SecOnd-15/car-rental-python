

class Delete():


    @staticmethod
    def delete_user(cursor, conn, id):
        cursor.execute("USE vehicle_management")
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()