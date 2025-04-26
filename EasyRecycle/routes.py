from flask import Blueprint, render_template, request, jsonify
from models.User import User
from ConnectionDB import get_db_connection
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template("index.html")

@routes.route('/home')
def home():
     db = get_db_connection()
     cursor = db.cursor(dictionary=True)
     cursor.execute("SELECT * FROM teste")
     dados = cursor.fetchall()

     print("=== Dados vindos do banco ===")
     for linha in dados:
         print(linha)

     cursor.close()
     db.close()
     return render_template("home.html",dados=dados)

@routes.route('/Points')
def Points():
    return render_template('Points.html')

@routes.route('/AddFriend')
def AddFriend():
    return render_template('AddFriend.html')

@routes.route('/Graphics')
def Graphics():
    return render_template('Graphics.html')

@routes.route('/Classification')
def Classification():
    return render_template('Classification.html')


@routes.route('/register', methods=['POST'])
def register():
    print('Rota /register foi chamada!')
    print(request.form)

    name = request.form['name']
    birth_date = request.form['birth_date']
    try:
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y").date()  # Converte para o formato correto
    except ValueError:
        raise ValueError("A data de nascimento está em um formato incorreto. Use o formato DD/MM/YYYY.")
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # Aqui cria o objeto User
    user = User(
        id=None,  # Pode ser None, se o MySQL gerar automaticamente
        name=name,
        email=email,
        password=password,
        phone=phone,
        address=address,
        birth_date = birth_date
    )

    result = user.cadastro()
    return jsonify({'message': result})

    

@routes.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']   # Pega do form, igual o cadastro
        password = request.form['password']

        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        result = User.login(email, password)

        if result.get('message') == 'Login bem-sucedido':
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        print('Erro no login:', e)
        return jsonify({'error': 'Erro interno no servidor'}), 500


@routes.route('/get-itens')
def get_itens():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name FROM category_item')
    itens = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(itens)    

@routes.route('/get-collection-points', methods=['GET'])
def get_collection_points():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM collection_point")
    points = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(points)

    