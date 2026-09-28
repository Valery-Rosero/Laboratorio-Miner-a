"""Utilidades comunes para entrenar, evaluar, graficar y exportar los
modelos de regresión lineal múltiple de los tres ejercicios del laboratorio.
"""

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score, KFold

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
PLOTS_DIR = BASE_DIR / "graficas"
MODELS_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)


def entrenar_y_evaluar(df, features, target, nombre_ejercicio, random_state=42):
    """Divide en train/test, entrena una regresión lineal múltiple,
    calcula métricas en train y test (para detectar sobreajuste) y
    valida con validación cruzada de 5 folds sobre todo el dataset.
    """
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_train_pred = modelo.predict(X_train)
    y_test_pred = modelo.predict(X_test)

    metrics = {
        "train": {
            "MSE": mean_squared_error(y_train, y_train_pred),
            "RMSE": np.sqrt(mean_squared_error(y_train, y_train_pred)),
            "R2": r2_score(y_train, y_train_pred),
        },
        "test": {
            "MSE": mean_squared_error(y_test, y_test_pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, y_test_pred)),
            "R2": r2_score(y_test, y_test_pred),
        },
    }

    kfold = KFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_scores = cross_val_score(LinearRegression(), X, y, cv=kfold, scoring="r2")
    metrics["cv_r2_mean"] = cv_scores.mean()
    metrics["cv_r2_std"] = cv_scores.std()

    print(f"\n===== {nombre_ejercicio} =====")
    print(f"Coeficientes: {dict(zip(features, modelo.coef_.round(4)))}")
    print(f"Intercepto: {modelo.intercept_:.4f}")
    print(f"Train -> MSE: {metrics['train']['MSE']:.3f} | RMSE: {metrics['train']['RMSE']:.3f} | R2: {metrics['train']['R2']:.4f}")
    print(f"Test  -> MSE: {metrics['test']['MSE']:.3f} | RMSE: {metrics['test']['RMSE']:.3f} | R2: {metrics['test']['R2']:.4f}")
    print(f"CV(5) R2: {metrics['cv_r2_mean']:.4f} +/- {metrics['cv_r2_std']:.4f}")

    gap = metrics["train"]["R2"] - metrics["test"]["R2"]
    print(f"Diferencia R2 train-test (indicador de sobreajuste): {gap:.4f}")
    if abs(gap) < 0.05 and metrics["test"]["R2"] > 0.90:
        print("-> Modelo con buen ajuste y SIN sobreajuste (R2 test > 0.90, gap < 0.05).")
    else:
        print("-> Revisar: gap alto o R2 test insuficiente.")

    return modelo, metrics, (X_train, X_test, y_train, y_test)


def guardar_modelo(modelo, features, target, nombre_archivo, metrics=None):
    """Guarda el modelo junto con metadatos (features, target y métricas) usando joblib."""
    payload = {"modelo": modelo, "features": features, "target": target, "metrics": metrics}
    ruta = MODELS_DIR / nombre_archivo
    joblib.dump(payload, ruta)
    print(f"Modelo exportado en: {ruta}")
    return ruta


def graficar_relaciones(df, features, target, nombre_ejercicio, prefijo_archivo):
    """Genera un scatter plot con línea de tendencia por cada variable
    independiente frente a la variable dependiente."""
    n = len(features)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, feat in zip(axes, features):
        ax.scatter(df[feat], df[target], alpha=0.4, s=15, color="#4C72B0")
        coef = np.polyfit(df[feat], df[target], 1)
        x_line = np.linspace(df[feat].min(), df[feat].max(), 100)
        ax.plot(x_line, np.polyval(coef, x_line), color="#C44E52", linewidth=2)
        corr = df[feat].corr(df[target])
        ax.set_xlabel(feat)
        ax.set_ylabel(target)
        ax.set_title(f"{feat} vs {target}\n(corr={corr:.2f})")

    fig.suptitle(f"Relaciones de variables independientes con {target} - {nombre_ejercicio}")
    fig.tight_layout()
    ruta = PLOTS_DIR / f"{prefijo_archivo}_relaciones.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    print(f"Gráfica guardada en: {ruta}")
    return ruta


def graficar_correlacion(df, nombre_ejercicio, prefijo_archivo):
    """Mapa de calor de correlación entre todas las variables numéricas."""
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black", fontsize=8)
    fig.colorbar(im, ax=ax, label="Correlación")
    ax.set_title(f"Matriz de correlación - {nombre_ejercicio}")
    fig.tight_layout()
    ruta = PLOTS_DIR / f"{prefijo_archivo}_correlacion.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    print(f"Gráfica guardada en: {ruta}")
    return ruta
