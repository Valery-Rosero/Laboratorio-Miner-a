// Configuración de los tres ejercicios — replica los mismos campos, rangos y
// métricas del modelo entrenado en /src (ver INFORME.pdf para el detalle).

export const EJERCICIOS = {
  Dolar: {
    nombre: "Dólar",
    descripcion:
      "Predicción del precio del dólar a partir del día, la inflación y la tasa de interés.",
    unidad: "COP",
    metrics: { r2Test: 0.9132, rmseTest: 81.27, r2CV: 0.9249 },
    inputs: [
      { key: "Dia", label: "Día (número de día)", min: 1, max: 3650, value: 225, step: 1 },
      { key: "Inflacion", label: "Inflación (%)", min: 0, max: 20, value: 6, step: 0.1 },
      { key: "Tasa_interes", label: "Tasa de interés (%)", min: 0, max: 25, value: 7, step: 0.1 },
    ],
  },
  Glucosa: {
    nombre: "Glucosa",
    descripcion:
      "Predicción del nivel de glucosa en sangre a partir de edad, IMC y actividad física.",
    unidad: "mg/dL",
    metrics: { r2Test: 0.9352, rmseTest: 5.62, r2CV: 0.927 },
    inputs: [
      { key: "Edad", label: "Edad (años)", min: 0, max: 120, value: 45, step: 1 },
      { key: "IMC", label: "Índice de Masa Corporal (IMC)", min: 10, max: 60, value: 25, step: 0.1 },
      {
        key: "Actividad_Fisica",
        label: "Actividad física (horas/semana)",
        min: 0,
        max: 30,
        value: 3,
        step: 0.5,
      },
    ],
  },
  Energia: {
    nombre: "Energía",
    descripcion:
      "Predicción del consumo de energía eléctrica a partir de temperatura, hora del día y día de la semana.",
    unidad: "kWh",
    metrics: { r2Test: 0.934, rmseTest: 4.93, r2CV: 0.9372 },
    inputs: [
      { key: "Temperatura", label: "Temperatura (°C)", min: -20, max: 55, value: 20, step: 0.5 },
      { key: "Hora", label: "Hora del día (1 a 24)", min: 1, max: 24, value: 12, step: 1 },
      {
        key: "Dia_Semana",
        label: "Día de la semana (1=Lunes ... 7=Domingo)",
        min: 1,
        max: 7,
        value: 1,
        step: 1,
      },
    ],
  },
};
