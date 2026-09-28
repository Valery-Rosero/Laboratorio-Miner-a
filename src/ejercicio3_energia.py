"""
Ejercicio 3: Predicción del consumo de energía eléctrica
Regresión lineal múltiple: Consumo_Energia ~ Temperatura + Hora + Dia_Semana
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from utils_modelado import entrenar_y_evaluar, guardar_modelo, graficar_relaciones, graficar_correlacion

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "energia_data.csv"

FEATURES = ["Temperatura", "Hora", "Dia_Semana"]
TARGET = "Consumo_Energia"


def main():
    df = pd.read_csv(DATA_PATH)
    print(df.describe())

    # Evaluación con RMSE y R2 (entrenar_y_evaluar ya calcula ambos, además de MSE)
    modelo, metrics, _ = entrenar_y_evaluar(df, FEATURES, TARGET, "Ejercicio 3 - Energía")

    importancias = {feat: abs(coef) * df[feat].std() for feat, coef in zip(FEATURES, modelo.coef_)}
    var_mas_importante = max(importancias, key=importancias.get)
    print("\nImportancia relativa (|coef| * desviación estándar):")
    for feat, imp in sorted(importancias.items(), key=lambda x: -x[1]):
        print(f"  - {feat}: {imp:.3f}")
    print(f"-> La variable con mayor impacto en Consumo_Energia es: {var_mas_importante}")

    graficar_relaciones(df, FEATURES, TARGET, "Consumo de Energía", "ejercicio3_energia")
    graficar_correlacion(df, "Consumo de Energía", "ejercicio3_energia")

    guardar_modelo(modelo, FEATURES, TARGET, "modelo_energia.pkl", metrics=metrics)


if __name__ == "__main__":
    main()
