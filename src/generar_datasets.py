"""
Generación de los datasets sintéticos para el Laboratorio de Minería de Datos.

Se crean relaciones LINEALES con ruido gaussiano calibrado para que el
R^2 poblacional de cada relación quede alrededor de 0.93, lo que en la
práctica (con ruido muestral) produce modelos con R^2 > 0.90 tanto en
entrenamiento como en prueba, sin sobreajuste (la diferencia entre R^2
de train y test se mantiene pequeña).

Ejecutar:
    python src/generar_datasets.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

RANDOM_STATE = 42
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def agregar_ruido(signal: np.ndarray, target_r2: float, rng: np.random.Generator) -> np.ndarray:
    """Agrega ruido gaussiano a `signal` calibrado para lograr aproximadamente
    `target_r2` como R^2 poblacional (var_señal / (var_señal + var_ruido))."""
    var_signal = signal.var()
    var_noise = var_signal * (1 - target_r2) / target_r2
    noise = rng.normal(0, np.sqrt(var_noise), size=len(signal))
    return signal + noise


# ---------------------------------------------------------------------------
# Ejercicio 1: Precio del dólar
# ---------------------------------------------------------------------------
def generar_dolar(n=450, target_r2=0.93, seed=RANDOM_STATE):
    rng = np.random.default_rng(seed)

    dia = np.arange(1, n + 1)
    # Inflacion y Tasa_interes se generan independientes de Dia para evitar
    # multicolinealidad (que el día "explique" indirectamente a las otras variables).
    inflacion = np.clip(rng.normal(6, 1.5, n), 1.5, 9.5)         # % diaria
    tasa_interes = np.clip(rng.normal(7, 1.8, n), 3, 13)         # % diaria

    # Relación lineal real: el dólar sube con el tiempo y la inflación,
    # y baja cuando sube la tasa de interés (atrae capital, fortalece la moneda local).
    señal = 4000 + 1.2 * dia + 140 * inflacion - 75 * tasa_interes
    precio_dolar = agregar_ruido(señal, target_r2, rng)

    df = pd.DataFrame({
        "Dia": dia,
        "Inflacion": inflacion.round(3),
        "Tasa_interes": tasa_interes.round(3),
        "Precio_Dolar": precio_dolar.round(2),
    })
    df.to_csv(DATA_DIR / "dolar_data.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# Ejercicio 2: Niveles de glucosa en sangre
# ---------------------------------------------------------------------------
def generar_glucosa(n=450, target_r2=0.93, seed=RANDOM_STATE + 1):
    rng = np.random.default_rng(seed)

    edad = rng.uniform(18, 75, n)
    imc = rng.uniform(17, 40, n)
    actividad_fisica = rng.uniform(0, 12, n)  # horas semanales

    # Relación lineal real: mayor edad e IMC -> más glucosa; más actividad -> menos glucosa.
    señal = 55 + 0.55 * edad + 1.9 * imc - 3.2 * actividad_fisica
    nivel_glucosa = agregar_ruido(señal, target_r2, rng)
    nivel_glucosa = np.clip(nivel_glucosa, 60, None)

    df = pd.DataFrame({
        "Edad": edad.round(1),
        "IMC": imc.round(2),
        "Actividad_Fisica": actividad_fisica.round(2),
        "Nivel_Glucosa": nivel_glucosa.round(2),
    })
    df.to_csv(DATA_DIR / "glucosa_data.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# Ejercicio 3: Consumo de energía eléctrica
# ---------------------------------------------------------------------------
def generar_energia(n=450, target_r2=0.93, seed=RANDOM_STATE + 2):
    rng = np.random.default_rng(seed)

    temperatura = rng.uniform(-5, 40, n)
    hora = rng.integers(1, 25, n)          # 1 a 24
    dia_semana = rng.integers(1, 8, n)     # 1=Lunes ... 7=Domingo

    # Relación lineal real: más consumo con temperaturas extremas (aire acondicionado),
    # en horas de mayor actividad, y algo menor en fin de semana (dia_semana alto).
    señal = 15 + 1.3 * temperatura + 0.9 * hora - 1.6 * dia_semana
    consumo_energia = agregar_ruido(señal, target_r2, rng)
    consumo_energia = np.clip(consumo_energia, 5, None)

    df = pd.DataFrame({
        "Temperatura": temperatura.round(2),
        "Hora": hora,
        "Dia_Semana": dia_semana,
        "Consumo_Energia": consumo_energia.round(2),
    })
    df.to_csv(DATA_DIR / "energia_data.csv", index=False)
    return df


if __name__ == "__main__":
    df1 = generar_dolar()
    df2 = generar_glucosa()
    df3 = generar_energia()
    print("Datasets generados en:", DATA_DIR)
    print("dolar_data.csv   ->", df1.shape)
    print("glucosa_data.csv ->", df2.shape)
    print("energia_data.csv ->", df3.shape)
