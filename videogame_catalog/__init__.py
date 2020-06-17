import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    _register_auth_blueprint(app)

    from . import catalog
    app.register_blueprint(catalog.bp)
    app.add_url_rule('/', endpoint='index')

    return app


def _register_auth_blueprint(app):
    from . import auth

    app.register_blueprint(auth.bp)
