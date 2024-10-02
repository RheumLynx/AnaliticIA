from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend')
    CORS(app)  # Habilitar CORS para toda la aplicación
    app.config.from_object(config_class)
    
    # Definir la ruta de la carpeta 'uploads'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Crear la carpeta 'uploads' si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Registrar los blueprints o rutas de la API
    from api.routes import api_bp
    app.register_blueprint(api_bp)

    # Servir el frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # Establecer debug=False en producción

# Crear una instancia de la aplicación para Gunicorn
app = create_app()
