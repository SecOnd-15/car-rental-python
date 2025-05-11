

class Edit:


    @staticmethod
    def edit_user_role(cursor, conn, user_id, user_role):
        cursor.execute("USE vehicle_management")

        # Get role_id
        cursor.execute("SELECT id FROM roles WHERE name = %s", (user_role,))
        role = cursor.fetchone()
        if not role:
            return 

        role_id = role[0]

        # Update user's role
        cursor.execute("UPDATE users SET role_id = %s WHERE id = %s", (role_id, user_id))
        conn.commit()