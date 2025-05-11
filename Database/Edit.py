

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

    def edit_car_availability(cursor, conn, licensePlate, newStatus):
        cursor.execute("""
            SELECT id FROM availability_statuses
            WHERE status = %s
        """, (newStatus,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Availability status '{newStatus}' does not exist.")

        availability_id = result[0]

        # Update the car's availability status
        cursor.execute("""
            UPDATE cars
            SET availability_id = %s
            WHERE plate_number = %s
        """, (availability_id, licensePlate))

        conn.commit()