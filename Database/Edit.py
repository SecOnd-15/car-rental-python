

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

    @staticmethod
    def mark_car_to_be_deleted(cursor, conn, license_plate):
        try:
            cursor.execute("""
                UPDATE cars
                SET deletion_status = 'To Be Deleted'
                WHERE plate_number = %s
            """, (license_plate,))
            
            conn.commit() 

        except Exception as e:
            raise Exception(f"Error marking car for deletion: {str(e)}")

    @staticmethod
    def mark_car_as_none(cursor, conn, license_plate):
        try:
            cursor.execute("""
                UPDATE cars
                SET deletion_status = 'None'
                WHERE plate_number = %s
            """, (license_plate,))
            
            conn.commit()
        
        except Exception as e:
            raise Exception(f"Error removing car for deletion: {str(e)}")
        
    @staticmethod
    def edit_car_price_by_plate(cursor, conn, license_plate, new_price):
        try:
            cursor.execute("""
                UPDATE cars
                SET daily_rental_price = %s
                WHERE plate_number = %s
            """, (new_price, license_plate))
            
            conn.commit()
        
        except Exception as e:
            raise Exception(f"Error updating price for car with plate '{license_plate}': {str(e)}")
          