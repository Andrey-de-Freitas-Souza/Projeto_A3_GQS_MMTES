from flask import Blueprint, render_template
from ConnectionDB import get_db_connection

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
    