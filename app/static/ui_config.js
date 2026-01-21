window.UI_CONFIG = {
  pageTitle: "CHD Predictor",
  title: "Coronary Heart Disease Predictor",
  subtitle: `
    Welcome to the Coronary Heart Disease Predictor! 
    By entering your patient's data and clicking 'Predict', we will give you the
    patient's probability of developing a coronary heart disease within the next 10 years.
  `,
  theme: {
    primary: "#7B53C6",
    background: "#E6CCFF",
    card: "#CA9EFF",
    text: "#000000",
    mutedText: "#642A7E",
    border: "#7B53C6",

    // Risk-based result colors
    riskLow: "#1B7F3A",
    riskMed: "#B7791F",
    riskHigh: "#B42318",
    riskLowBg: "#EAF6EE",
    riskMedBg: "#FFF4E5",
    riskHighBg: "#FDECEC"
  },

  // Results display
  result: {
    title: "Prediction",
    showTable: true,
    // Probability thresholds for UI coloring
    uiRiskBands: [
      { 
          max: 0.25,
          label: "Low risk",
          colorKey: "riskLow"
      },
      { 
          max: 0.60,
          label: "Moderate risk",
          colorKey: "riskMed"
      },
      { 
          max: 1.00,
          label: "High risk",
          colorKey: "riskHigh"
      }
    ],
    summaryTemplate: (resp) => {
      const pct = (resp.probability * 100).toFixed(1);
      return `Estimated 10-year CHD probability: ${pct}%`;
    },
    tableOrder: ["prediction", "probability", "threshold", "roc_auc", "model_version"],
    tableLabels: {
      prediction: "Prediction (0 = no, 1 = yes)",
      probability: "Probability",
      threshold: "Decision threshold",
      roc_auc: "ROC-AUC (test)",
      model_version: "Model version"
    },
    tableFormatters: {
      probability: (v) => (v * 100).toFixed(1) + "%",
      roc_auc: (v) => (v == null ? "—" : Number(v).toFixed(3))
    }
  },

  // Field groups and sections
  sections: [
    {
      title: "Demographics",
      description: "Basic demographic information.",
      fields: [
        {
          id: "sex",
          label: "Sex",
          description: "0 = female, 1 = male",
          type: "select",
          options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
          default: 0
        },
        {
          id: "age",
          label: "Age",
          description: "Age in years.",
          type: "range",
          min: 0,
          max: 120,
          step: 1,
          default: 45,
          valueType: "int"
        },
        {
          id: "education_level",
          label: "Education level",
          description: "Ordinal scale 1–4.",
          type: "range",
          min: 1,
          max: 4,
          step: 1,
          default: 2,
          valueType: "int"
        }
      ]
    },
    {
      title: "Smoking",
      fields: [
        {
          id: "current_smoker",
          label: "Current Smoker",
          description: "0 = no, 1 = yes",
          type: "select",
          options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
          default: 0
        },
        {
          id: "cigs_per_day",
          label: "Cigarettes per day",
          description: "Average number of cigarettes smoked per day (0 if non-smoker).",
          type: "range",
          min: 0,
          max: 100,
          step: 1,
          default: 1,
          valueType: "int"
        }
      ]
    },
    {
      title: "Clinical history",
      description: "Key conditions and medication.",
      fields: [
        {
            id: "bp_meds",
            label: "Takes Blood Pressure Medication?",
            description: "0 = no, 1 = yes",
            type: "select",
            options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
            default: 0
        },
        { 
            id: "prevalent_stroke",
            label: "Has Ever Had a Stroke?",
            description: "0 = no, 1 = yes",
            type: "select",
            options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
            default: 0
        },
        {
            id: "prevalent_hypertension",
            label: "Has Hypertension?",
            description: "0 = no, 1 = yes",
            type: "select",
            options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
            default: 0
        },
        { 
            id: "diabetes",
            label: "Has Diabetes?", 
            description: "0 = no, 1 = yes",
            type: "select",
            options: [{ label: "0", value: 0 }, { label: "1", value: 1 }],
            default: 0
        }
      ]
    },
    {
      title: "Vitals and Labs",
      description: "Patient's measurements.",
      fields: [
        { 
            id: "total_cholesterol",
            label: "Cholesterol",
            description: "Total cholesterol in mg/dL.",
            type: "range",
            min: 100,
            max: 800,
            step: 1,
            default: 200,
            valueType: "float"
        },
        { 
            id: "systolic_bp",
            label: "Systolic Blood Pressure",
            description: "Systolic blood pressure in mmHg.",
            type: "range",
            min: 80,
            max: 250,
            step: 1,
            default: 120,
            valueType: "float"
        },
        { 
            id: "diastolic_bp",
            label: "Diastolic Blood Pressure",
            description: "Diastolic blood pressure in mmHg.",
            type: "range",
            min: 40,
            max: 160,
            step: 1,
            default: 80,
            valueType: "float"
        },
        {
            id: "bmi",
            label: "BMI",
            description: "Body mass index (kg/m²).",
            type: "range",
            min: 10,
            max: 100,
            step: 0.1,
            default: 25.0,
            valueType: "float"
        },
        {
            id: "heart_rate",
            label: "Heart Rate",
            description: "Heart rate (beats per minute).",
            type: "range",
            min: 30,
            max: 220,
            step: 1,
            default: 72,
            valueType: "int"
        },
        {
            id: "glucose",
            label: "Blood Glucose Level",
            description: "Blood glucose level in mg/dL.",
            type: "range",
            min: 40,
            max: 600,
            step: 1,
            default: 85,
            valueType: "float"
        }
      ]
    }
  ]
};
