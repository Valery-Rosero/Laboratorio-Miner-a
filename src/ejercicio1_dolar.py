"""
Ejercicio 1: Predicción del precio del dólar
Regresión lineal múltiple: Precio_Dolar ~ Dia + Inflacion + Tasa_interes
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from utils_modelado import entrenar_y_evaluar, guardar_modelo, graficar_relaciones, graficar_correlacion

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dolar_data.csv"

FEATURES = ["Dia", "Inflacion", "Tasa_interes"]
TARGET = "Precio_Dolar"


def main():
    df = pd.read_csv(DATA_PATH)
    print(df.describe())

    modelo, metrics, _ = entrenar_y_evaluar(df, FEATURES, TARGET, "Ejercicio 1 - Dólar")

    print("\nInterpretación de coeficientes:")
    for feat, coef in zip(FEATURES, modelo.coef_):
        signo = "aumenta" if coef > 0 else "disminuye"
        print(f"  - Por cada unidad que sube {feat}, Precio_Dolar {signo} en {abs(coef):.3f} (manteniendo las demás constantes).")

    graficar_relaciones(df, FEATURES, TARGET, "Precio del Dólar", "ejercicio1_dolar")
    graficar_correlacion(df, "Precio del Dólar", "ejercicio1_dolar")

    guardar_modelo(modelo, FEATURES, TARGET, "modelo_dolar.pkl", metrics=metrics)


if __name__ == "__main__":
    main()
