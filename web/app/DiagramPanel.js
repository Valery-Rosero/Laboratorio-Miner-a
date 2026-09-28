"use client";

export default function DiagramPanel({ ejercicio }) {
  return (
    <div className="lab-card">
      <h4>Diagramas del análisis exploratorio</h4>
      <p style={{ marginBottom: "1rem" }}>
        Relación de cada variable independiente con {ejercicio.nombre.toLowerCase()} y matriz de
        correlación, calculadas sobre el conjunto de datos real de entrenamiento.
      </p>
      <img
        src={ejercicio.imgRelaciones}
        alt={`Relación de las variables independientes con ${ejercicio.nombre}`}
        style={{ width: "100%", borderRadius: 10, border: "1px solid rgba(27,58,76,0.1)" }}
      />
      <p className="diagram-caption">
        Dispersión de cada variable frente a la variable objetivo, con línea de tendencia.
      </p>
      <img
        src={ejercicio.imgCorrelacion}
        alt={`Matriz de correlación — ${ejercicio.nombre}`}
        style={{
          width: "100%",
          maxWidth: 380,
          margin: "0.6rem auto 0 auto",
          display: "block",
          borderRadius: 10,
          border: "1px solid rgba(27,58,76,0.1)",
        }}
      />
      <p className="diagram-caption">Matriz de correlación entre todas las variables numéricas.</p>
    </div>
  );
}
