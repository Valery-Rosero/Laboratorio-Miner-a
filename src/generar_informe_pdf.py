"""
Genera el informe académico formal (INFORME.pdf) en formato APA (7.ª edición),
fuente Times New Roman, con portada institucional, cuerpo del documento,
tablas de resultados, figuras y referencias.

Ejecutar:
    python src/generar_informe_pdf.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = Path(__file__).resolve().parent.parent
PLOTS_DIR = BASE_DIR / "graficas"
OUTPUT_PATH = BASE_DIR / "INFORME.pdf"

# ---------------------------------------------------------------------------
# Datos institucionales
# ---------------------------------------------------------------------------
TITULO = (
    "APLICACIÓN DE REGRESIÓN LINEAL MÚLTIPLE BAJO LA METODOLOGÍA CRISP-DM PARA LA "
    "PREDICCIÓN DEL PRECIO DEL DÓLAR, EL NIVEL DE GLUCOSA EN SANGRE Y EL CONSUMO DE "
    "ENERGÍA ELÉCTRICA"
)
ESTUDIANTE = "Valery Nickol Rosero Molina"
UNIVERSIDAD = "Universidad Cooperativa de Colombia"
FACULTAD = "Facultad de Ingeniería, Programa de Ingeniería de Software"
ASIGNATURA = "Inteligencia de Negocios y Minería de Datos"
DOCENTE = "Dr. Cristian Camilo Ordoñez Quintero"
CIUDAD = "San Juan de Pasto, Colombia"
FECHA = "28 de septiembre de 2026"

# ---------------------------------------------------------------------------
# Fuentes — Times New Roman embebida
# ---------------------------------------------------------------------------
FONTS_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("TimesNewRoman", FONTS_DIR / "times.ttf"))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", FONTS_DIR / "timesbd.ttf"))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Italic", FONTS_DIR / "timesi.ttf"))
pdfmetrics.registerFont(TTFont("TimesNewRoman-BoldItalic", FONTS_DIR / "timesbi.ttf"))
pdfmetrics.registerFontFamily(
    "TimesNewRoman",
    normal="TimesNewRoman",
    bold="TimesNewRoman-Bold",
    italic="TimesNewRoman-Italic",
    boldItalic="TimesNewRoman-BoldItalic",
)

NAVY = colors.HexColor("#1B3A4C")

# ---------------------------------------------------------------------------
# Estilos (APA: Times New Roman 12pt, interlineado doble, sangría 0.5")
# ---------------------------------------------------------------------------
styles = {
    "cover_title": ParagraphStyle(
        "cover_title", fontName="TimesNewRoman-Bold", fontSize=12, leading=24,
        alignment=TA_CENTER, spaceAfter=0,
    ),
    "cover_text": ParagraphStyle(
        "cover_text", fontName="TimesNewRoman", fontSize=12, leading=24,
        alignment=TA_CENTER, spaceAfter=0,
    ),
    "cover_small": ParagraphStyle(
        "cover_small", fontName="TimesNewRoman", fontSize=11, leading=15,
        alignment=TA_CENTER, spaceAfter=0,
    ),
    "h1": ParagraphStyle(
        "h1", fontName="TimesNewRoman-Bold", fontSize=13, leading=24,
        alignment=TA_CENTER, spaceBefore=18, spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="TimesNewRoman-Bold", fontSize=12, leading=24,
        alignment=TA_JUSTIFY, spaceBefore=14, spaceAfter=6,
    ),
    "body": ParagraphStyle(
        "body", fontName="TimesNewRoman", fontSize=12, leading=24,
        alignment=TA_JUSTIFY, firstLineIndent=36, spaceAfter=6,
    ),
    "body_noindent": ParagraphStyle(
        "body_noindent", fontName="TimesNewRoman", fontSize=12, leading=24,
        alignment=TA_JUSTIFY, spaceAfter=6,
    ),
    "italic_center": ParagraphStyle(
        "italic_center", fontName="TimesNewRoman-Italic", fontSize=12, leading=16,
        alignment=TA_CENTER, spaceBefore=10, spaceAfter=2,
    ),
    "caption": ParagraphStyle(
        "caption", fontName="TimesNewRoman", fontSize=10, leading=13,
        alignment=TA_CENTER, spaceAfter=14,
    ),
    "reference": ParagraphStyle(
        "reference", fontName="TimesNewRoman", fontSize=12, leading=24,
        alignment=TA_JUSTIFY, leftIndent=36, firstLineIndent=-36, spaceAfter=6,
    ),
    "table_cell": ParagraphStyle(
        "table_cell", fontName="TimesNewRoman", fontSize=10.5, leading=13,
        alignment=TA_CENTER,
    ),
    "table_header": ParagraphStyle(
        "table_header", fontName="TimesNewRoman-Bold", fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=colors.white,
    ),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def tabla_metricas(filas, encabezados):
    data = [[Paragraph(h, styles["table_header"]) for h in encabezados]]
    for fila in filas:
        data.append([Paragraph(str(c), styles["table_cell"]) for c in fila])
    tabla = Table(data, hAlign="CENTER", colWidths=None)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B9B9B9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F1EA")]),
    ]))
    return tabla


def figura(nombre_archivo, ancho_in, alto_in, numero, titulo):
    ruta = PLOTS_DIR / nombre_archivo
    img = Image(str(ruta), width=ancho_in * inch, height=alto_in * inch)
    img.hAlign = "CENTER"
    return KeepTogether([
        p(f"<i>Figura {numero}</i>", "italic_center"),
        p(f"<i>{titulo}</i>", "caption"),
        img,
        Spacer(1, 14),
    ])


# ---------------------------------------------------------------------------
# Numeración de páginas (esquina superior derecha, formato APA)
# ---------------------------------------------------------------------------
class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont("TimesNewRoman", 11)
            self.drawRightString(letter[0] - inch, letter[1] - 0.6 * inch, str(self._pageNumber))
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)


# ---------------------------------------------------------------------------
# Construcción del documento
# ---------------------------------------------------------------------------
def construir_story():
    story = []

    # ----- PORTADA -----
    story.append(Spacer(1, 1.6 * inch))
    story.append(p(TITULO, "cover_title"))
    story.append(Spacer(1, 0.5 * inch))
    story.append(p(ESTUDIANTE, "cover_text"))
    story.append(p(FACULTAD, "cover_text"))
    story.append(p(UNIVERSIDAD, "cover_text"))
    story.append(Spacer(1, 0.2 * inch))
    story.append(p(ASIGNATURA, "cover_text"))
    story.append(p(f"Docente: {DOCENTE}", "cover_text"))
    story.append(Spacer(1, 0.3 * inch))
    story.append(p(CIUDAD, "cover_text"))
    story.append(p(FECHA, "cover_text"))
    story.append(PageBreak())

    # ----- RESUMEN -----
    story.append(p("Resumen", "h1"))
    story.append(p(
        "El presente informe documenta la aplicación de la metodología CRISP-DM "
        "(Cross Industry Standard Process for Data Mining) para el desarrollo de tres "
        "modelos de regresión lineal múltiple orientados a la predicción del precio del "
        "dólar, el nivel de glucosa en sangre y el consumo de energía eléctrica. "
        "Se describen las fases de comprensión de los datos, preparación, modelado y "
        "evaluación, esta última basada en el error cuadrático medio (MSE), la raíz del "
        "error cuadrático medio (RMSE) y el coeficiente de determinación (R²), calculados "
        "tanto en el conjunto de entrenamiento como en el de prueba, además de validación "
        "cruzada de cinco particiones (5-fold), con el fin de descartar sobreajuste. "
        "Los tres modelos alcanzaron un R² superior al 90&#37; en el conjunto de prueba, "
        "con diferencias inferiores al 2&#37; frente al conjunto de entrenamiento. "
        "Finalmente, se exportaron los modelos mediante la librería joblib y se integraron "
        "en una interfaz web desarrollada con Streamlit para su uso interactivo.",
        "body_noindent",
    ))
    story.append(p(
        "<i>Palabras clave:</i> minería de datos, regresión lineal múltiple, CRISP-DM, "
        "aprendizaje automático, evaluación de modelos.",
        "body_noindent",
    ))
    story.append(PageBreak())

    # ----- 1. INTRODUCCIÓN -----
    story.append(p("1. Introducción", "h1"))
    story.append(p(
        "La minería de datos comprende un conjunto de técnicas orientadas a descubrir "
        "patrones, relaciones y modelos predictivos a partir de conjuntos de datos "
        "estructurados. Entre las técnicas de modelado predictivo más utilizadas se "
        "encuentra la regresión lineal múltiple, la cual permite estimar el valor de una "
        "variable cuantitativa dependiente a partir de dos o más variables independientes, "
        "asumiendo una relación lineal entre ellas (Montgomery et al., 2021). "
        "El objetivo del presente laboratorio es aplicar las fases de la metodología "
        "CRISP-DM (Chapman et al., 2000) para construir, evaluar, exportar y desplegar "
        "tres modelos de regresión lineal múltiple en distintos contextos: económico "
        "(precio del dólar), clínico (nivel de glucosa en sangre) e industrial/energético "
        "(consumo de energía eléctrica).",
        "body",
    ))

    # ----- 2. METODOLOGÍA -----
    story.append(p("2. Metodología", "h1"))
    story.append(p(
        "El desarrollo del laboratorio se estructuró siguiendo las fases del modelo "
        "CRISP-DM (Chapman et al., 2000), tal como se resume en la Tabla 1.",
        "body",
    ))
    story.append(KeepTogether([
        tabla_metricas(
            [
                ["Comprensión del negocio", "Predecir el comportamiento de tres variables de interés (precio del dólar, glucosa y consumo eléctrico) a partir de variables explicativas disponibles."],
                ["Comprensión de los datos", "Exploración de los conjuntos de datos mediante estadística descriptiva y matrices de correlación."],
                ["Preparación de los datos", "Selección de variables independientes y dependiente; partición en entrenamiento (80&#37;) y prueba (20&#37;)."],
                ["Modelado", "Ajuste de un modelo de regresión lineal múltiple (scikit-learn) por cada ejercicio (Pedregosa et al., 2011)."],
                ["Evaluación", "Cálculo de MSE, RMSE y R² en entrenamiento y prueba, y validación cruzada de 5 particiones para descartar sobreajuste."],
                ["Despliegue", "Exportación de los modelos con joblib e integración en una interfaz web desarrollada con Streamlit."],
            ],
            ["Fase CRISP-DM", "Aplicación en el laboratorio"],
        ),
        p("<i>Tabla 1</i>", "italic_center"),
        p("<i>Fases de la metodología CRISP-DM aplicadas en el laboratorio</i>", "caption"),
    ]))

    story.append(p(
        "Para determinar si un modelo presenta sobreajuste se comparó el coeficiente de "
        "determinación (R²) obtenido en el conjunto de entrenamiento frente al obtenido en "
        "el conjunto de prueba, y frente al promedio de una validación cruzada de cinco "
        "particiones con barajado aleatorio de los datos. Se consideró que un modelo no "
        "presenta sobreajuste significativo cuando la diferencia entre el R² de "
        "entrenamiento y el de prueba es inferior a 0.05, y el R² de validación cruzada es "
        "consistente con ambos valores.",
        "body",
    ))

    # ----- 3-5. EJERCICIOS -----
    ejercicios = [
        {
            "n": "3", "nombre": "Predicción del precio del dólar",
            "vars": "Día, Inflación y Tasa de interés",
            "target": "Precio_Dolar",
            "ecuacion": "Precio_Dolar = 3989.85 + 1.18 · Día + 139.87 · Inflación − 72.74 · Tasa_interes",
            "interpretacion": (
                "El coeficiente de la variable Día (+1.18) indica una tendencia de largo plazo al alza del "
                "precio del dólar. La variable Inflación (+139.87) presenta el mayor efecto marginal: por "
                "cada punto porcentual adicional de inflación, el precio del dólar aumenta en promedio "
                "139.87 unidades, manteniendo las demás variables constantes. Por su parte, la Tasa de "
                "interés (−72.74) tiene un efecto inverso, consistente con la teoría económica según la "
                "cual tasas de interés más altas atraen capital extranjero y fortalecen la moneda local."
            ),
            "tabla": [
                ["Entrenamiento", "6148.51", "78.41", "0.9304"],
                ["Prueba", "6604.58", "81.27", "0.9132"],
                ["Validación cruzada (5-fold)", "—", "—", "0.9249 ± 0.0132"],
            ],
            "img_rel": "ejercicio1_dolar_relaciones.png", "img_corr": "ejercicio1_dolar_correlacion.png",
            "fig_n1": "1", "fig_n2": "2",
            "gap": "0.0172",
        },
        {
            "n": "4", "nombre": "Predicción de niveles de glucosa en sangre",
            "vars": "Edad, IMC y Actividad física",
            "target": "Nivel_Glucosa",
            "ecuacion": "Nivel_Glucosa = 55.86 + 0.52 · Edad + 1.92 · IMC − 3.23 · Actividad_Fisica",
            "interpretacion": (
                "Por cada año adicional de edad, el nivel de glucosa aumenta en promedio 0.52 mg/dL. "
                "Por cada punto adicional de índice de masa corporal (IMC), la glucosa aumenta en promedio "
                "1.92 mg/dL. La actividad física presenta un efecto protector: por cada hora semanal "
                "adicional de ejercicio, el nivel de glucosa disminuye en promedio 3.23 mg/dL. "
                "Al calcular la importancia relativa de cada variable (valor absoluto del coeficiente "
                "multiplicado por la desviación estándar de la variable, para hacerlas comparables en una "
                "misma escala), se obtuvo: IMC = 12.54, Actividad física = 11.69 y Edad = 8.53. "
                "Por lo tanto, el IMC es la variable con mayor impacto global sobre el nivel de glucosa, "
                "seguida muy de cerca por la actividad física."
            ),
            "tabla": [
                ["Entrenamiento", "27.74", "5.27", "0.9296"],
                ["Prueba", "31.53", "5.62", "0.9352"],
                ["Validación cruzada (5-fold)", "—", "—", "0.9270 ± 0.0095"],
            ],
            "img_rel": "ejercicio2_glucosa_relaciones.png", "img_corr": "ejercicio2_glucosa_correlacion.png",
            "fig_n1": "3", "fig_n2": "4",
            "gap": "−0.0056",
        },
        {
            "n": "5", "nombre": "Predicción del consumo de energía eléctrica",
            "vars": "Temperatura, Hora del día y Día de la semana",
            "target": "Consumo_Energia",
            "ecuacion": "Consumo_Energia = 14.73 + 1.32 · Temperatura + 0.89 · Hora − 1.61 · Dia_Semana",
            "interpretacion": (
                "La importancia relativa de cada variable (valor absoluto del coeficiente multiplicado por "
                "su desviación estándar) fue: Temperatura = 16.98, Hora = 6.45 y Día de la semana = 3.33. "
                "La temperatura es, por un margen amplio, la variable con mayor impacto en el consumo "
                "eléctrico, lo cual es consistente con el uso de sistemas de climatización (calefacción o "
                "aire acondicionado) ante temperaturas extremas. La hora del día ocupa el segundo lugar en "
                "importancia, y el día de la semana presenta una influencia menor, aunque consistente con "
                "un menor consumo hacia el fin de semana."
            ),
            "tabla": [
                ["Entrenamiento", "20.44", "4.52", "0.9424"],
                ["Prueba", "24.25", "4.93", "0.9340"],
                ["Validación cruzada (5-fold)", "—", "—", "0.9372 ± 0.0105"],
            ],
            "img_rel": "ejercicio3_energia_relaciones.png", "img_corr": "ejercicio3_energia_correlacion.png",
            "fig_n1": "5", "fig_n2": "6",
            "gap": "0.0084",
        },
    ]

    for ej in ejercicios:
        story.append(p(f"{ej['n']}. {ej['nombre']}", "h1"))
        story.append(p(
            f"Se ajustó un modelo de regresión lineal múltiple utilizando las variables independientes "
            f"{ej['vars']} para predecir la variable {ej['target']}. La ecuación del modelo resultante es "
            f"la siguiente:",
            "body",
        ))
        story.append(p(f"<i>{ej['ecuacion']}</i>", "italic_center"))
        story.append(Spacer(1, 8))
        story.append(p(f"{ej['n']}.1 Interpretación de coeficientes", "h2"))
        story.append(p(ej["interpretacion"], "body"))
        story.append(p(f"{ej['n']}.2 Desempeño del modelo", "h2"))
        story.append(KeepTogether([
            tabla_metricas(ej["tabla"], ["Conjunto", "MSE", "RMSE", "R²"]),
            p(f"<i>Tabla {2 + int(ej['n'])}</i>", "italic_center"),
            p(f"<i>Métricas de desempeño del modelo de {ej['target']}</i>", "caption"),
        ]))
        story.append(p(
            f"La diferencia entre el R² de entrenamiento y de prueba fue de {ej['gap']}, valor inferior "
            f"al umbral de 0.05 establecido como criterio de sobreajuste, y el R² obtenido en la validación "
            f"cruzada resultó consistente con ambos conjuntos. En consecuencia, el modelo generaliza "
            f"adecuadamente y no presenta evidencia de sobreajuste, superando el umbral de R² &gt; 0.90 "
            f"exigido para el conjunto de prueba.",
            "body",
        ))
        story.append(p(f"{ej['n']}.3 Visualización de relaciones entre variables", "h2"))
        story.append(figura(ej["img_rel"], 6.3, 6.3 * 4 / 15, ej["fig_n1"],
                             f"Relación de cada variable independiente con {ej['target']}"))
        story.append(figura(ej["img_corr"], 3.6, 3.6 * 4 / 5, ej["fig_n2"],
                             f"Matriz de correlación — {ej['nombre']}"))

    # ----- 6. RESUMEN COMPARATIVO -----
    story.append(p("6. Resumen comparativo de los tres modelos", "h1"))
    story.append(p(
        "La Tabla 5 presenta un resumen comparativo del desempeño de los tres modelos "
        "desarrollados. En todos los casos el R² del conjunto de prueba superó el 90&#37;, "
        "con una diferencia mínima frente al R² de entrenamiento y resultados consistentes "
        "en validación cruzada, lo que confirma que los modelos generalizan correctamente y "
        "no se encuentran sobreajustados.",
        "body",
    ))
    story.append(KeepTogether([
        tabla_metricas(
            [
                ["Dólar", "0.9304", "0.9132", "0.9249 ± 0.0132", "0.0172", "No"],
                ["Glucosa", "0.9296", "0.9352", "0.9270 ± 0.0095", "−0.0056", "No"],
                ["Energía", "0.9424", "0.9340", "0.9372 ± 0.0105", "0.0084", "No"],
            ],
            ["Ejercicio", "R² Train", "R² Test", "R² CV (5-fold)", "Diferencia Train-Test", "¿Sobreajuste?"],
        ),
        p("<i>Tabla 5</i>", "italic_center"),
        p("<i>Comparación del desempeño de los tres modelos de regresión lineal múltiple</i>", "caption"),
    ]))

    # ----- 7. EXPORTACIÓN -----
    story.append(p("7. Exportación de los modelos", "h1"))
    story.append(p(
        "Se investigaron las librerías <i>pickle</i> y <i>joblib</i> de Python para la "
        "serialización de modelos entrenados. Se optó por <i>joblib</i>, dado que "
        "scikit-learn la recomienda de forma oficial para objetos que contienen grandes "
        "arreglos de NumPy —como es el caso de los modelos de regresión lineal—, al ofrecer "
        "una compresión y velocidad de lectura/escritura más eficiente que <i>pickle</i> en "
        "estos escenarios (Pedregosa et al., 2011). Cada modelo se exportó junto con sus "
        "metadatos (variables independientes, variable dependiente y métricas de "
        "desempeño) en un único archivo: <i>modelo_dolar.pkl</i>, <i>modelo_glucosa.pkl</i> "
        "y <i>modelo_energia.pkl</i>, ubicados en la carpeta <i>models/</i> del proyecto.",
        "body",
    ))

    # ----- 8. INTERFAZ WEB -----
    story.append(p("8. Desarrollo de la interfaz web", "h1"))
    story.append(p(
        "Se desarrolló una interfaz web interactiva utilizando el framework Streamlit, la "
        "cual permite al usuario seleccionar uno de los tres ejercicios (Dólar, Glucosa o "
        "Energía), ingresar por teclado los valores de las variables independientes "
        "correspondientes y obtener de forma inmediata la predicción de la variable "
        "dependiente, junto con los indicadores de desempeño del modelo (R² y RMSE) y la "
        "posibilidad de consultar los coeficientes utilizados. La interfaz carga "
        "directamente los modelos previamente exportados, sin necesidad de reentrenamiento, "
        "lo que permite su despliegue como una aplicación productiva independiente del "
        "proceso de modelado.",
        "body",
    ))

    # ----- 9. CONCLUSIONES -----
    story.append(p("9. Conclusiones", "h1"))
    conclusiones = [
        "La metodología CRISP-DM permitió estructurar el desarrollo del laboratorio de "
        "forma ordenada, desde la comprensión del problema hasta el despliegue de un "
        "producto utilizable por un usuario final no técnico.",
        "Los tres modelos de regresión lineal múltiple lograron un ajuste satisfactorio "
        "(R² superior al 90&#37; en el conjunto de prueba), sin evidencia de sobreajuste, "
        "gracias a la validación mediante conjuntos de prueba independientes y validación "
        "cruzada de cinco particiones.",
        "En el caso del precio del dólar, la inflación resultó ser la variable con mayor "
        "efecto marginal, mientras que la tasa de interés actúa en sentido contrario, "
        "resultado coherente con la teoría económica.",
        "En el caso del nivel de glucosa, el índice de masa corporal (IMC) fue la variable "
        "con mayor impacto global, seguida de cerca por la actividad física, la cual actúa "
        "como factor protector.",
        "En el caso del consumo de energía eléctrica, la temperatura fue la variable "
        "dominante, resultado consistente con el uso de sistemas de climatización.",
        "La exportación de los modelos mediante joblib y su integración en una interfaz "
        "web desarrollada con Streamlit permitió completar el flujo integral de un "
        "proyecto de minería de datos: desde el dato crudo hasta un modelo productivo, "
        "accesible e interpretable.",
    ]
    for c in conclusiones:
        story.append(p(f"• {c}", "body_noindent"))

    # ----- REFERENCIAS -----
    story.append(PageBreak())
    story.append(p("Referencias", "h1"))
    referencias = [
        "American Psychological Association. (2020). <i>Publication manual of the "
        "American Psychological Association</i> (7.ª ed.). https://doi.org/10.1037/0000165-000",
        "Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., "
        "&amp; Wirth, R. (2000). <i>CRISP-DM 1.0: Step-by-step data mining guide</i>. "
        "SPSS Inc.",
        "Montgomery, D. C., Peck, E. A., &amp; Vining, G. G. (2021). <i>Introduction to "
        "linear regression analysis</i> (6.ª ed.). Wiley.",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., "
        "Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., "
        "Cournapeau, D., Brucher, M., Perrot, M., &amp; Duchesnay, E. (2011). Scikit-learn: "
        "Machine learning in Python. <i>Journal of Machine Learning Research, 12</i>, "
        "2825–2830.",
    ]
    for ref in referencias:
        story.append(p(ref, "reference"))

    return story


def main():
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        title="Informe - Laboratorio de Minería de Datos",
        author=ESTUDIANTE,
    )
    story = construir_story()
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Informe generado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
