# Laboratorio Minería de Datos — Regresión lineal múltiple (CRISP-DM)

## Requisitos
Python 3.12 (ya instalado) y las librerías de `requirements.txt` (ya instaladas).

```bash
pip install -r requirements.txt
```

## Pasos para reproducir todo desde cero

```bash
# 1. Generar los datasets sintéticos
python src/generar_datasets.py

# 2. Entrenar, evaluar, graficar y exportar cada modelo
python src/ejercicio1_dolar.py
python src/ejercicio2_glucosa.py
python src/ejercicio3_energia.py

# 3. Levantar la interfaz web de predicción
streamlit run app.py

# 4. (Opcional) Regenerar el informe académico en PDF (portada APA, Times New Roman)
python src/generar_informe_pdf.py
```

## Resultados obtenidos (R² en conjunto de prueba)

| Ejercicio | R² Test | R² CV (5-fold) | Sobreajuste |
|---|---|---|---|
| Dólar | 0.9132 | 0.9249 ± 0.0132 | No |
| Glucosa | 0.9352 | 0.9270 ± 0.0095 | No |
| Energía | 0.9340 | 0.9372 ± 0.0105 | No |

Detalle completo de interpretación de coeficientes, métricas y conclusiones en [`INFORME.pdf`](INFORME.pdf) (informe académico formal, portada APA, Times New Roman).

## Estructura

- `data/` — datasets CSV
- `src/` — scripts de generación de datos, de cada ejercicio y del informe PDF
- `models/` — modelos exportados (`.pkl`, cargados con `joblib`, incluyen métricas)
- `graficas/` — visualizaciones generadas
- `.streamlit/config.toml` — tema visual (paleta navy / crema / dorado)
- `app.py` — interfaz web Streamlit (selecciona ejercicio, ingresa datos, predice)
- `INFORME.pdf` — informe académico formal (portada APA, Times New Roman)
