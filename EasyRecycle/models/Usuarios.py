from datetime import datetime
from ConnectionDB import get_db_connection  # se você tiver um módulo separado para conexão

class Usuario:
    def __init__(self, id, nome, email, senha, telefone=None, endereco=None,
                 pontos=0, data_cadastro=None, status='ativo', data_ultimo_login=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.pontos = pontos
        self.data_cadastro = data_cadastro
        self.status = status
        self.data_ultimo_login = data_ultimo_login

    @staticmethod
    def buscar_por_email(email):
        """Busca um usuário no banco de dados pelo e-mail e retorna um objeto Usuario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, senha, telefone, endereco, pontos, data_cadastro, status, data_ultimo_login FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return Usuario(*resultado)
        else:
            return None
