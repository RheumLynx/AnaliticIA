from flask import Flask
from flask_cors import CORS
from api import create_api
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)  # Esto habilita CORS para toda la aplicación
    app.config.from_object(config_class)
    
    # Definir la ruta de la carpeta 'uploads'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Crear la carpeta 'uploads' si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    create_api(app)

    @app.route('/')
    def index():
        return "Bienvenido a la API de análisis de resultados de laboratorio"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# Crear una instancia de la aplicación para Gunicorn
app = create_app()
    