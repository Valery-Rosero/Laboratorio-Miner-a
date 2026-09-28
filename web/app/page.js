"use client";

import { useState } from "react";
import { EJERCICIOS } from "./ejercicios";
import DiagramPanel from "./DiagramPanel";
import EntrenamientoEnVivo from "./EntrenamientoEnVivo";

export default function Home() {
  const [ejercicioKey, setEjercicioKey] = useState("Dolar");
  const ejercicio = EJERCICIOS[ejercicioKey];

  const [valores, setValores] = useState(
    Object.fromEntries(ejercicio.inputs.map((f) => [f.key, f.value]))
  );
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  function cambiarEjercicio(key) {
    setEjercicioKey(key);
    setValores(Object.fromEntries(EJERCICIOS[key].inputs.map((f) => [f.key, f.value])));
    setResultado(null);
    setError(null);
  }

  function actualizarValor(key, value) {
    setValores((prev) => ({ ...prev, [key]: value }));
  }

  async function predecir(e) {
    e.preventDefault();
    setCargando(true);
    setError(null);
    setResultado(null);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ejercicio: ejercicioKey, valores }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "No se pudo obtener la predicción.");
      }
      setResultado(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <main>
      <header className="lab-header">
        <h1 className="lab-title">Laboratorio de Minería de Datos</h1>
        <p className="lab-subtitle">Regresión Lineal Múltiple · CRISP-DM</p>
      </header>

      <nav className="nav-menu">
        {Object.entries(EJERCICIOS).map(([key, ej]) => (
          <button
            key={key}
            className={`nav-link ${key === ejercicioKey ? "active" : ""}`}
            onClick={() => cambiarEjercicio(key)}
            type="button"
          >
            {ej.nombre}
          </button>
        ))}
      </nav>

      <div className="lab-card">
        <h4>{ejercicio.nombre}</h4>
        <p>{ejercicio.descripcion}</p>
      </div>

      <div className="stat-row">
        <div className="stat-tile">
          <div className="value">{(ejercicio.metrics.r2Test * 100).toFixed(1)}%</div>
          <div className="label">R² Prueba</div>
        </div>
        <div className="stat-tile">
          <div className="value">{ejercicio.metrics.rmseTest.toFixed(2)}</div>
          <div className="label">RMSE Prueba</div>
        </div>
        <div className="stat-tile">
          <div className="value">{(ejercicio.metrics.r2CV * 100).toFixed(1)}%</div>
          <div className="label">R² Val. Cruzada</div>
        </div>
      </div>

      <section className="section-analisis">
        <DiagramPanel ejercicio={ejercicio} />
        <EntrenamientoEnVivo ejercicioKey={ejercicioKey} />
      </section>

      <section className="section-prediccion">
        <form className="lab-card" onSubmit={predecir}>
          <h4 style={{ marginBottom: "0.8rem" }}>Ingresa los valores</h4>
          <div className="form-grid">
            {ejercicio.inputs.map((f) => (
              <div className="form-field" key={f.key}>
                <label htmlFor={f.key}>{f.label}</label>
                <input
                  id={f.key}
                  type="number"
                  min={f.min}
                  max={f.max}
                  step={f.step}
                  value={valores[f.key]}
                  onChange={(e) => actualizarValor(f.key, e.target.value)}
                  required
                />
              </div>
            ))}
          </div>
          <button className="btn-predict" type="submit" disabled={cargando}>
            {cargando ? "Calculando..." : "Predecir →"}
          </button>
        </form>

        {error && <p className="error-text">{error}</p>}

        {resultado && (
          <div className="result-card">
            <div className="label">Predicción de {resultado.target}</div>
            <div className="value">
              {resultado.prediccion.toLocaleString("es-CO", { maximumFractionDigits: 2 })}{" "}
              {resultado.unidad}
            </div>
          </div>
        )}

        {resultado && (
          <details className="coef-box lab-card">
            <summary>Ver coeficientes del modelo</summary>
            <ul>
              {Object.entries(resultado.coeficientes).map(([k, v]) => (
                <li key={k}>
                  {k}: {v.toFixed(4)}
                </li>
              ))}
              <li>Intercepto: {resultado.intercepto.toFixed(4)}</li>
            </ul>
          </details>
        )}
      </section>

      <div className="lab-footer">Valery Rosero</div>
    </main>
  );
}
