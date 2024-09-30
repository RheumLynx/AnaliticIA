from api.models import Analysis
import openai
from flask import current_app

def interpret_lab_results(values):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    prompt = f"""
    Analiza los siguientes resultados de laboratorio:
    PCR (Proteína C Reactiva): {values['PCR']}
    VSG (Velocidad de Sedimentación Globular): {values['VSG']}
    Factor Reumatoide (FR): {values['FR']}
    ANA (Anticuerpos Antinucleares): {values['ANA']}

    Basándote en estos resultados:
    1. Determina si cada valor es positivo o negativo.
    2. Evalúa si el paciente debe ser derivado a un reumatólogo.
    3. Proporciona una breve explicación de tu recomendación.

    Formato de respuesta:
    PCR: [Positivo/Negativo]
    VSG: [Positivo/Negativo]
    FR: [Positivo/Negativo]
    ANA: [Positivo/Negativo]
    
    Derivación a reumatólogo: [Sí/No]
    
    Explicación: [Tu explicación aquí]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente médico especializado en interpretar resultados de laboratorio relacionados con enfermedades reumáticas."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message['content']