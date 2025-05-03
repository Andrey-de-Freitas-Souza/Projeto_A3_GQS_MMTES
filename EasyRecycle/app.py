from flask import Flask,g,session # type: ignore
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
app.config['SECRET_KEY'] = 'devkey'

from types import SimpleNamespace

@app.before_request
def before_request():
    user_info = session.get('user_info')
    if user_info:
        g.user = SimpleNamespace(**user_info)
    else:
        g.user = None
        
@app.context_processor
def inject_user():
    return dict(user=g.user)

if __name__ == '__main__':
    app.run(debug=True)