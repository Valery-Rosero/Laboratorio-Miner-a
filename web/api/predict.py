"""
Función serverless (Flask) desplegada en Vercel que expone la predicción
de los tres modelos de regresión lineal múltiple entrenados en el
laboratorio (ver /src en la raíz del repositorio).

Ruta: POST /api/predict
Body: {"ejercicio": "Dolar" | "Glucosa" | "Energia", "valores": {feature: valor, ...}}
"""

from pathlib import Path

import joblib
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
_MODELOS_CACHE = {}

CONFIG = {
    "Dolar": {
        "archivo": "modelo_dolar.pkl",
        "features": ["Dia", "Inflacion", "Tasa_interes"],
        "target": "Precio_Dolar",
        "unidad": "COP",
    },
    "Glucosa": {
        "archivo": "modelo_glucosa.pkl",
        "features": ["Edad", "IMC", "Actividad_Fisica"],
        "target": "Nivel_Glucosa",
        "unidad": "mg/dL",
    },
    "Energia": {
        "archivo": "modelo_energia.pkl",
        "features": ["Temperatura", "Hora", "Dia_Semana"],
        "target": "Consumo_Energia",
        "unidad": "kWh",
    },
}


def cargar_modelo(nombre_ejercicio):
    if nombre_ejercicio not in _MODELOS_CACHE:
        cfg = CONFIG[nombre_ejercicio]
        payload = joblib.load(BASE_DIR / "models" / cfg["archivo"])
        _MODELOS_CACHE[nombre_ejercicio] = payload["modelo"]
    return _MODELOS_CACHE[nombre_ejercicio]


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    ejercicio = data.get("ejercicio")
    valores = data.get("valores", {})

    if ejercicio not in CONFIG:
        return jsonify({"error": "Ejercicio no válido"}), 400

    cfg = CONFIG[ejercicio]
    try:
        entrada = [[float(valores[f]) for f in cfg["features"]]]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Valores de entrada inválidos o incompletos"}), 400

    modelo = cargar_modelo(ejercicio)
    prediccion = float(modelo.predict(entrada)[0])

    return jsonify({
        "prediccion": prediccion,
        "target": cfg["target"],
        "unidad": cfg["unidad"],
        "coeficientes": dict(zip(cfg["features"], [float(c) for c in modelo.coef_])),
        "intercepto": float(modelo.intercept_),
    })


@app.route("/api/predict", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ejercicios": list(CONFIG.keys())})
