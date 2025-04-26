from datetime import datetime
from ConnectionDB import get_db_connection  # Certifique-se de que esse módulo esteja no lugar certo
import bcrypt
from flask import session

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
        # Verificar se a senha contém apenas caracteres UTF-8
        if not all(ord(c) < 128 for c in self.password):
            raise ValueError("A senha contém caracteres não permitidos")

        
        # Conectar ao banco de dados
        conn = get_db_connection()  # Alterado para chamar a função externa
        cursor = conn.cursor(dictionary=True)

        # Verificar se o email já existe no banco de dados
        cursor.execute("SELECT * FROM users WHERE email = %s", (self.email,))
        user = cursor.fetchone()
        
        if user:
            raise ValueError("O email já está em uso")

        # Criptografar a senha
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        # Inserir o usuário no banco de dados
        cursor.execute(
            "INSERT INTO users (name, email, password, phone,birth_date, address, points, registration_date, status, last_login_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.name, self.email, hashed_password, self.phone, self.birth_date, self.address, self.points, 
             self.registration_date, self.status, self.last_login_date)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Usuário cadastrado com sucesso!"}

    @staticmethod
    def login(email, password):
        """Método para login do usuário e retornar um objeto com as informações"""
        conn = get_db_connection()  # Conecta ao banco de dados
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Atualizar a data de último login
            last_login_date = datetime.now()
            cursor.execute("UPDATE users SET last_login_date = %s WHERE email = %s", 
                        (last_login_date, email))
            conn.commit()

            # Fechar o cursor e a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Criar um dicionário com todas as informações do usuário
            user_info = {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "last_login_date": last_login_date.isoformat(),  # Para garantir que a data seja serializada corretamente
                "cep": user.get('address')  # Assumindo que o campo 'address' contém o CEP
            }

            # Armazenar as informações do usuário na sessão
            session['user_info'] = user_info

            # Retornar a resposta
            return {"message": "Login bem-sucedido", "user": user_info}

        cursor.close()
        conn.close()
        return {"message": "Credenciais inválidas"}
