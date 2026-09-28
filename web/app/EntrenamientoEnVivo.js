"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { MUESTRAS } from "./muestras";

// Colores de marca reservados para las marcas de datos (distintos de los de la UI),
// validados con el validador de paletas (contraste, banda de luminosidad, separación CVD).
const COLOR_DATOS = "#2C6E9E";
const COLOR_MODELO = "#C17817";

const VB_W = 640;
const SCATTER_H = 300;
const LOSS_H = 170;
const MARGIN = { left: 54, right: 16, top: 14, bottom: 34 };
const LR = 0.15;
const MAX_EPOCHS = 80;
const TICK_MS = 90;

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}
function std(arr, m) {
  return Math.sqrt(arr.reduce((a, b) => a + (b - m) ** 2, 0) / arr.length) || 1;
}

export default function EntrenamientoEnVivo({ ejercicioKey }) {
  const muestra = MUESTRAS[ejercicioKey];
  const puntos = muestra.points; // [[x,y], ...]

  const stats = useMemo(() => {
    const xs = puntos.map((p) => p[0]);
    const ys = puntos.map((p) => p[1]);
    const meanX = mean(xs);
    const meanY = mean(ys);
    const stdX = std(xs, meanX);
    const stdY = std(ys, meanY);
    const zx = xs.map((x) => (x - meanX) / stdX);
    const zy = ys.map((y) => (y - meanY) / stdY);
    return {
      xs,
      ys,
      meanX,
      meanY,
      stdX,
      stdY,
      zx,
      zy,
      xMin: Math.min(...xs),
      xMax: Math.max(...xs),
      yMin: Math.min(...ys),
      yMax: Math.max(...ys),
    };
  }, [puntos]);

  const [epoch, setEpoch] = useState(0);
  const [w, setW] = useState({ w0: 0, w1: 0 });
  const [historial, setHistorial] = useState([]); // [{epoch, mse}]
  const [corriendo, setCorriendo] = useState(false);
  const [hoverPoint, setHoverPoint] = useState(null);
  const [hoverLoss, setHoverLoss] = useState(null);
  const intervalRef = useRef(null);
  const wRef = useRef({ w0: 0, w1: 0 });
  const epochRef = useRef(0);
  const scatterSvgRef = useRef(null);
  const lossSvgRef = useRef(null);

  function reiniciar() {
    clearInterval(intervalRef.current);
    wRef.current = { w0: 0, w1: 0 };
    epochRef.current = 0;
    setW({ w0: 0, w1: 0 });
    setEpoch(0);
    setHistorial([]);
    setCorriendo(false);
  }

  function paso() {
    const { zx, zy } = stats;
    const n = zx.length;
    let { w0, w1 } = wRef.current;
    let sumErr = 0;
    let sumErrX = 0;
    for (let i = 0; i < n; i++) {
      const pred = w0 + w1 * zx[i];
      const err = pred - zy[i];
      sumErr += err;
      sumErrX += err * zx[i];
    }
    w0 -= LR * (sumErr / n);
    w1 -= LR * (sumErrX / n);
    wRef.current = { w0, w1 };

    // MSE en unidades originales para que sea interpretable
    const slopeOrig = (w1 * stats.stdY) / stats.stdX;
    const interceptOrig = stats.meanY + w0 * stats.stdY - slopeOrig * stats.meanX;
    let sse = 0;
    for (let i = 0; i < n; i++) {
      const yhat = interceptOrig + slopeOrig * stats.xs[i];
      sse += (yhat - stats.ys[i]) ** 2;
    }
    const mse = sse / n;

    epochRef.current += 1;
    setW({ w0, w1 });
    setEpoch(epochRef.current);
    setHistorial((h) => [...h, { epoch: epochRef.current, mse }]);
  }

  function entrenar() {
    if (corriendo) return;
    setCorriendo(true);
    intervalRef.current = setInterval(() => {
      if (epochRef.current >= MAX_EPOCHS) {
        clearInterval(intervalRef.current);
        setCorriendo(false);
        return;
      }
      paso();
    }, TICK_MS);
  }

  useEffect(() => {
    reiniciar();
    const t = setTimeout(() => entrenar(), 500);
    return () => {
      clearTimeout(t);
      clearInterval(intervalRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ejercicioKey]);

  useEffect(() => {
    if (epoch >= MAX_EPOCHS) {
      clearInterval(intervalRef.current);
      setCorriendo(false);
    }
  }, [epoch]);

  // ---------- escalas del scatter ----------
  const padX = (stats.xMax - stats.xMin) * 0.08 || 1;
  const padY = (stats.yMax - stats.yMin) * 0.12 || 1;
  const domX = [stats.xMin - padX, stats.xMax + padX];
  const domY = [stats.yMin - padY, stats.yMax + padY];
  const plotW = VB_W - MARGIN.left - MARGIN.right;
  const plotH = SCATTER_H - MARGIN.top - MARGIN.bottom;

  const sx = (x) => MARGIN.left + ((x - domX[0]) / (domX[1] - domX[0])) * plotW;
  const sy = (y) => MARGIN.top + plotH - ((y - domY[0]) / (domY[1] - domY[0])) * plotH;

  const slopeOrig = (w.w1 * stats.stdY) / stats.stdX;
  const interceptOrig = stats.meanY + w.w0 * stats.stdY - slopeOrig * stats.meanX;
  const lineX1 = domX[0];
  const lineX2 = domX[1];
  const lineY1 = interceptOrig + slopeOrig * lineX1;
  const lineY2 = interceptOrig + slopeOrig * lineX2;

  const ticksX = [domX[0], (domX[0] + domX[1]) / 2, domX[1]];
  const ticksY = [domY[0], (domY[0] + domY[1]) / 2, domY[1]];

  // ---------- escalas de la curva de pérdida ----------
  const lossPlotW = VB_W - MARGIN.left - MARGIN.right;
  const lossPlotH = LOSS_H - MARGIN.top - MARGIN.bottom;
  const maxMse = historial.length ? Math.max(...historial.map((h) => h.mse)) : 1;
  const lx = (e) => MARGIN.left + (e / MAX_EPOCHS) * lossPlotW;
  const ly = (mse) => MARGIN.top + lossPlotH - (mse / (maxMse || 1)) * lossPlotH;
  const lossPath = historial.map((h, i) => `${i === 0 ? "M" : "L"} ${lx(h.epoch)} ${ly(h.mse)}`).join(" ");

  function handleLossMove(e) {
    const svg = lossSvgRef.current;
    if (!svg || historial.length === 0) return;
    const rect = svg.getBoundingClientRect();
    const frac = (e.clientX - rect.left) / rect.width;
    const xVb = frac * VB_W;
    let nearest = historial[0];
    let best = Infinity;
    for (const h of historial) {
      const d = Math.abs(lx(h.epoch) - xVb);
      if (d < best) {
        best = d;
        nearest = h;
      }
    }
    setHoverLoss(nearest);
  }

  const ultimoMse = historial.length ? historial[historial.length - 1].mse : null;

  return (
    <div className="lab-card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
        <h4 style={{ margin: 0 }}>Entrenamiento en vivo (descenso de gradiente)</h4>
        <button
          type="button"
          className="btn-mini"
          onClick={() => {
            reiniciar();
            setTimeout(entrenar, 150);
          }}
        >
          {corriendo ? "Entrenando…" : "⟳ Reiniciar"}
        </button>
      </div>
      <p>
        Esta animación entrena, en tu navegador y en tiempo real, una regresión simple de{" "}
        <strong>{muestra.yLabel}</strong> sobre <strong>{muestra.xLabel}</strong> (la variable con
        mayor correlación, r = {muestra.corr}) usando descenso de gradiente sobre una muestra real
        de 70 observaciones. El modelo en producción usa regresión lineal <em>múltiple</em> resuelta
        de forma exacta (mínimos cuadrados) con las 3 variables — esta vista es ilustrativa del
        proceso de aprendizaje.
      </p>

      <div className="legend-row">
        <span className="legend-item">
          <span className="legend-dot" style={{ background: COLOR_DATOS }} /> Datos reales
        </span>
        <span className="legend-item">
          <span className="legend-line" style={{ background: COLOR_MODELO }} /> Modelo (recta en
          entrenamiento)
        </span>
      </div>

      <svg ref={scatterSvgRef} viewBox={`0 0 ${VB_W} ${SCATTER_H}`} className="chart-svg">
        {ticksY.map((t, i) => (
          <g key={`gy${i}`}>
            <line x1={MARGIN.left} x2={VB_W - MARGIN.right} y1={sy(t)} y2={sy(t)} className="grid-line" />
            <text x={MARGIN.left - 8} y={sy(t) + 4} textAnchor="end" className="axis-label">
              {t.toFixed(t > 100 ? 0 : 1)}
            </text>
          </g>
        ))}
        {ticksX.map((t, i) => (
          <text key={`tx${i}`} x={sx(t)} y={SCATTER_H - MARGIN.bottom + 20} textAnchor="middle" className="axis-label">
            {t.toFixed(t > 100 ? 0 : 1)}
          </text>
        ))}
        <text x={VB_W / 2} y={SCATTER_H - 4} textAnchor="middle" className="axis-title">
          {muestra.xLabel}
        </text>

        {puntos.map(([x, y], i) => (
          <circle
            key={i}
            cx={sx(x)}
            cy={sy(y)}
            r={hoverPoint === i ? 6 : 4}
            fill={COLOR_DATOS}
            fillOpacity={0.75}
            onMouseEnter={() => setHoverPoint(i)}
            onMouseLeave={() => setHoverPoint(null)}
          />
        ))}

        <line x1={sx(lineX1)} y1={sy(lineY1)} x2={sx(lineX2)} y2={sy(lineY2)} stroke={COLOR_MODELO} strokeWidth={3} strokeLinecap="round" />

        {hoverPoint !== null && (
          <g transform={`translate(${sx(puntos[hoverPoint][0]) + 10}, ${sy(puntos[hoverPoint][1]) - 14})`}>
            <rect width={118} height={34} rx={6} fill="var(--navy-dark)" opacity={0.92} />
            <text x={8} y={14} className="tooltip-text">
              {muestra.xLabel}: {puntos[hoverPoint][0]}
            </text>
            <text x={8} y={27} className="tooltip-text">
              {muestra.yLabel}: {puntos[hoverPoint][1]}
            </text>
          </g>
        )}
      </svg>

      <div className="stat-row" style={{ marginTop: 4 }}>
        <div className="stat-tile">
          <div className="value">{epoch}</div>
          <div className="label">Época</div>
        </div>
        <div className="stat-tile">
          <div className="value">{slopeOrig.toFixed(2)}</div>
          <div className="label">Pendiente</div>
        </div>
        <div className="stat-tile">
          <div className="value">{ultimoMse !== null ? ultimoMse.toFixed(1) : "—"}</div>
          <div className="label">MSE actual</div>
        </div>
      </div>

      <p className="axis-title" style={{ textAlign: "left", marginBottom: 4 }}>
        Error cuadrático medio (MSE) por época
      </p>
      <svg
        ref={lossSvgRef}
        viewBox={`0 0 ${VB_W} ${LOSS_H}`}
        className="chart-svg"
        onMouseMove={handleLossMove}
        onMouseLeave={() => setHoverLoss(null)}
      >
        {[0, 0.5, 1].map((f, i) => (
          <line
            key={i}
            x1={MARGIN.left}
            x2={VB_W - MARGIN.right}
            y1={MARGIN.top + lossPlotH * f}
            y2={MARGIN.top + lossPlotH * f}
            className="grid-line"
          />
        ))}
        <text x={MARGIN.left - 8} y={MARGIN.top + 4} textAnchor="end" className="axis-label">
          {maxMse.toFixed(0)}
        </text>
        <text x={MARGIN.left - 8} y={MARGIN.top + lossPlotH + 4} textAnchor="end" className="axis-label">
          0
        </text>
        <text x={MARGIN.left} y={LOSS_H - 6} textAnchor="middle" className="axis-label">
          0
        </text>
        <text x={VB_W - MARGIN.right} y={LOSS_H - 6} textAnchor="middle" className="axis-label">
          {MAX_EPOCHS}
        </text>
        {historial.length > 1 && <path d={lossPath} fill="none" stroke={COLOR_MODELO} strokeWidth={2} strokeLinecap="round" />}
        {hoverLoss && (
          <>
            <line x1={lx(hoverLoss.epoch)} x2={lx(hoverLoss.epoch)} y1={MARGIN.top} y2={MARGIN.top + lossPlotH} className="crosshair" />
            <g transform={`translate(${Math.min(lx(hoverLoss.epoch) + 8, VB_W - 140)}, ${MARGIN.top + 6})`}>
              <rect width={128} height={32} rx={6} fill="var(--navy-dark)" opacity={0.92} />
              <text x={8} y={13} className="tooltip-text">
                Época {hoverLoss.epoch}
              </text>
              <text x={8} y={26} className="tooltip-text">
                MSE: {hoverLoss.mse.toFixed(2)}
              </text>
            </g>
          </>
        )}
      </svg>
    </div>
  );
}
