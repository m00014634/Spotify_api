from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# setting flask
app = Flask(__name__)

# Database connection
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
db.init_app(app)


from users import bp as users_bp


app.register_blueprint(users_bp)

@app.route('/')
def hello():
    return 'Hello, World!'


app.run()