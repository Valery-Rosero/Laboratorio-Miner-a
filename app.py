"""
Interfaz web (Streamlit) para el Laboratorio de Minería de Datos.

Permite seleccionar uno de los tres ejercicios (Dólar, Glucosa, Energía),
ingresar por teclado los valores de las variables independientes y obtener
la predicción de la variable dependiente usando el modelo de regresión
lineal múltiple previamente entrenado y exportado con joblib.

Ejecutar:
    streamlit run app.py
"""

from pathlib import Path

import joblib
import streamlit as st
from streamlit_option_menu import option_menu

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

AUTOR = "Valery Nickol Rosero Molina"

st.set_page_config(
    page_title="Laboratorio de Minería de Datos",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Estilo — paleta navy / crema / dorado
# ---------------------------------------------------------------------------
NAVY = "#1B3A4C"
NAVY_DARK = "#102530"
CREAM = "#F4F1EA"
CARD = "#FFFFFF"
GOLD = "#C9A876"
GOLD_DARK = "#AD8A57"
TEAL = "#3C6E8F"
MUTED = "#7A8790"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {CREAM};
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    .block-container {{
        padding-top: 2rem;
        max-width: 760px;
    }}

    /* ---------- Encabezado ---------- */
    .lab-avatar {{
        width: 84px;
        height: 84px;
        border-radius: 50%;
        background: linear-gradient(160deg, {NAVY} 0%, {NAVY_DARK} 100%);
        border: 3px solid {GOLD};
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.1rem auto;
        box-shadow: 0 6px 18px rgba(27,58,76,0.25);
    }}
    .lab-avatar span {{
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        color: {GOLD};
        font-weight: 700;
    }}
    .lab-title {{
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 2rem;
        text-align: center;
        color: {NAVY};
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
    }}
    .lab-subtitle {{
        text-align: center;
        color: {TEAL};
        font-size: 0.78rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-style: italic;
        margin-bottom: 1.1rem;
    }}
    .lab-divider {{
        display: flex;
        align-items: center;
        text-align: center;
        color: {GOLD_DARK};
        margin: 0 auto 1.6rem auto;
        width: 70%;
    }}
    .lab-divider::before, .lab-divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {GOLD};
        opacity: 0.6;
    }}
    .lab-divider span {{
        padding: 0 10px;
        font-size: 0.55rem;
    }}

    /* ---------- Tarjetas ---------- */
    .lab-card {{
        background: {CARD};
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 4px 18px rgba(27,58,76,0.08);
        border: 1px solid rgba(201,168,118,0.25);
        margin-bottom: 1.3rem;
    }}
    .lab-card h4 {{
        font-family: 'Playfair Display', serif;
        color: {NAVY};
        margin-top: 0;
        margin-bottom: 0.3rem;
    }}
    .lab-card p {{
        color: {MUTED};
        font-size: 0.92rem;
        margin-bottom: 0;
    }}

    .stat-tile {{
        background: {CARD};
        border-radius: 12px;
        padding: 0.9rem 0.6rem;
        text-align: center;
        border: 1px solid rgba(201,168,118,0.3);
        box-shadow: 0 2px 10px rgba(27,58,76,0.06);
    }}
    .stat-tile .value {{
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: {NAVY};
        font-weight: 700;
    }}
    .stat-tile .label {{
        font-size: 0.68rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: {TEAL};
        margin-top: 2px;
    }}

    .result-card {{
        background: linear-gradient(135deg, {NAVY} 0%, {NAVY_DARK} 100%);
        border: 1px solid {GOLD};
        border-radius: 14px;
        padding: 1.6rem;
        text-align: center;
        margin: 1rem 0 1.4rem 0;
        box-shadow: 0 8px 24px rgba(27,58,76,0.25);
    }}
    .result-card .label {{
        color: {GOLD};
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.72rem;
        margin-bottom: 0.4rem;
    }}
    .result-card .value {{
        font-family: 'Playfair Display', serif;
        color: #FFFFFF;
        font-size: 2.2rem;
        font-weight: 700;
    }}

    /* ---------- Botones ---------- */
    .stButton>button, .stFormSubmitButton>button {{
        background: linear-gradient(135deg, {GOLD} 0%, {GOLD_DARK} 100%);
        color: {NAVY_DARK};
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.55rem 1.2rem;
        letter-spacing: 0.5px;
        transition: all 0.2s ease-in-out;
    }}
    .stButton>button:hover, .stFormSubmitButton>button:hover {{
        box-shadow: 0 4px 14px rgba(173,138,87,0.45);
        transform: translateY(-1px);
        color: {NAVY_DARK};
    }}

    .lab-footer {{
        text-align: center;
        color: {MUTED};
        font-size: 0.72rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(201,168,118,0.35);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def cargar_modelo(nombre_archivo):
    payload = joblib.load(MODELS_DIR / nombre_archivo)
    return payload["modelo"], payload["features"], payload["target"], payload.get("metrics")


EJERCICIOS = {
    "Dólar": {
        "archivo": "modelo_dolar.pkl",
        "icono": "cash-coin",
        "descripcion": "Predicción del precio del dólar a partir del día, la inflación y la tasa de interés.",
        "inputs": {
            "Dia": {"label": "Día (número de día)", "min": 1, "max": 3650, "value": 225, "step": 1},
            "Inflacion": {"label": "Inflación (%)", "min": 0.0, "max": 20.0, "value": 6.0, "step": 0.1},
            "Tasa_interes": {"label": "Tasa de interés (%)", "min": 0.0, "max": 25.0, "value": 7.0, "step": 0.1},
        },
        "unidad": "COP",
    },
    "Glucosa": {
        "archivo": "modelo_glucosa.pkl",
        "icono": "droplet",
        "descripcion": "Predicción del nivel de glucosa en sangre a partir de edad, IMC y actividad física.",
        "inputs": {
            "Edad": {"label": "Edad (años)", "min": 0, "max": 120, "value": 45, "step": 1},
            "IMC": {"label": "Índice de Masa Corporal (IMC)", "min": 10.0, "max": 60.0, "value": 25.0, "step": 0.1},
            "Actividad_Fisica": {"label": "Actividad física (horas/semana)", "min": 0.0, "max": 30.0, "value": 3.0, "step": 0.5},
        },
        "unidad": "mg/dL",
    },
    "Energía": {
        "archivo": "modelo_energia.pkl",
        "icono": "lightning-charge",
        "descripcion": "Predicción del consumo de energía eléctrica a partir de temperatura, hora del día y día de la semana.",
        "inputs": {
            "Temperatura": {"label": "Temperatura (°C)", "min": -20.0, "max": 55.0, "value": 20.0, "step": 0.5},
            "Hora": {"label": "Hora del día (1 a 24)", "min": 1, "max": 24, "value": 12, "step": 1},
            "Dia_Semana": {"label": "Día de la semana (1=Lunes ... 7=Domingo)", "min": 1, "max": 7, "value": 1, "step": 1},
        },
        "unidad": "kWh",
    },
}

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown('<div class="lab-avatar"><span>M</span></div>', unsafe_allow_html=True)
st.markdown('<div class="lab-title">Laboratorio de Minería de Datos</div>', unsafe_allow_html=True)
st.markdown('<div class="lab-subtitle">Regresión Lineal Múltiple · CRISP-DM</div>', unsafe_allow_html=True)
st.markdown('<div class="lab-divider"><span>◆</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Selector de ejercicio
# ---------------------------------------------------------------------------
ejercicio = option_menu(
    menu_title=None,
    options=list(EJERCICIOS.keys()),
    icons=[cfg["icono"] for cfg in EJERCICIOS.values()],
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": "transparent", "margin-bottom": "1.2rem"},
        "icon": {"color": GOLD_DARK, "font-size": "16px"},
        "nav-link": {
            "font-family": "Inter, sans-serif",
            "font-weight": "600",
            "color": NAVY,
            "background-color": CARD,
            "border-radius": "10px",
            "margin": "0 4px",
            "border": f"1px solid rgba(201,168,118,0.35)",
        },
        "nav-link-selected": {"background-color": NAVY, "color": "#FFFFFF"},
    },
)

config = EJERCICIOS[ejercicio]

modelo_path = MODELS_DIR / config["archivo"]
if not modelo_path.exists():
    st.error(
        f"No se encontró el modelo '{config['archivo']}'. "
        f"Ejecuta primero los scripts en la carpeta 'src/' para entrenar y exportar los modelos."
    )
    st.stop()

modelo, features, target, metrics = cargar_modelo(config["archivo"])

st.markdown(
    f'<div class="lab-card"><h4>{ejercicio}</h4><p>{config["descripcion"]}</p></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Indicadores de desempeño del modelo
# ---------------------------------------------------------------------------
if metrics:
    c1, c2, c3 = st.columns(3)
    tiles = [
        (c1, f"{metrics['test']['R2'] * 100:.1f}%", "R² Prueba"),
        (c2, f"{metrics['test']['RMSE']:.2f}", "RMSE Prueba"),
        (c3, f"{metrics.get('cv_r2_mean', 0) * 100:.1f}%", "R² Val. Cruzada"),
    ]
    for col, valor, etiqueta in tiles:
        col.markdown(
            f'<div class="stat-tile"><div class="value">{valor}</div><div class="label">{etiqueta}</div></div>',
            unsafe_allow_html=True,
        )
    st.write("")

# ---------------------------------------------------------------------------
# Formulario de predicción
# ---------------------------------------------------------------------------
st.markdown('<div class="lab-card">', unsafe_allow_html=True)
st.markdown("##### Ingresa los valores")
valores = {}
with st.form(key=f"form_{ejercicio}"):
    for feat in features:
        cfg = config["inputs"][feat]
        valores[feat] = st.number_input(
            cfg["label"], min_value=cfg["min"], max_value=cfg["max"], value=cfg["value"], step=cfg["step"]
        )
    enviar = st.form_submit_button("Predecir →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if enviar:
    entrada = [[valores[feat] for feat in features]]
    prediccion = modelo.predict(entrada)[0]
    st.markdown(
        f"""
        <div class="result-card">
            <div class="label">Predicción de {target}</div>
            <div class="value">{prediccion:,.2f} {config['unidad']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Ver coeficientes del modelo"):
        for feat, coef in zip(features, modelo.coef_):
            st.write(f"- **{feat}**: {coef:.4f}")
        st.write(f"- **Intercepto**: {modelo.intercept_:.4f}")

st.markdown(
    f'<div class="lab-footer">© 2026 {AUTOR} — Laboratorio de Minería de Datos</div>',
    unsafe_allow_html=True,
)
