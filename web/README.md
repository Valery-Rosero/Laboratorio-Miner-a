# Laboratorio de Minería de Datos — Versión web (Next.js + Flask API)

Versión desplegable en **Vercel** de la interfaz de predicción. El resto del
laboratorio (generación de datos, entrenamiento, notebooks, informe PDF y la
app Streamlit original) vive en la raíz del repositorio, en `..`.

## Arquitectura

- **Frontend**: Next.js (App Router) + React — réplica de la interfaz navy/crema/dorado.
- **Backend**: función serverless de Python con **Flask**, en `api/predict.py`, que carga
  los modelos `.pkl` (`api/models/`) y expone `POST /api/predict`.

Este patrón (Next.js + funciones Python serverless) sí es compatible con Vercel,
a diferencia de Streamlit, que requiere un servidor persistente con WebSocket y
por eso no puede desplegarse en Vercel.

## Desarrollo local

```bash
cd web
npm install
npm run dev        # http://localhost:3000 (solo frontend)

# En otra terminal, para probar la API:
cd web/api
pip install -r ../requirements.txt
flask --app predict run --port 5328
```

## Despliegue en Vercel

**Opción recomendada — desde el dashboard (sin necesidad de login en la terminal):**

1. Entra a [vercel.com](https://vercel.com) e inicia sesión con tu cuenta de GitHub.
2. "Add New… → Project" → importa el repositorio `Valery-Rosero/Laboratorio-Miner-a`.
3. En "Root Directory" selecciona **`web`** (importante: no la raíz del repo).
4. Framework Preset: Vercel detectará **Next.js** automáticamente.
5. Deploy. Vercel instalará `requirements.txt` y construirá `api/predict.py`
   como función serverless de Python automáticamente (no requiere configuración adicional).

**Alternativa — desde la terminal (requiere `vercel login` interactivo):**

```bash
cd web
npx vercel login
npx vercel --prod
```
