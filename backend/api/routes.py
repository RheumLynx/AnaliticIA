from flask import Blueprint, jsonify, request, current_app
from api.services import pdf_service, openai_service
from api.models import LabResult, Analysis
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf'}

# Lista para almacenar el historial de análisis (en una aplicación real, usarías una base de datos)
analysis_history = []

# Definir el Blueprint
api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo en la solicitud."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            
            # Extraer texto del PDF
            text = pdf_service.extract_text_from_pdf(filepath)
            
            # Extraer valores relevantes
            lab_result = pdf_service.extract_lab_values(text)
            
            if not lab_result:
                return jsonify({"error": "No se pudieron extraer los valores del PDF"}), 400
            
            # Interpretar resultados con OpenAI
            analysis = openai_service.interpret_lab_results(lab_result)
            
            if analysis is None:
                return jsonify({"error": "Error al interpretar los resultados"}), 500
            
            # Guardar el análisis en el historial
            analysis_history.append(analysis)
            
            return jsonify(analysis.to_dict()), 200
        except Exception as e:
            print(f"Error en analyze_pdf: {e}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            # Limpiar el archivo después de procesarlo
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

@api_bp.route('/analysis-history', methods=['GET'])
def get_analysis_history():
    return jsonify([analysis.to_dict() for analysis in analysis_history]), 200

