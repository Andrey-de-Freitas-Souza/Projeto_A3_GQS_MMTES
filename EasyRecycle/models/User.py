from datetime import datetime
from ConnectionDB import get_db_connection  # se você tiver um módulo separado para conexão

class User:
    def __init__(self, id, name, email, password, phone=None, address=None,
                 points=0, registration_date=None, status='active', last_login_date=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.points = points
        self.registration_date = registration_date
        self.status = status
        self.last_login_date = last_login_date

    @staticmethod
    def find_by_email(email):
        """Searches for a user in the database by email and returns a User object."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, email, password, phone, address, points, registration_date, status, last_login_date 
            FROM Users 
            WHERE email = %s
        """, (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return User(*result)
        else:
            return None

