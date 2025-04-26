from flask import Flask # type: ignore
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
app.config['SECRET_KEY'] = 'devkey'

if __name__ == '__main__':
    app.run(debug=True)