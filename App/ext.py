from flask import Blueprint
from flask_migrate import Migrate
from flask_session import Session
from App.models import db

blue=Blueprint('admin',__name__)


def init_ext(app):
    Session(app=app)
    db.init_app(app=app)
    app.register_blueprint(blueprint=blue)
    migrate = Migrate()
    migrate.init_app(app=app,db=db)




