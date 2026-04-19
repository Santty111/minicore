from flask import Flask
from utils.database import db
from flask_migrate import Migrate
import os
import sqlite3

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)
_db_file = os.path.join(app.instance_path, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(_db_file).replace('\\', '/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev')

db.init_app(app)
migrate = Migrate(app, db)

from controllers.venta_controller import main_blueprint
app.register_blueprint(main_blueprint)


def init_db():
    db_path = os.path.join(app.instance_path, 'db.sqlite3')
    need_init = not os.path.exists(db_path)
    if not need_init:
        try:
            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='vendedores'"
                ).fetchone()
                need_init = row is None
        except sqlite3.Error:
            need_init = True
    if need_init:
        with sqlite3.connect(db_path) as conn:
            with open(os.path.join(os.path.dirname(__file__), 'data.sql'), encoding='utf-8') as f:
                conn.executescript(f.read())


with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
