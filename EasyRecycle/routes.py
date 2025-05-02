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

@routes.route('/recycle_by_category')
def dados_reciclados():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            category_item.name, 
            recycle.weight_item / 1000 as weight_item,
            category_item.color_hex
        FROM recycle 
        LEFT JOIN category_item ON recycle.category_id = category_item.id;
    """)
    resultados = cursor.fetchall()

    from collections import defaultdict
    categoria_peso = defaultdict(float)
    cores = {}

    for nome, peso, cor in resultados:
        categoria_peso[nome] += peso
        cores[nome] = cor  # salva a cor da categoria

    labels = list(categoria_peso.keys())
    series = [round(categoria_peso[label], 2) for label in labels]
    colors = [cores[label] for label in labels]

    return jsonify({
        "labels": labels,
        "series": series,
        "colors": colors
    })


@routes.route('/first_recycle')
def first_recycle():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Utiliza a CTE para obter a categoria mais reciclada
    cursor.execute("""
WITH ranked_categories AS (
SELECT 
    recycle.category_id,
    SUM(recycle.weight_item) AS total_weight,
    ROW_NUMBER() OVER (ORDER BY SUM(recycle.weight_item) DESC) AS `rank`
FROM recycle
GROUP BY recycle.category_id
)
SELECT 
    category_item.name,
    recycle.date_recycle,
    recycle.weight_item,
    category_item.color_hex
FROM recycle
JOIN ranked_categories ON recycle.category_id = ranked_categories.category_id
JOIN category_item ON recycle.category_id = category_item.id
WHERE ranked_categories. `rank`= 1;
    """)

    rows = cursor.fetchall()

    # Extrair nome da categoria e cor (todas as linhas terão os mesmos valores)
    category_name = rows[0][0] if rows else "Categoria"
    color_hex = rows[0][3] if rows else "#cccccc"

    # Agrupar os dados por data
    from collections import defaultdict
    data_por_dia = defaultdict(float)
    for _, data, peso, _ in rows:
        data_por_dia[data.date()] += peso

    # Ordenar por data e preparar os dados
    labels = sorted(data_por_dia.keys())
    series = [round(data_por_dia[data] / 1000, 2) for data in labels]  # converter para Kg
    labels = [data.isoformat() for data in labels]

    # Peso total
    total_peso = round(sum(series), 2)

    return jsonify({
        "labels": labels,
        "series": series,
        "category": category_name,
        "color": color_hex,
        "total": total_peso
    })


@routes.route('/second_recycle')
def second_recycle():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Utiliza a CTE para obter a categoria mais reciclada
    cursor.execute("""
WITH ranked_categories AS (
SELECT 
    recycle.category_id,
    SUM(recycle.weight_item) AS total_weight,
    ROW_NUMBER() OVER (ORDER BY SUM(recycle.weight_item) DESC) AS `rank`
FROM recycle
GROUP BY recycle.category_id
)
SELECT 
    category_item.name,
    recycle.date_recycle,
    recycle.weight_item,
    category_item.color_hex
FROM recycle
JOIN ranked_categories ON recycle.category_id = ranked_categories.category_id
JOIN category_item ON recycle.category_id = category_item.id
WHERE ranked_categories. `rank`= 2;
    """)

    rows = cursor.fetchall()

    # Extrair nome da categoria e cor (todas as linhas terão os mesmos valores)
    category_name = rows[0][0] if rows else "Categoria"
    color_hex = rows[0][3] if rows else "#cccccc"

    # Agrupar os dados por data
    from collections import defaultdict
    data_por_dia = defaultdict(float)
    for _, data, peso, _ in rows:
        data_por_dia[data.date()] += peso

    # Ordenar por data e preparar os dados
    labels = sorted(data_por_dia.keys())
    series = [round(data_por_dia[data] / 1000, 2) for data in labels]  # converter para Kg
    labels = [data.isoformat() for data in labels]

    # Peso total
    total_peso = round(sum(series), 2)

    return jsonify({
        "labels": labels,
        "series": series,
        "category": category_name,
        "color": color_hex,
        "total": total_peso
    })

@routes.route('/third_recycle')
def third_recycle():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Utiliza a CTE para obter a categoria mais reciclada
    cursor.execute("""
WITH ranked_categories AS (
SELECT 
    recycle.category_id,
    SUM(recycle.weight_item) AS total_weight,
    ROW_NUMBER() OVER (ORDER BY SUM(recycle.weight_item) DESC) AS `rank`
FROM recycle
GROUP BY recycle.category_id
)
SELECT 
    category_item.name,
    recycle.date_recycle,
    recycle.weight_item,
    category_item.color_hex
FROM recycle
JOIN ranked_categories ON recycle.category_id = ranked_categories.category_id
JOIN category_item ON recycle.category_id = category_item.id
WHERE ranked_categories. `rank`= 3;
    """)

    rows = cursor.fetchall()

    # Extrair nome da categoria e cor (todas as linhas terão os mesmos valores)
    category_name = rows[0][0] if rows else "Categoria"
    color_hex = rows[0][3] if rows else "#cccccc"

    # Agrupar os dados por data
    from collections import defaultdict
    data_por_dia = defaultdict(float)
    for _, data, peso, _ in rows:
        data_por_dia[data.date()] += peso

    # Ordenar por data e preparar os dados
    labels = sorted(data_por_dia.keys())
    series = [round(data_por_dia[data] / 1000, 2) for data in labels]  # converter para Kg
    labels = [data.isoformat() for data in labels]

    # Peso total
    total_peso = round(sum(series), 2)

    return jsonify({
        "labels": labels,
        "series": series,
        "category": category_name,
        "color": color_hex,
        "total": total_peso
    })


@routes.route('/peso_por_categoria_data')
def peso_por_categoria_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            category_item.name,
            category_item.color_hex,
            DATE(recycle.date_recycle) as data,
            SUM(recycle.weight_item)/1000.0 as peso_kg
        FROM recycle
        JOIN category_item ON recycle.category_id = category_item.id
        GROUP BY category_item.name, category_item.color_hex, DATE(recycle.date_recycle)
        ORDER BY data ASC;
    """)
    rows = cursor.fetchall()

    from collections import defaultdict
    import datetime

    categorias = defaultdict(lambda: defaultdict(float))
    cores = {}

    # Organiza os dados por categoria e por data
    for nome, cor, data, peso in rows:
        categorias[nome][data] += peso
        cores[nome] = cor

    # Define todas as datas únicas em ordem
    todas_datas = sorted({data for cat in categorias.values() for data in cat})
    labels = [data.isoformat() for data in todas_datas]

    # Constrói as series no formato esperado pelo ApexCharts
    series = []
    for categoria, pesos_por_data in categorias.items():
        serie = {
            "name": categoria,
            "data": [round(pesos_por_data.get(data, 0), 2) for data in todas_datas]
        }
        series.append(serie)

    return jsonify({
        "labels": labels,
        "series": series,
        "colors": [cores[nome] for nome in categorias.keys()]
    })


@routes.route('/verificar-email', methods=['POST'])
def verificar_email():
    data = request.get_json()
    email_destino = data.get('email')
    user_info = session.get('user_info')

    if not user_info or not user_info.get('id'):
        return jsonify({"erro": "Usuário não autenticado"}), 401

    id_remetente = user_info['id']

    # Conexão com o banco de dados
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifica se o e-mail existe
    cursor.execute("SELECT id, name, status FROM users WHERE email = %s", (email_destino,))
    usuario_destino = cursor.fetchone()

    if not usuario_destino:
        conn.close()
        return jsonify({"existe": False, "mensagem": "Este e-mail não está cadastrado no sistema."})

    id_destinatario = usuario_destino['id']
    nome_remetente = user_info['name']

    # Verifica se já existe uma solicitação de amizade com status 'Solicitado'
    cursor.execute("""
        SELECT * FROM user_friendship
        WHERE (requesting_user_id = %s AND approver_user_id = %s)
        OR (requesting_user_id = %s AND approver_user_id = %s)
    """, (id_remetente, id_destinatario, id_destinatario, id_remetente))

    amizade_existente = cursor.fetchone()

    if amizade_existente:
        if amizade_existente['status'] == 'Solicitado':
            conn.close()
            return jsonify({"existe": True, "mensagem": "Convite já enviado. A solicitação de amizade está pendente."})

        elif amizade_existente['status'] == 'Aceito':
            conn.close()
            return jsonify({"existe": True, "mensagem": "Você já são amigos!"})

    # Caso não tenha amizade ou convite pendente, insere amizade
    cursor.execute("""
        INSERT INTO user_friendship (requesting_user_id, approver_user_id, status)
        VALUES (%s, %s, 'Solicitado')
    """, (id_remetente, id_destinatario))

    # Insere notificação para o destinatário
    cursor.execute("""
        INSERT INTO user_notification (user_id, type_notification, message)
        VALUES (%s, 'Convite de amizade', %s)
    """, (id_destinatario, f"{nome_remetente} te enviou um convite de amizade."))

    conn.commit()

    # Fechar conexão
    cursor.close()
    conn.close()

    return jsonify({"existe": True, "mensagem": "Convite de amizade enviado com sucesso!"})

@routes.route('/AddFriend', methods=['GET'])
def solicitacoes_pendentes():
    print("Rota /solicitacoes acessada")
    user_info = session.get('user_info')

    if not user_info or not user_info.get('id'):
        return jsonify({"erro": "Usuário não autenticado"}), 401

    id_usuario = user_info['id']

    # Conexão com o banco de dados
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Consulta para pegar solicitações pendentes em que o usuário logado é o approver (quem pode aprovar)
    cursor.execute("""
        SELECT u.id, u.name, uf.status, uf.date_friend
        FROM users u
        JOIN user_friendship uf ON (u.id = uf.requesting_user_id)
        WHERE uf.approver_user_id = %s
        AND uf.status = 'Solicitado'
    """, (id_usuario,))

    solicitacoes = cursor.fetchall()
    print(f"Solicitações pendentes: {solicitacoes}")
    cursor.close()
    conn.close()

    # Retorna as solicitações pendentes
    return render_template('AddFriend.html', solicitacao=solicitacoes)










