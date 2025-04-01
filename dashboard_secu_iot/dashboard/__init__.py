import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = os.getenv("SECRET_KEY"),
        DATABASE = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'dbname': os.getenv("DB_NAME"),
            'port': os.getenv("DB_PORT")
        }
    )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    return app
