/* ============================================================
   ADSE Control 1 — Módulos Interactivos Extendidos
   Nuevas visualizaciones y mejoras a módulos existentes
   ============================================================ */
'use strict';

const newModuleInited = new Set();

window.initNewFeatures = function(moduleId) {
  if (newModuleInited.has(moduleId)) return;
  newModuleInited.add(moduleId);
  switch (moduleId) {
    case 'mod1': initMod1ZoneMap(); break;
    case 'mod2': initMod2Hysteresis(); break;
    case 'mod3': initMod3Enhanced(); break;
    case 'mod6': initMod6Enhanced(); break;
    case 'mod8': initMod8Enhanced(); break;
  }
};

// ============================================================
// MOD2: LAZO HISTERÉTICO INTERACTIVO
// ============================================================
function initMod2Hysteresis() {
  const canvas = document.getElementById('mod2-hysteresis-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  function generateHysteresis(mu) {
    const Fy = 100;
    const dy = 10;
    const du = dy * mu;
    const k = Fy / dy;
    const kh = k * 0.02; // post-yield stiffness
    const points = [];
    // Loading
    for (let d = 0; d <= du; d += 0.5) {
      if (d <= dy) points.push({ x: d, y: k * d });
      else points.push({ x: d, y: Fy + kh * (d - dy) });
    }
    // Unloading from du
    const Fu = Fy + kh * (du - dy);
    const d_residual = du - Fu / k;
    for (let d = du; d >= d_residual; d -= 0.5) {
      points.push({ x: d, y: Fu - k * (du - d) });
    }
    // Reloading negative
    for (let d = d_residual; d >= -du; d -= 0.5) {
      if (d >= -dy + d_residual) points.push({ x: d, y: -k * (d_residual - d) });
      else points.push({ x: d, y: -Fy + kh * (d + du) });
    }
    // Unloading from -du
    for (let d = -du; d <= -d_residual; d += 0.5) {
      points.push({ x: d, y: -Fu + k * (d + du) });
    }
    // Return to zero area
    for (let d = -d_residual; d <= du * 0.5; d += 0.5) {
      if (d <= dy - d_residual) points.push({ x: d, y: k * (d + d_residual) });
      else points.push({ x: d, y: Fy + kh * (d - dy + d_residual) });
    }
    return points;
  }

  function generateElastic() {
    const points = [];
    for (let d = 0; d <= 30; d += 0.5) points.push({ x: d, y: d * 10 });
    for (let d = 30; d >= -30; d -= 0.5) points.push({ x: d, y: d * 10 });
    for (let d = -30; d <= 0; d += 0.5) points.push({ x: d, y: d * 10 });
    return points;
  }

  const chart = new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Lazo histerético (μ=4)',
          data: generateHysteresis(4),
          borderColor: '#a855f7', showLine: true, pointRadius: 0, borderWidth: 2,
          fill: true, backgroundColor: 'rgba(168,85,247,0.15)'
        },
        {
          label: 'Elástico (μ=1)',
          data: generateElastic(),
          borderColor: '#00d4ff', showLine: true, pointRadius: 0, borderWidth: 1,
          borderDash: [4, 4]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Lazo Histerético — Energía Disipada', color: '#e0e0e0' },
        legend: { labels: { color: '#ccc' } }
      },
      scales: {
        x: { title: { display: true, text: 'Deformación δ (mm)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } },
        y: { title: { display: true, text: 'Fuerza F (kN)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } }
      }
    }
  });

  const slider = document.getElementById('mod2-ductility-slider');
  const valEl = document.getElementById('mod2-ductility-value');
  if (slider) {
    slider.addEventListener('input', () => {
      const mu = parseFloat(slider.value);
      if (valEl) valEl.textContent = mu.toFixed(1);
      chart.data.datasets[0].data = generateHysteresis(mu);
      chart.data.datasets[0].label = `Lazo histerético (μ=${mu})`;
      chart.update();
    });
  }
}

// ============================================================
// MOD3: MEJORAS A LA SIMULACIÓN 3D
// ============================================================
function initMod3Enhanced() {
  // Add intensity slider and floor slider if they exist
  const intensitySlider = document.getElementById('mod3-intensity-slider');
  const floorSlider = document.getElementById('mod3-floor-slider');

  if (intensitySlider) {
    intensitySlider.addEventListener('input', () => {
      const val = parseFloat(intensitySlider.value);
      const label = document.getElementById('mod3-intensity-value');
      if (label) label.textContent = val.toFixed(1) + 'g';
    });
  }
}

// ============================================================
// MOD6: DEFORMADA INTERACTIVA + CHART
// ============================================================
function initMod6Enhanced() {
  const canvas = document.getElementById('mod6-deformation-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  const floors = 10;
  const marcoData = [], muroData = [];
  for (let i = 0; i <= floors; i++) {
    const h = i / floors;
    // Marco: shear-type deformation (larger drift at base)
    marcoData.push({ x: 1 - Math.pow(1 - h, 2), y: h * 100 });
    // Muro: flexure-type deformation (larger drift at top)
    muroData.push({ x: Math.pow(h, 1.5), y: h * 100 });
  }

  new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: [
        { label: 'Marco (Tipo I) — Corte', data: marcoData, borderColor: '#00d4ff', showLine: true, pointRadius: 3, borderWidth: 2 },
        { label: 'Muro (Tipo III) — Flexión', data: muroData, borderColor: '#a855f7', showLine: true, pointRadius: 3, borderWidth: 2 }
      ]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: {
        title: { display: true, text: 'Deformada Característica: Marco vs Muro', color: '#e0e0e0' },
        legend: { labels: { color: '#ccc' } }
      },
      scales: {
        x: { title: { display: true, text: 'Desplazamiento lateral normalizado', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0, max: 1.1 },
        y: { title: { display: true, text: 'Altura (%)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0, max: 100 }
      }
    }
  });
}

// ============================================================
// MOD8: MODOS MEJORADOS — PISOS VARIABLES + ANIMACIÓN
// ============================================================
function initMod8Enhanced() {
  const canvas = document.getElementById('mod8-modes-canvas');
  if (!canvas) return;
  // Set canvas coordinate space to match container
  canvas.width = canvas.parentElement?.clientWidth || 600;
  canvas.height = 400;
  const ctx = canvas.getContext('2d');

  let currentMode = 1;
  let nFloors = parseInt(document.getElementById('mod8-num-floors')?.value || '5');
  let animating = false;
  let animFrame = 0;

  function getModeShape(mode, n) {
    const shape = [];
    for (let i = 1; i <= n; i++) {
      shape.push(Math.sin(mode * Math.PI * i / (2 * n + 1)));
    }
    // Normalize to max = 1
    const maxVal = Math.max(...shape.map(Math.abs));
    return shape.map(v => v / maxVal);
  }

  function drawMode(mode, n, phase) {
    const W = canvas.width || canvas.parentElement?.clientWidth || 600;
    const H = canvas.height || 400;
    ctx.clearRect(0, 0, W, H);
    const shape = getModeShape(mode, n);
    const baseX = W / 2, baseY = H - 40;
    const floorH = (H - 80) / n;
    const maxDisp = 80;
    const amp = phase !== undefined ? Math.sin(phase) : 1;

    // Title
    ctx.fillStyle = '#e0e0e0'; ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'center';
    ctx.fillText(`Modo ${mode} — ${n} pisos`, W / 2, 25);

    // Period estimate
    const Tbase = 0.08 * n; // approximate
    const Tn = Tbase / mode;
    ctx.fillStyle = '#aaa'; ctx.font = '12px Inter';
    ctx.fillText(`T${mode} ≈ ${Tn.toFixed(2)}s`, W / 2, 42);

    // Undeformed (dashed)
    ctx.setLineDash([4, 4]); ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(baseX, baseY);
    for (let i = 0; i < n; i++) ctx.lineTo(baseX, baseY - (i + 1) * floorH);
    ctx.stroke(); ctx.setLineDash([]);

    // Deformed shape
    const grad = ctx.createLinearGradient(0, H, 0, 0);
    grad.addColorStop(0, '#00d4ff'); grad.addColorStop(1, '#a855f7');
    ctx.strokeStyle = grad; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(baseX, baseY);
    for (let i = 0; i < n; i++) {
      const x = baseX + shape[i] * maxDisp * amp;
      const y = baseY - (i + 1) * floorH;
      ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Floor markers
    for (let i = 0; i < n; i++) {
      const x = baseX + shape[i] * maxDisp * amp;
      const y = baseY - (i + 1) * floorH;
      // Floor line
      ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(baseX - maxDisp - 20, y); ctx.lineTo(baseX + maxDisp + 20, y); ctx.stroke();
      // Node
      ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#00d4ff'; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
      // Labels (only show some to avoid clutter)
      if (n <= 10 || (i + 1) % Math.ceil(n / 10) === 0 || i === n - 1) {
        ctx.fillStyle = '#aaa'; ctx.font = '10px Inter'; ctx.textAlign = 'right';
        ctx.fillText(`${i + 1}`, baseX - maxDisp - 25, y + 4);
        ctx.textAlign = 'left';
        ctx.fillText(`φ=${(shape[i] * amp).toFixed(2)}`, baseX + maxDisp + 25, y + 4);
      }
    }

    // Ground
    ctx.fillStyle = '#444'; ctx.fillRect(baseX - maxDisp - 20, baseY, maxDisp * 2 + 40, 3);
    for (let i = 0; i < 15; i++) {
      const sx = baseX - maxDisp - 20 + i * 12;
      ctx.strokeStyle = '#555'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(sx, baseY + 3); ctx.lineTo(sx - 8, baseY + 12); ctx.stroke();
    }

    // Mass participation estimate
    const L = shape.reduce((s, v) => s + v, 0);
    const M = shape.reduce((s, v) => s + v * v, 0);
    const massPct = Math.round((L * L / (M * n)) * 100);
    ctx.fillStyle = '#ff6b35'; ctx.font = 'bold 12px Inter'; ctx.textAlign = 'center';
    ctx.fillText(`Masa participante ≈ ${massPct}%`, W / 2, H - 10);
  }

  // Initial draw
  drawMode(1, nFloors);

  // Mode selector
  const modeSelector = document.getElementById('mod8-mode-selector');
  if (modeSelector) {
    modeSelector.querySelectorAll('.mode-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        modeSelector.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMode = parseInt(btn.dataset.mode);
        animating = false;
        drawMode(currentMode, nFloors);
      });
    });
  }

  // Floor count
  const floorInput = document.getElementById('mod8-num-floors');
  if (floorInput) {
    floorInput.addEventListener('change', () => {
      nFloors = Math.max(2, Math.min(20, parseInt(floorInput.value) || 5));
      floorInput.value = nFloors;
      animating = false;
      drawMode(currentMode, nFloors);
    });
  }

  // Animate button
  const animBtn = document.getElementById('mod8-animate');
  if (animBtn) {
    animBtn.addEventListener('click', () => {
      if (animating) {
        animating = false;
        animBtn.textContent = '▶ Animar';
        return;
      }
      animating = true;
      animBtn.textContent = '⏸ Detener';
      animFrame = 0;
      function animLoop() {
        if (!animating) return;
        animFrame += 0.05;
        drawMode(currentMode, nFloors, animFrame);
        requestAnimationFrame(animLoop);
      }
      animLoop();
    });
  }
}

// ============================================================
// MOD1: MAPA DE ZONIFICACIÓN SÍSMICA INTERACTIVO
// ============================================================
function initMod1ZoneMap() {
  const mapContainer = document.getElementById('mod1-zone-map');
  const infoPanel = document.getElementById('mod1-zone-info');
  if (!mapContainer) return;

  const zones = [
    {
      id: 1, name: 'Zona 1', Ao: '0.20g', color: '#22c55e',
      cities: 'Punta Arenas, Coyhaique',
      desc: 'Sismicidad baja. Extremo sur patagónico.',
      soils: { A: { S: 0.90, T0: 0.15, Tp: 0.20, n: 1.00 }, B: { S: 1.00, T0: 0.30, Tp: 0.35, n: 1.33 }, C: { S: 1.05, T0: 0.40, Tp: 0.45, n: 1.40 }, D: { S: 1.20, T0: 0.75, Tp: 0.85, n: 1.80 }, E: { S: 1.30, T0: 1.20, Tp: 1.35, n: 1.80 } }
    },
    {
      id: 2, name: 'Zona 2', Ao: '0.30g', color: '#eab308',
      cities: 'Santiago, Temuco, Osorno',
      desc: 'Sismicidad moderada. Zona central interior.',
      soils: { A: { S: 0.90, T0: 0.15, Tp: 0.20, n: 1.00 }, B: { S: 1.00, T0: 0.30, Tp: 0.35, n: 1.33 }, C: { S: 1.05, T0: 0.40, Tp: 0.45, n: 1.40 }, D: { S: 1.20, T0: 0.75, Tp: 0.85, n: 1.80 }, E: { S: 1.30, T0: 1.20, Tp: 1.35, n: 1.80 } }
    },
    {
      id: 3, name: 'Zona 3', Ao: '0.40g', color: '#ef4444',
      cities: 'Antofagasta, Valparaíso, Concepción, Arica',
      desc: 'Sismicidad alta. Costa y norte grande. Subducción directa.',
      soils: { A: { S: 0.90, T0: 0.15, Tp: 0.20, n: 1.00 }, B: { S: 1.00, T0: 0.30, Tp: 0.35, n: 1.33 }, C: { S: 1.05, T0: 0.40, Tp: 0.45, n: 1.40 }, D: { S: 1.20, T0: 0.75, Tp: 0.85, n: 1.80 }, E: { S: 1.30, T0: 1.20, Tp: 1.35, n: 1.80 } }
    }
  ];

  // Render zone buttons
  let html = '<div class="zone-map-grid">';
  zones.forEach(z => {
    html += `<button class="zone-map-btn" data-zone="${z.id}" style="--zone-color: ${z.color}">
      <span class="zone-map-num" style="background: ${z.color}">${z.id}</span>
      <span class="zone-map-label">${z.name}</span>
      <span class="zone-map-ao">A<sub>0</sub> = ${z.Ao}</span>
    </button>`;
  });
  html += '</div>';
  mapContainer.innerHTML = html;

  // Click handlers
  mapContainer.querySelectorAll('.zone-map-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      mapContainer.querySelectorAll('.zone-map-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const z = zones.find(zz => zz.id === parseInt(btn.dataset.zone));
      if (z && infoPanel) showZoneInfo(z, infoPanel);
    });
  });

  function showZoneInfo(z, panel) {
    let soilRows = '';
    Object.entries(z.soils).forEach(([name, s]) => {
      soilRows += `<tr><td><strong>${name}</strong></td><td>${s.S}</td><td>${s.T0}</td><td>${s.Tp}</td><td>${s.n}</td></tr>`;
    });
    panel.innerHTML = `
      <h4 style="color: ${z.color}">${z.name} — A<sub>0</sub> = ${z.Ao}</h4>
      <p>${z.desc}</p>
      <p><strong>Ciudades:</strong> ${z.cities}</p>
      <h5>Parámetros de Suelo (DS61)</h5>
      <table class="data-table data-table-striped">
        <thead><tr><th>Suelo</th><th>S</th><th>T<sub>0</sub>(s)</th><th>T'(s)</th><th>n</th></tr></thead>
        <tbody>${soilRows}</tbody>
      </table>
      <div class="key-point" style="margin-top:0.5rem">
        <span>&#128204;</span> Antofagasta = Zona 3, suelo típico B-C. Diseño con A<sub>0</sub>=0.4g.
      </div>`;
  }
}
