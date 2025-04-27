from flask import Blueprint, render_template, request, jsonify, session
from models.User import User
from ConnectionDB import get_db_connection
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template("index.html")

from datetime import datetime, timedelta

@routes.route('/home')
def home():
    # Conectar ao banco de dados e buscar as reciclagens
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Supondo que sua tabela de reciclagens se chame 'reciclagens'
    user_id = session.get('user_info', {}).get('id')

    if user_id:
        cursor.execute("""
                        SELECT 
                            recycle.date_recycle, 
                            category_item.`name` as category, 
                            recycle.weight_item,
                            collection_point.`name`,
                            category_item.score_by_kilo * (recycle.weight_item / 1000) AS score,
                            category_item.color_hex  -- Adiciona a cor em formato hexadecimal
                        FROM recycle
                        LEFT JOIN category_item ON recycle.category_id = category_item.id
                        LEFT JOIN collection_point ON recycle.point_id = collection_point.id
                        WHERE recycle.user_id = %s
                        ORDER BY recycle.date_recycle DESC;
                    """, (user_id,))
    else:
        print("Erro: Usuário não autenticado")
    
    dados = cursor.fetchall()

    # Formatar a data no formato 'dd/mm/yyyy'
    for linha in dados:
        linha['date_recycle'] = linha['date_recycle'].strftime('%d/%m/%Y')  # Formata a data

    # Separar os dados nas categorias: Hoje, Ontem, Ainda esta semana, Período anterior
    hoje = []
    ontem = []
    ainda_esta_semana = []
    periodo_anterior = []

    hoje_data = datetime.today()
    ontem_data = hoje_data - timedelta(days=1)
    inicio_semana = hoje_data - timedelta(days=hoje_data.weekday())  # Início da semana
    fim_semana = inicio_semana + timedelta(days=6)  # Fim da semana

    for linha in dados:
        # Convertendo a data para datetime
        data_recycle = datetime.strptime(linha['date_recycle'], '%d/%m/%Y')

        # Verificando se a data é hoje
        if data_recycle.date() == hoje_data.date():
            hoje.append(linha)
        # Verificando se a data é ontem
        elif data_recycle.date() == ontem_data.date():
            ontem.append(linha)
        # Verificando se a data está dentro da mesma semana
        elif inicio_semana.date() <= data_recycle.date() <= fim_semana.date():
            ainda_esta_semana.append(linha)
        else:
            periodo_anterior.append(linha)

    cursor.close()
    conn.close()

    # Passar os dados para o template
    return render_template('home.html', hoje=hoje, ontem=ontem, ainda_esta_semana=ainda_esta_semana, periodo_anterior=periodo_anterior)


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

@routes.route('/cadastrar-reciclagem', methods=['POST'])
def cadastrar_reciclagem():
    data = request.get_json()
    user_info = session.get('user_info')
    if not user_info:
        return {"message": "Usuário não autenticado"}, 401

    user_id = user_info['id']  # Aqui você pega o id do usuário
    date_recycle = datetime.now()
    category_id = data.get('category')
    point_id = data.get('collection_point')
    weight_item = data.get('peso')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO recycle (user_id, category_id, weight_item, point_id, date_recycle)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, category_id, weight_item, point_id, date_recycle))

        conn.commit()
        return jsonify({"message": "Reciclagem cadastrada com sucesso!"})
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar reciclagem:", e)
        return jsonify({"message": "Erro ao cadastrar reciclagem."}), 500
    finally:
        cursor.close()
        conn.close()