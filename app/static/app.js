(function () {
  const cfg = window.UI_CONFIG;

  const rootStyle = document.documentElement.style;
  rootStyle.setProperty("--primary", cfg.theme.primary);
  rootStyle.setProperty("--bg", cfg.theme.background);
  rootStyle.setProperty("--card", cfg.theme.card);
  rootStyle.setProperty("--text", cfg.theme.text);
  rootStyle.setProperty("--muted", cfg.theme.mutedText);
  rootStyle.setProperty("--border", cfg.theme.border);
  rootStyle.setProperty("--riskLow", cfg.theme.riskLow);
  rootStyle.setProperty("--riskMed", cfg.theme.riskMed);
  rootStyle.setProperty("--riskHigh", cfg.theme.riskHigh);
  rootStyle.setProperty("--riskLowBg", cfg.theme.riskLowBg);
  rootStyle.setProperty("--riskMedBg", cfg.theme.riskMedBg);
  rootStyle.setProperty("--riskHighBg", cfg.theme.riskHighBg);

  document.getElementById("page-title").textContent = cfg.pageTitle;
  document.getElementById("app-title").textContent = cfg.title;
  document.getElementById("app-subtitle").textContent = cfg.subtitle;
  document.getElementById("result-title").textContent = cfg.result.title;

  const formRoot = document.getElementById("form-root");
  const resultSummary = document.getElementById("result-summary");
  const resultBox = document.getElementById("result-box");

  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k === "html") node.innerHTML = v;
      else node.setAttribute(k, v);
    }
    for (const c of children) node.appendChild(c);
    return node;
  }

  function buildField(field) {
    const wrap = el("div", { class: "field" });
    wrap.appendChild(el("label", { for: field.id, html: field.label }));

    if (field.description) {
      wrap.appendChild(el("div", { class: "desc", html: field.description }));
    }

    if (field.type === "select") {
      const sel = el("select", { id: field.id });
      for (const opt of field.options) {
        const o = el("option", { value: String(opt.value), html: opt.label });
        if (opt.value === field.default) o.selected = true;
        sel.appendChild(o);
      }
      wrap.appendChild(sel);
      return wrap;
    }

    if (field.type === "range") {
      const row = el("div", { class: "row" });
      const num = el("input", {
        id: field.id + "_num",
        type: "number",
        min: String(field.min),
        max: String(field.max),
        step: String(field.step),
        value: String(field.default)
      });

      const slider = el("input", {
        id: field.id,
        type: "range",
        min: String(field.min),
        max: String(field.max),
        step: String(field.step),
        value: String(field.default)
      });

      const out = el("span", {
          id: field.id + "_val",
          class: "val",
          html: String(field.default)
      });

      slider.addEventListener("input", () => {
        num.value = slider.value;
        out.textContent = slider.value;
      });
      num.addEventListener("input", () => {
        slider.value = num.value;
        out.textContent = num.value;
      });

      row.appendChild(num);
      row.appendChild(slider);
      row.appendChild(out);
      wrap.appendChild(row);
      return wrap;
    }
  }

  function renderForm() {
    formRoot.innerHTML = "";
    for (const section of cfg.sections) {
      const card = el("section", { class: "card" });
      card.appendChild(el("h2", { class: "card-title", html: section.title }));
      if (section.description) {
        card.appendChild(el("p", { class: "muted", html: section.description }));
      }

      const grid = el("div", { class: "grid" });
      for (const f of section.fields) grid.appendChild(buildField(f));
      card.appendChild(grid);

      formRoot.appendChild(card);
    }
  }

  function collectPayload() {
    const payload = {};
    for (const section of cfg.sections) {
      for (const f of section.fields) {
        if (f.type === "select") {
          payload[f.id] = parseInt(document.getElementById(f.id).value, 10);
        } else if (f.type === "range") {
          const v = document.getElementById(f.id + "_num").value;
          if (f.valueType === "int") payload[f.id] = parseInt(v, 10);
          else payload[f.id] = parseFloat(v);
        }
      }
    }
    return payload;
  }

  function formatValue(key, value) {
    const fmts = (cfg.result && cfg.result.tableFormatters);
    if (key in fmts && typeof fmts[key] === "function") return fmts[key](value);
  
    return String(value);
  }
  
  function renderJsonTable(data) {
    const container = document.getElementById("result-table");
    container.style.display = "block";
  
    const labels = cfg.result.tableLabels;
  
    const rows = [];
    for (const k of cfg.result.tableOrder) {
      if (!(k in data)) continue;
      const label = labels[k];
      const val = formatValue(k, data[k]);
      rows.push(`<tr><th>${label}</th><td>${val}</td></tr>`);
    }
    container.innerHTML = `<table>${rows.join("")}</table>`;
  }
  

  function riskBand(prob) {
    for (const band of cfg.result.uiRiskBands) {
      if (prob <= band.max) return band;
    }
  }

  async function predict() {
    const payload = collectPayload();
    resultSummary.textContent = "Predicting ...";

    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const text = await resp.text();
    if (!resp.ok) {
      resultSummary.textContent = `Error ${resp.status}`;
      return;
    }

    const data = JSON.parse(text);

    resultSummary.textContent = cfg.result.summaryTemplate
      ? cfg.result.summaryTemplate(data)
      : `Probability: ${data.probability}`;

    // Risk coloring
    const band = riskBand(data.probability);
    const styles = getComputedStyle(document.documentElement);

    const borderColorVar = `--${band.colorKey}`;
    const bgKey = band.colorKey + "Bg";
    const bgColorVar = `--${bgKey}`;

    resultBox.style.borderColor = styles.getPropertyValue(borderColorVar).trim();
    resultBox.style.backgroundColor = styles.getPropertyValue(bgColorVar).trim();
    
    renderJsonTable(data);
  }

// Reset to defaults
  function reset() {
    for (const section of cfg.sections) {
      for (const f of section.fields) {
        if (f.type === "select") {
          document.getElementById(f.id).value = String(f.default);
        } else if (f.type === "range") {
          document.getElementById(f.id).value = String(f.default);
          document.getElementById(f.id + "_num").value = String(f.default);
          document.getElementById(f.id + "_val").textContent = String(f.default);
        }
      }
    }
    resultSummary.textContent = "No prediction yet.";
    resultBox.style.borderColor = "var(--border)";
    resultBox.style.backgroundColor = "transparent";
    const table = document.getElementById("result-table");
    table.innerHTML = "";
  }

  document.getElementById("predict-btn").addEventListener("click", predict);
  document.getElementById("reset-btn").addEventListener("click", reset);

  renderForm();
  reset();
})();
