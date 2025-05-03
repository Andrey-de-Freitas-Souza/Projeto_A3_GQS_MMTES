from datetime import datetime
import bcrypt
from ConnectionDB import get_db_connection  # Certifique-se de que esse módulo esteja correto
from flask import jsonify, session

class User:
    def __init__(self, id=None, name=None, email=None, password=None, phone=None, address=None,
                 points=0, registration_date=None, status='active', last_login_date=None, birth_date=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.points = points
        self.registration_date = registration_date if registration_date else datetime.now()
        self.status = status
        self.last_login_date = last_login_date
        self.birth_date = birth_date

    def cadastro(self):
        """Método para cadastrar o usuário no banco de dados"""
        try:
            # Verificar se a senha contém apenas caracteres UTF-8
            if not all(ord(c) < 128 for c in self.password):
                raise ValueError("A senha contém caracteres não permitidos")

            # Conectar ao banco de dados
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Verificar se o email já existe no banco de dados
            cursor.execute("SELECT * FROM users WHERE email = %s", (self.email,))
            user = cursor.fetchone()
            
            if user:
                raise ValueError("O email já está em uso")

            # Criptografar a senha
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Inserir o usuário no banco de dados
            cursor.execute(
                "INSERT INTO users (name, email, password, phone, birth_date, address, points, registration_date, status, last_login_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (self.name, self.email, hashed_password, self.phone, self.birth_date, self.address, self.points, 
                 self.registration_date, self.status, self.last_login_date)
            )
            conn.commit()

            cursor.close()
            conn.close()

            return {"message": "Usuário cadastrado com sucesso!"}

        except Exception as e:
            print(f"Erro no cadastro: {e}")
            return {"message": f"Erro: {e}"}

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "address": self.address,
            "points": self.points,
            "registration_date": self.registration_date,
            "status": self.status,
            "last_login_date": self.last_login_date,
            "birth_date": self.birth_date
        }

    @staticmethod
    def login(email, password):
        """Método para login do usuário e retornar um objeto com as informações"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                hashed_password = user['password']
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    # Atualizar a data de último login
                    last_login_date = datetime.now()
                    cursor.execute("UPDATE users SET last_login_date = %s WHERE email = %s", 
                                (last_login_date, email))
                    conn.commit()

                    # Criar objeto User
                    user_obj = User(
                        id=user['id'],
                        name=user['name'],
                        email=user['email'],
                        password=hashed_password,
                        phone=user['phone'],
                        address=user['address'],
                        points=user['points'],
                        registration_date=user['registration_date'],
                        status=user['status'],
                        last_login_date=last_login_date,
                        birth_date=user['birth_date']
                    )

                    # Sessão
                    session['user_info'] = user_obj.to_dict()

                    return {
                        "message": "Login bem-sucedido",
                        "user": user_obj.to_dict()
                    }

            return {"message": "Credenciais inválidas"}

        except Exception as e:
            print(f"Erro no login: {e}")
            return {"message": "Erro no servidor"}

        finally:
            cursor.close()
            conn.close()
