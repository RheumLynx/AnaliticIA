from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend')
    CORS(app)  # Habilitar CORS para toda la aplicación
    app.config.from_object(config_class)
    
    # Definir la ruta de la carpeta 'uploads'
    app_root = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(app_root, 'uploads')
    
    # Crear la carpeta 'uploads' si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Importar y registrar el blueprint con prefijo '/api'
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Servir el frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app

# Crear una instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Establecer debug=False en producción


