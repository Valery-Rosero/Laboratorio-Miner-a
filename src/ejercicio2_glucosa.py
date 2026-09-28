"""
Ejercicio 2: Predicción de niveles de glucosa en sangre
Regresión lineal múltiple: Nivel_Glucosa ~ Edad + IMC + Actividad_Fisica
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from utils_modelado import entrenar_y_evaluar, guardar_modelo, graficar_relaciones, graficar_correlacion

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "glucosa_data.csv"

FEATURES = ["Edad", "IMC", "Actividad_Fisica"]
TARGET = "Nivel_Glucosa"


def main():
    df = pd.read_csv(DATA_PATH)
    print(df.describe())

    modelo, metrics, _ = entrenar_y_evaluar(df, FEATURES, TARGET, "Ejercicio 2 - Glucosa")

    print("\nInterpretación de coeficientes:")
    for feat, coef in zip(FEATURES, modelo.coef_):
        signo = "aumenta" if coef > 0 else "disminuye"
        print(f"  - Por cada unidad que sube {feat}, Nivel_Glucosa {signo} en {abs(coef):.3f} (manteniendo las demás constantes).")

    # Importancia relativa de cada variable: se estandarizan las variables
    # (coef * desviación estándar de la variable) para comparar en una misma escala.
    importancias = {feat: abs(coef) * df[feat].std() for feat, coef in zip(FEATURES, modelo.coef_)}
    var_mas_importante = max(importancias, key=importancias.get)
    print("\nImportancia relativa (|coef| * desviación estándar):")
    for feat, imp in sorted(importancias.items(), key=lambda x: -x[1]):
        print(f"  - {feat}: {imp:.3f}")
    print(f"-> La variable con mayor impacto en Nivel_Glucosa es: {var_mas_importante}")

    graficar_relaciones(df, FEATURES, TARGET, "Nivel de Glucosa", "ejercicio2_glucosa")
    graficar_correlacion(df, "Nivel de Glucosa", "ejercicio2_glucosa")

    guardar_modelo(modelo, FEATURES, TARGET, "modelo_glucosa.pkl", metrics=metrics)


if __name__ == "__main__":
    main()
