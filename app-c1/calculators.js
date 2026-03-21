/* ============================================================
   ADSE Control 1 — Calculadoras Interactivas
   Método estático, CQC, drift checker
   ============================================================ */
'use strict';

// ============================================================
// PARÁMETROS DS61
// ============================================================
const DS61 = {
  zones: { '1': 0.2, '2': 0.3, '3': 0.4 },
  soils: {
    'A': { S: 0.90, T0: 0.15, Tp: 0.20, n: 1.00, p: 2.0 },
    'B': { S: 1.00, T0: 0.30, Tp: 0.35, n: 1.33, p: 1.5 },
    'C': { S: 1.05, T0: 0.40, Tp: 0.45, n: 1.40, p: 1.6 },
    'D': { S: 1.20, T0: 0.75, Tp: 0.85, n: 1.80, p: 1.0 },
    'E': { S: 1.30, T0: 1.20, Tp: 1.35, n: 1.80, p: 1.0 },
  }
};

function calcAlpha(T, soil) {
  const { T0, p } = soil;
  return (1 + 4.5 * Math.pow(T0 / T, p)) / (1 + Math.pow(T0 / T, 3));
}

function calcRstar(T, Ro, soil) {
  return 1 + (Ro - 1) * (T / (0.1 * Ro + T));
}

function calcC(T, zone, soil, Ro) {
  const Ao = DS61.zones[zone] || 0.4;
  const params = DS61.soils[soil] || DS61.soils['C'];
  const S = params.S;
  const alpha = calcAlpha(T, params);
  const Rstar = calcRstar(T, Ro, params);
  const g = 9.81;
  return (S * Ao * alpha) / (g * Rstar);
}

function calcCmin(zone, soil) {
  const Ao = DS61.zones[zone] || 0.4;
  const S = (DS61.soils[soil] || DS61.soils['C']).S;
  return (Ao * S) / (6 * 9.81);
}

function calcCmax(zone, soil) {
  const Ao = DS61.zones[zone] || 0.4;
  const S = (DS61.soils[soil] || DS61.soils['C']).S;
  return (0.35 * S * Ao) / 9.81;
}

// ============================================================
// CALCULADORA MÉTODO ESTÁTICO (MOD7)
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  const calcBtn = document.getElementById('calc-static-btn');
  if (calcBtn) calcBtn.addEventListener('click', runStaticCalc);

  const driftGenBtn = document.getElementById('drift-generate-btn');
  if (driftGenBtn) driftGenBtn.addEventListener('click', generateDriftTable);

  const cqcBtn = document.getElementById('cqc-calc-btn');
  if (cqcBtn) cqcBtn.addEventListener('click', runCQC);
});

function runStaticCalc() {
  const zone = document.getElementById('calc-zone')?.value || '3';
  const soil = document.getElementById('calc-soil')?.value || 'C';
  const Ro = parseFloat(document.getElementById('calc-Ro')?.value || '7');
  const I = parseFloat(document.getElementById('calc-I')?.value || '1.0');
  const T = parseFloat(document.getElementById('calc-T')?.value || '0.8');
  const P = parseFloat(document.getElementById('calc-P')?.value || '5000');
  const N = parseInt(document.getElementById('calc-N')?.value || '10');

  const Ao = DS61.zones[zone];
  const params = DS61.soils[soil];
  const C_calc = calcC(T, zone, soil, Ro);
  const Cmin = calcCmin(zone, soil);
  const Cmax = calcCmax(zone, soil);
  const C = Math.max(Cmin, Math.min(Cmax, C_calc));
  const Qo = C * I * P;

  // Distribute forces by floor
  // Assume uniform weight and equal height per floor
  const h_floor = 3.0; // default
  const w_per_floor = P / N;
  const x = T <= 0.5 ? 1 : (T >= 2.5 ? 2 : 1 + (T - 0.5) / 2);

  let sumWH = 0;
  const floors = [];
  for (let i = 1; i <= N; i++) {
    const hi = i * h_floor;
    const wh = w_per_floor * Math.pow(hi, x);
    sumWH += wh;
    floors.push({ floor: i, hi, w: w_per_floor, wh });
  }

  floors.forEach(f => {
    f.Fi = Qo * f.wh / sumWH;
    f.Vi = floors.filter(fl => fl.floor >= f.floor).reduce((s, fl) => s + fl.Fi, 0);
  });

  // Results HTML
  const results = document.getElementById('calc-static-results');
  if (results) {
    let html = `<div class="calc-result-summary">
      <div class="result-item"><span class="result-label">A<sub>0</sub>:</span><span class="result-value">${Ao}g</span></div>
      <div class="result-item"><span class="result-label">S:</span><span class="result-value">${params.S}</span></div>
      <div class="result-item"><span class="result-label">T<sub>0</sub>:</span><span class="result-value">${params.T0}s</span></div>
      <div class="result-item"><span class="result-label">R*:</span><span class="result-value">${calcRstar(T, Ro, params).toFixed(2)}</span></div>
      <div class="result-item"><span class="result-label">C<sub>calc</sub>:</span><span class="result-value">${C_calc.toFixed(5)}</span></div>
      <div class="result-item"><span class="result-label">C<sub>mín</sub>:</span><span class="result-value">${Cmin.toFixed(5)}</span></div>
      <div class="result-item"><span class="result-label">C<sub>máx</sub>:</span><span class="result-value">${Cmax.toFixed(5)}</span></div>
      <div class="result-item result-highlight"><span class="result-label">C<sub>diseño</sub>:</span><span class="result-value">${C.toFixed(5)}</span></div>
      <div class="result-item result-highlight"><span class="result-label">Q<sub>0</sub>:</span><span class="result-value">${Qo.toFixed(1)} tonf</span></div>
    </div>`;

    if (C_calc < Cmin) html += `<div class="concept-box concept-box-warning"><p>C calculado < C<sub>mín</sub> → se usa <strong>C<sub>mín</sub></strong>. Corte basal gobernado por mínimo.</p></div>`;
    if (C_calc > Cmax) html += `<div class="concept-box concept-box-highlight"><p>C calculado > C<sub>máx</sub> → se usa <strong>C<sub>máx</sub></strong>. Edificio muy rígido.</p></div>`;

    html += `<h4>Distribución de Fuerzas por Piso</h4>
    <div class="table-responsive"><table class="data-table data-table-striped">
      <thead><tr><th>Piso</th><th>h<sub>i</sub> (m)</th><th>w<sub>i</sub> (tonf)</th><th>F<sub>i</sub> (tonf)</th><th>V<sub>i</sub> (tonf)</th></tr></thead>
      <tbody>`;
    floors.forEach(f => {
      html += `<tr><td>${f.floor}</td><td>${f.hi.toFixed(1)}</td><td>${f.w.toFixed(1)}</td><td>${f.Fi.toFixed(2)}</td><td>${f.Vi.toFixed(2)}</td></tr>`;
    });
    html += `</tbody></table></div>`;
    results.innerHTML = html;

    // Render MathJax if available
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([results]).catch(() => {});
  }

  // Force distribution chart (horizontal bars)
  const chartCanvas = document.getElementById('mod7-force-dist-chart');
  if (chartCanvas && typeof Chart !== 'undefined') {
    if (window._forceDistChart) window._forceDistChart.destroy();
    window._forceDistChart = new Chart(chartCanvas, {
      type: 'bar',
      data: {
        labels: floors.map(f => `Piso ${f.floor}`),
        datasets: [
          { label: 'Fi (tonf)', data: floors.map(f => f.Fi), backgroundColor: '#00d4ff', borderRadius: 4 },
          { label: 'Vi (tonf)', data: floors.map(f => f.Vi), backgroundColor: 'rgba(168,85,247,0.5)', borderRadius: 4 }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
          title: { display: true, text: 'Fuerza por Piso (Fi) y Corte Acumulado (Vi)', color: '#e0e0e0' },
          legend: { labels: { color: '#ccc' } }
        },
        scales: {
          x: { title: { display: true, text: 'Fuerza (tonf)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } },
          y: { grid: { display: false }, ticks: { color: '#aaa' } }
        }
      }
    });
  }
}

// ============================================================
// VERIFICADOR DE DRIFT (MOD8)
// ============================================================
function generateDriftTable() {
  const N = parseInt(document.getElementById('drift-floors')?.value || '5');
  const h = parseFloat(document.getElementById('drift-height')?.value || '2.8');
  const container = document.getElementById('drift-table-container');
  if (!container) return;

  let html = `<table class="data-table data-table-striped">
    <thead><tr><th>Piso</th><th>u<sub>CM</sub> (mm)</th><th>u<sub>max</sub> (mm)</th><th>drift CM</th><th>drift max</th><th>Estado</th></tr></thead>
    <tbody>`;

  for (let i = 1; i <= N; i++) {
    // Default values (triangular displacement)
    const u_cm = (i * 5).toFixed(1);
    const u_max = (i * 7).toFixed(1);
    html += `<tr>
      <td>${i}</td>
      <td><input type="number" class="drift-input drift-cm" data-floor="${i}" value="${u_cm}" step="0.1" style="width:70px"></td>
      <td><input type="number" class="drift-input drift-max" data-floor="${i}" value="${u_max}" step="0.1" style="width:70px"></td>
      <td class="drift-val-cm" data-floor="${i}">--</td>
      <td class="drift-val-max" data-floor="${i}">--</td>
      <td class="drift-status" data-floor="${i}">--</td>
    </tr>`;
  }
  html += `</tbody></table>
    <button class="btn btn-primary mt-sm" id="drift-check-btn">Verificar Drift</button>`;
  container.innerHTML = html;

  document.getElementById('drift-check-btn')?.addEventListener('click', () => checkDrift(N, h));
}

function checkDrift(N, h) {
  const hm = h * 1000; // convert to mm
  const drifts = [];

  for (let i = 1; i <= N; i++) {
    const ucm = parseFloat(document.querySelector(`.drift-cm[data-floor="${i}"]`)?.value || '0');
    const umax = parseFloat(document.querySelector(`.drift-max[data-floor="${i}"]`)?.value || '0');
    const ucm_prev = i > 1 ? parseFloat(document.querySelector(`.drift-cm[data-floor="${i - 1}"]`)?.value || '0') : 0;
    const umax_prev = i > 1 ? parseFloat(document.querySelector(`.drift-max[data-floor="${i - 1}"]`)?.value || '0') : 0;

    const delta_cm = ucm - ucm_prev;
    const delta_max = umax - umax_prev;
    const drift_cm = delta_cm / hm;
    const drift_max = delta_max / hm;

    const ok_cm = drift_cm <= 0.002;
    const ok_max = drift_max <= 0.001;

    const cmEl = document.querySelector(`.drift-val-cm[data-floor="${i}"]`);
    const maxEl = document.querySelector(`.drift-val-max[data-floor="${i}"]`);
    const statusEl = document.querySelector(`.drift-status[data-floor="${i}"]`);

    if (cmEl) { cmEl.textContent = drift_cm.toFixed(5); cmEl.style.color = ok_cm ? '#22c55e' : '#ef4444'; }
    if (maxEl) { maxEl.textContent = drift_max.toFixed(5); maxEl.style.color = ok_max ? '#22c55e' : '#ef4444'; }
    if (statusEl) {
      if (ok_cm && ok_max) { statusEl.textContent = '✓ OK'; statusEl.style.color = '#22c55e'; }
      else { statusEl.textContent = '✗ NO CUMPLE'; statusEl.style.color = '#ef4444'; }
    }

    drifts.push({ floor: i, drift_cm, drift_max, ok_cm, ok_max });
  }

  // Drift chart
  const chartCanvas = document.getElementById('mod8-drift-chart');
  if (chartCanvas && typeof Chart !== 'undefined') {
    if (window._driftChart) window._driftChart.destroy();
    window._driftChart = new Chart(chartCanvas, {
      type: 'bar',
      data: {
        labels: drifts.map(d => `Piso ${d.floor}`),
        datasets: [
          {
            label: 'Drift CM',
            data: drifts.map(d => d.drift_cm * 1000), // x1000 for visibility
            backgroundColor: drifts.map(d => d.ok_cm ? '#22c55e' : '#ef4444'),
            borderRadius: 4
          },
          {
            label: 'Drift máx',
            data: drifts.map(d => d.drift_max * 1000),
            backgroundColor: drifts.map(d => d.ok_max ? '#06b6d4' : '#ff6b35'),
            borderRadius: 4
          }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
          title: { display: true, text: 'Drift por Piso (×10⁻³)', color: '#e0e0e0' },
          legend: { labels: { color: '#ccc' } },
          annotation: {
            annotations: {
              line1: { type: 'line', xMin: 2, xMax: 2, borderColor: '#ef4444', borderWidth: 2, borderDash: [5, 5], label: { display: true, content: '0.002', color: '#ef4444' } },
              line2: { type: 'line', xMin: 1, xMax: 1, borderColor: '#ff6b35', borderWidth: 2, borderDash: [5, 5], label: { display: true, content: '0.001', color: '#ff6b35' } }
            }
          }
        },
        scales: {
          x: { title: { display: true, text: 'Drift (×10⁻³)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } },
          y: { grid: { display: false }, ticks: { color: '#aaa' } }
        }
      }
    });
  }
}

// ============================================================
// CALCULADORA CQC (MOD8)
// ============================================================
function runCQC() {
  const xi = parseFloat(document.getElementById('cqc-xi')?.value || '0.05');
  const Ts = [...document.querySelectorAll('.cqc-T')].map(el => parseFloat(el.value));
  const rs = [...document.querySelectorAll('.cqc-r')].map(el => parseFloat(el.value));

  const n = Math.min(Ts.length, rs.length);
  if (n < 2) return;

  const omegas = Ts.map(T => 2 * Math.PI / T);

  // Calculate correlation matrix
  const rho = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) { rho[i][j] = 1; continue; }
      const beta = omegas[i] / omegas[j];
      rho[i][j] = (8 * xi * xi * (1 + beta) * Math.pow(beta, 1.5)) /
        (Math.pow(1 - beta * beta, 2) + 4 * xi * xi * beta * Math.pow(1 + beta, 2));
    }
  }

  // CQC combination
  let sumCQC = 0;
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      sumCQC += rs[i] * rho[i][j] * rs[j];
    }
  }
  const rCQC = Math.sqrt(sumCQC);

  // SRSS for comparison
  const rSRSS = Math.sqrt(rs.reduce((s, r) => s + r * r, 0));

  // Results
  const results = document.getElementById('cqc-results');
  if (!results) return;

  let html = `<div class="calc-result-summary">
    <div class="result-item result-highlight"><span class="result-label">r<sub>CQC</sub>:</span><span class="result-value">${rCQC.toFixed(2)}</span></div>
    <div class="result-item"><span class="result-label">r<sub>SRSS</sub>:</span><span class="result-value">${rSRSS.toFixed(2)}</span></div>
    <div class="result-item"><span class="result-label">Diferencia:</span><span class="result-value">${((rCQC / rSRSS - 1) * 100).toFixed(1)}%</span></div>
  </div>`;

  // Correlation matrix
  html += `<h4>Matriz de Correlación ρ<sub>ij</sub></h4>
    <div class="table-responsive"><table class="data-table matrix-table">
    <thead><tr><th></th>`;
  for (let j = 0; j < n; j++) html += `<th>Modo ${j + 1}</th>`;
  html += `</tr></thead><tbody>`;
  for (let i = 0; i < n; i++) {
    html += `<tr><td><strong>Modo ${i + 1}</strong></td>`;
    for (let j = 0; j < n; j++) {
      const val = rho[i][j];
      const cls = i === j ? 'diagonal' : (val > 0.1 ? 'off-diagonal' : 'zero');
      html += `<td class="${cls}">${val.toFixed(4)}</td>`;
    }
    html += `</tr>`;
  }
  html += `</tbody></table></div>`;

  // Modal contributions
  html += `<h4>Contribuciones Modales</h4><table class="data-table data-table-striped">
    <thead><tr><th>Modo</th><th>T (s)</th><th>r<sub>i</sub></th><th>r<sub>i</sub>²</th><th>% del total SRSS</th></tr></thead><tbody>`;
  rs.forEach((r, i) => {
    const pct = rSRSS > 0 ? ((r * r) / (rSRSS * rSRSS) * 100).toFixed(1) : '0';
    html += `<tr><td>${i + 1}</td><td>${Ts[i].toFixed(3)}</td><td>${r.toFixed(2)}</td><td>${(r * r).toFixed(2)}</td><td>${pct}%</td></tr>`;
  });
  html += `</tbody></table>`;

  if (Math.abs(rCQC - rSRSS) / rSRSS > 0.05) {
    html += `<div class="concept-box concept-box-warning"><p>Diferencia > 5% entre CQC y SRSS. Esto indica <strong>acoplamiento modal significativo</strong>. Se recomienda usar CQC.</p></div>`;
  } else {
    html += `<div class="concept-box concept-box-highlight"><p>CQC ≈ SRSS (< 5% diferencia). Modos bien separados, ambos métodos son equivalentes.</p></div>`;
  }

  results.innerHTML = html;
}
