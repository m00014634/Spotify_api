from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# setting flask
app = Flask(__name__)

# Database connection
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
app.config['UPLOAD_FOLDER'] = 'media'
db.init_app(app)
migrate = Migrate(app,db)

from users import bp as users_bp
from artists import bp as artists_bp
from songs import bp as songs_bp

app.register_blueprint(users_bp)
app.register_blueprint(artists_bp)
app.register_blueprint(songs_bp)


@app.route('/')
def hello():
    return 'Hello, World!'


app.run()