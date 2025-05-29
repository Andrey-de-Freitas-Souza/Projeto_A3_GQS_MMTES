from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session,redirect,url_for,make_response,g
import os
from werkzeug.utils import secure_filename
from models.User import User
from ConnectionDB import get_db_connection
from datetime import datetime,timedelta

routes = Blueprint('routes', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@routes.route('/')
def index():
    session.clear()
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@routes.route('/home')
@login_required
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
        # Verifica se a data não é None antes de tentar formatá-la
        if linha['date_recycle']:
            data_recycle = linha['date_recycle']  # A data original
            linha['date_recycle'] = data_recycle.strftime('%d/%m/%Y')  # Formata a data
        else:
            linha['date_recycle'] = 'Data não disponível'  # Ou qualquer outro valor padrão
            data_recycle = None  # Define para None quando não houver data

        # Verificando se a data é hoje
        if data_recycle and data_recycle.date() == hoje_data.date():
            hoje.append(linha)
        # Verificando se a data é ontem
        elif data_recycle and data_recycle.date() == ontem_data.date():
            ontem.append(linha)
        # Verificando se a data está dentro da mesma semana
        elif data_recycle and inicio_semana.date() <= data_recycle.date() <= fim_semana.date():
            ainda_esta_semana.append(linha)
        else:
            periodo_anterior.append(linha)

    cursor.close()
    conn.close()

    # Passar os dados para o template
    return render_template('home.html', hoje=hoje, ontem=ontem, ainda_esta_semana=ainda_esta_semana, periodo_anterior=periodo_anterior)


import os

@routes.route('/MyInfo')
@login_required
def MyInfo():
    user_info = session.get('user_info')  # Recupera as informações salvas na sessão
    user_id = user_info['id']             # Pega o ID do usuário logado

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, email, phone, address, points, birth_date
        FROM users
        WHERE id = %s
    """, (user_id,))

    dados_usuario = cursor.fetchall()
    conn.close()

    # Verifica se existe imagem personalizada
    caminho_imagem = os.path.join('static', 'Images', 'Profiles', f"{user_id}.jpg")
    if os.path.exists(caminho_imagem):
        img_url = f"Images/Profiles/{user_id}.jpg"
    else:
        img_url = "Images/default_profile.jpg"

    # Renderiza a página com os dados do usuário e a URL da imagem
    return render_template('MyInfo.html', usuario=dados_usuario, img_url=img_url)


@routes.route('/Points')
@login_required
def Points():
    return render_template('Points.html')


@routes.route('/Graphics')
@login_required
def Graphics():
    return render_template('Graphics.html')

@routes.route('/Contents')
@login_required
def Contents():
    return render_template('Content.html')

@routes.route('/help')
@login_required
def help():
    return render_template('help.html')

@routes.route('/Classification')
@login_required
def Classification():
    print("Rota /AddFriend acessada")
    user_info = session.get('user_info')

    if not user_info or not user_info.get('id'):
        return jsonify({"erro": "Usuário não autenticado"}), 401

    id_usuario = user_info['id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Amigos aprovados
    cursor.execute("""
        SELECT 
    all_users.id, 
    all_users.name, 
    all_users.points,
    ROW_NUMBER() OVER (ORDER BY all_users.points DESC) AS ranking
FROM (
    -- Amigos aprovados
    SELECT 
        u.id, 
        u.name, 
        u.points
    FROM user_friendship uf
    JOIN users u ON (
        (uf.requesting_user_id = u.id AND uf.approver_user_id = %s) OR
        (uf.approver_user_id = u.id AND uf.requesting_user_id = %s)
    )
    WHERE uf.status = 'Aprovado'

    UNION

    -- Usuário logado
    SELECT 
        u.id, 
        u.name, 
        u.points
    FROM users u
    WHERE u.id = %s
) AS all_users
ORDER BY all_users.points DESC;
    """, (id_usuario, id_usuario,id_usuario))

    amigos = cursor.fetchall()
    print(f"Amigos aprovados: {amigos}")

    # Busca as solicitações pendentes
    solicitacoes = solicitacoes_pendentes(id_usuario)
    print(f"Solicitações: {solicitacoes}")
   
    return render_template('Classification.html',amigos=amigos) 



@routes.route('/register', methods=['POST'])
def register():
    print('Rota /register foi chamada!')
    print(request.form)

    # Coletando os dados do formulário
    name = request.form['name']
    birth_date = request.form['birth_date']

    # Tentando converter a data para o formato correto
    try:
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y").date()
    except ValueError:
        return jsonify({'message': 'A data de nascimento está em um formato incorreto. Use o formato DD/MM/YYYY.'}), 400

    address = request.form['address']
    email = request.form['email']
    phone = request.form['ddi'] + request.form['phone']
    password = request.form['senha']
    registration_date = datetime.today()

    # Definindo o status e a data de último login, caso necessário
    status = 'ativo'  # Isso pode variar dependendo da lógica do seu sistema
    last_login_date = None  # Você pode definir isso conforme necessário

    # Criando o objeto User
    user = User(
        id=None,
        name=name,
        email=email,
        password=password,  # A senha será criptografada dentro da função cadastro
        phone=phone,
        address=address,
        birth_date=birth_date,
        points=0,  # Pode ser um valor padrão se não estiver sendo enviado
        registration_date=registration_date,
        status=status,
        last_login_date=last_login_date
    )

    # Chama a função cadastro que vai criptografar a senha e salvar no banco
    try:
        result = user.cadastro()  # Chama a função de cadastro
        return jsonify(result), 201  # Resposta de sucesso
    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro: {str(e)}'}), 500

@routes.route('/check-email', methods=['GET'])
def check_email():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'message': 'O e-mail é obrigatório.'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()

        
        cursor.close()
        conn.close()

        if result['count'] > 0:
            return jsonify({'emailExists': True}), 200
        else:
            return jsonify({'emailExists': False}), 200

    except Exception as e:
        print(f"Erro ao verificar o e-mail: {e}")
        return jsonify({'message': 'Erro ao verificar o e-mail. Tente novamente mais tarde.'}), 500

@routes.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        result = User.login(email, password)

        # Verifica o tipo de resposta e retorna a resposta correspondente
        if 'message' in result and result['message'] == 'Login bem-sucedido':
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        print('Erro no login:', e)
        return jsonify({'error': 'Erro interno no servidor'}), 500


@routes.route('/get-itens')
@login_required
def get_itens():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name FROM category_item')
    itens = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(itens)    

@routes.route('/get-collection-points', methods=['GET'])
@login_required
def get_collection_points():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM collection_point")
    points = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(points)

@routes.route('/cadastrar-reciclagem', methods=['POST'])
@login_required
def cadastrar_reciclagem():
    data = request.get_json()
    user_info = session.get('user_info')
    if not user_info:
        return {"message": "Usuário não autenticado"}, 401

    user_id = user_info['id']  # Corrigido aqui
    date_recycle = datetime.now()
    category_id = data.get('category')
    point_id = data.get('collection_point')
    if point_id is None:
        point_id = 0
        
    try:
        weight_item = float(data.get('peso'))  # Corrigido aqui
    except (TypeError, ValueError):
        return jsonify({"message": "Peso inválido."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Buscar score por quilo da categoria
        cursor.execute("SELECT score_by_kilo FROM category_item WHERE id = %s", (category_id,))
        resultado = cursor.fetchone()
        if not resultado:
            return jsonify({"message": "Categoria não encontrada"}), 404

        score_by_kilo = resultado[0]
        pontos_obtidos = (weight_item / 1000) * score_by_kilo  # Corrigido aqui

        # Atualizar a pontuação do usuário
        cursor.execute("SELECT points FROM users WHERE id = %s", (user_id,))
        score_atual = cursor.fetchone()[0]
        novo_score = score_atual + pontos_obtidos

        cursor.execute("UPDATE users SET points = %s WHERE id = %s", (novo_score, user_id))

        # Inserir a reciclagem
        cursor.execute("""
            INSERT INTO recycle (user_id, category_id, weight_item, point_id, date_recycle)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, category_id, weight_item, point_id, date_recycle))

        conn.commit()
        return jsonify({"message": "Reciclagem cadastrada com sucesso!", "pontos_obtidos": pontos_obtidos})
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar reciclagem:", e)
        return jsonify({"message": "Erro ao cadastrar reciclagem."}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/recycle_by_category')
@login_required
def dados_reciclados():
    user_info = session.get('user_info')
    id_user = user_info['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            category_item.name, 
            recycle.weight_item / 1000 as weight_item,
            category_item.color_hex
        FROM recycle 
        LEFT JOIN category_item ON recycle.category_id = category_item.id
        where user_id = %s;
    """, (id_user,))
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
@login_required
def first_recycle():
    user_info = session.get('user_info')
    id_user = user_info['id']
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
where user_id = %s
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
    """, (id_user,))

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
@login_required
def second_recycle():
    user_info = session.get('user_info')
    id_user = user_info['id']
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
where user_id = %s
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
    """, (id_user,))

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
@login_required
def third_recycle():
    user_info = session.get('user_info')
    id_user = user_info['id']
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
where user_id = %s
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
    """, (id_user,))

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
@login_required
def peso_por_categoria_data():
    user_info = session.get('user_info')
    id_user = user_info['id']
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
        where user_id = %s
        GROUP BY category_item.name, category_item.color_hex, DATE(recycle.date_recycle)
        ORDER BY data ASC;
    """, (id_user,))
    rows = cursor.fetchall()

    from collections import defaultdict

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
@login_required
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
@login_required
def listar_amigos():
    if 'user_info' not in session:
        return redirect('/')
    print("Rota /AddFriend acessada")
    user_info = session.get('user_info')

    if not user_info or not user_info.get('id'):
        return jsonify({"erro": "Usuário não autenticado"}), 401

    id_usuario = user_info['id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Amigos aprovados
    cursor.execute("""
        SELECT u.id, u.name, uf.date_friend
        FROM user_friendship uf
        JOIN users u ON (
            (uf.requesting_user_id = u.id AND uf.approver_user_id = %s) OR
            (uf.approver_user_id = u.id AND uf.requesting_user_id = %s)
        )
        WHERE uf.status = 'Aprovado'
    """, (id_usuario, id_usuario))

    amigos = cursor.fetchall()
    print(f"Amigos aprovados: {amigos}")

    # Busca as solicitações pendentes
    solicitacoes = solicitacoes_pendentes(id_usuario)
    print(f"Solicitações: {solicitacoes}")

    cursor.close()
    conn.close()

    # Retorna o template com ambas as informações
    return render_template('AddFriend.html', 
                           solicitacao=solicitacoes, 
                           amigos=amigos)


def solicitacoes_pendentes(id_usuario):
    
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

    return solicitacoes

@routes.route('/desconect')
@login_required
def desconectar():
    session.clear()  # Limpa a sessão do servidor
    response = make_response("""
    <script>
        // Limpa a sessão no lado do cliente
        sessionStorage.clear();
        localStorage.clear();
        window.location.replace("/");  // Redireciona para a página de login (index.html)
    </script>
    """)
    
    # Previne cache para garantir que o usuário não consiga voltar para a página após desconectar
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

UPLOAD_FOLDER = os.path.join('static', 'Images', 'Profiles')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from PIL import Image
import io

@routes.route('/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    user_info = session.get('user_info')  # Recupera as informações do usuário logado
    user_id = user_info['id']  # Pega o ID do usuário logado

    # Verifica se o arquivo foi enviado
    if 'profile_picture' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado'})

    file = request.files['profile_picture']

    # Verifica se o arquivo tem uma extensão válida
    if file and allowed_file(file.filename):
        # Garante que o nome do arquivo é seguro
        filename = secure_filename(f"{user_id}.jpg")
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Lê a imagem e converte para JPG
        image = Image.open(file)
        if image.mode in ("RGBA", "P"):  # Se a imagem estiver com transparência (PNG), converte para RGB
            image = image.convert("RGB")

        # Salva a imagem convertida
        image.save(file_path, "JPEG")

        # Atualiza a URL da imagem no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Users
            SET picture_profile = %s
            WHERE id = %s
        """, (f"Images/Profiles/{filename}", user_id))
        conn.commit()

        # Retorna a URL da imagem
        img_url = f"Images/Profiles/{filename}"
        return jsonify({'success': True, 'img_url': img_url})

    return jsonify({'success': False, 'message': 'Extensão de arquivo inválida'})


@routes.route('/get_user_id', methods=['GET'])
def get_user_id():
    # Verifica se o usuário está logado
    if g.user:
        # Retorna o id do usuário logado como JSON
        return jsonify({'user_id': g.user['id']})
    else:
        # Caso não esteja logado, retorna um erro
        return jsonify({'error': 'Usuário não logado'}), 401


@routes.route("/notifications")
def notifications():
    user_info = session.get('user_info')  # Recupera as informações do usuário logado
    user_id = user_info['id']  # Pega o ID do usuário logado
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
    "SELECT * FROM user_notification WHERE user_id = %s AND is_read = 0 ORDER BY date_notification DESC",
    (user_id,)
)
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("notifications.html", notifications=notifications)

@routes.route('/mark_as_read/<int:notification_id>', methods=['POST'])
def mark_as_read(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_notification SET is_read = TRUE WHERE id = %s", (notification_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {'success': True}

@routes.route('/amizade/aceitar', methods=['POST'])
def aceitar_amizade():
    data = request.get_json()  # Obtém os dados enviados como JSON
    convite_id = data.get('convite_id')  # Recupera o id do convite
    user_info = session.get('user_info')  # Recupera as informações do usuário logado
    usuario_logado_name= user_info['name'].strip("'")
    usuario_logado_id = user_info['id']  # Obtém o ID do usuário logado
   
    if not convite_id or not usuario_logado_id:
        return jsonify({'status': 'error', 'message': 'Convite ID ou Usuário Logado não fornecido'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Atualiza o status da amizade para "Aprovado" onde o convite foi solicitado pelo usuário
        cursor.execute("""
            UPDATE user_friendship
            SET status = 'Aprovado'
            WHERE requesting_user_id = %s AND approver_user_id = %s
        """, ( convite_id, usuario_logado_id))

        conn.commit()

        # Verifique se a linha foi atualizada
        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'Convite não encontrado ou inválido'}), 404
        
        # Agora vamos inserir uma nova notificação para o solicitante
        cursor.execute("""
        INSERT INTO user_notification (user_id, type_notification, message, is_read)
        VALUES (%s, 'Convite de amizade', %s, FALSE)
    """, (convite_id, f"Seu convite de amizade para {usuario_logado_name} foi aceito!"))

        conn.commit()

        return jsonify({'status': 'success', 'message': 'Convite aceito com sucesso'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@routes.route('/amizade/recusar', methods=['POST'])
def recusar_amizade():
    data = request.get_json()
    convite_id = data.get('convite_id')
    user_info = session.get('user_info')  # Recupera as informações do usuário logado
    usuario_logado_id = user_info['id']  # Obtém o ID do usuário logado

    conn = get_db_connection()
    cursor = conn.cursor()

    # Remove o convite da tabela
    cursor.execute("""DELETE FROM user_friendship 
                        WHERE requesting_user_id = %s AND approver_user_id = %s
                        or    requesting_user_id = %s AND approver_user_id = %s"""
                   , ( convite_id, usuario_logado_id,usuario_logado_id,convite_id))
    conn.commit()
    
    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Convite recusado'})