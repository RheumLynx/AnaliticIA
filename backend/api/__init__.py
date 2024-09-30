from flask import Blueprint

api = Blueprint('api', __name__)

from api import routes

def create_api(app):
    app.register_blueprint(api, url_prefix='/api')