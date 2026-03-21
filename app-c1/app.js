/* ============================================================
   ADSE Control 1 — App Principal
   Análisis y Diseño Sísmico de Edificios — UCN 1S-2026
   ============================================================ */

'use strict';

// ============================================================
// 1. STATE & CONSTANTS
// ============================================================
const APP = {
  currentModule: 'dashboard',
  charts: {},
  threeScenes: {},
  progress: JSON.parse(localStorage.getItem('adse-c1-progress') || '{}'),
  quizState: null,
  modulesVisited: new Set(JSON.parse(localStorage.getItem('adse-c1-visited') || '[]')),
  testHistory: JSON.parse(localStorage.getItem('adse-c1-tests') || '[]'),
};

const MODULES = ['dashboard','mod1','mod2','mod3','mod4','mod5','mod6','mod7','mod8','mod9'];

function saveProgress() {
  localStorage.setItem('adse-c1-progress', JSON.stringify(APP.progress));
  localStorage.setItem('adse-c1-visited', JSON.stringify([...APP.modulesVisited]));
  localStorage.setItem('adse-c1-tests', JSON.stringify(APP.testHistory));
}

// ============================================================
// 2. NAVIGATION
// ============================================================
function navigateTo(moduleId) {
  if (!MODULES.includes(moduleId)) return;
  document.querySelectorAll('.module-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const section = document.getElementById('section-' + moduleId);
  const navBtn = document.querySelector(`.nav-item[data-module="${moduleId}"]`);
  if (section) { section.classList.add('active'); section.scrollTop = 0; }
  if (navBtn) navBtn.classList.add('active');
  APP.currentModule = moduleId;
  APP.modulesVisited.add(moduleId);
  saveProgress();
  updateDashboard();
  // Init module-specific features on first visit
  initModuleIfNeeded(moduleId);
  // Hook for new modules/calculators (modules.js, calculators.js)
  if (typeof initNewFeatures === 'function') initNewFeatures(moduleId);
  // Scroll main to top
  const main = document.getElementById('main-content');
  if (main) main.scrollTop = 0;
  // Re-typeset MathJax
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise([section]).catch(() => {});
  }
}

function initNavigation() {
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => navigateTo(btn.dataset.module));
  });
  document.querySelectorAll('[data-goto]').forEach(btn => {
    btn.addEventListener('click', () => navigateTo(btn.dataset.goto));
  });
  // Sidebar toggle
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => {
      // Mobile: toggle 'open' class (sidebar is off-screen by default)
      if (window.innerWidth <= 768) {
        sidebar.classList.toggle('open');
      } else {
        sidebar.classList.toggle('collapsed');
      }
    });
  }
  // Close sidebar on mobile when navigating
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      if (window.innerWidth <= 768 && sidebar) sidebar.classList.remove('open');
    });
  });
}

// ============================================================
// 3. THEME
// ============================================================
function initTheme() {
  const saved = localStorage.getItem('adse-c1-theme') || 'dark';
  document.body.dataset.theme = saved;
  if (saved === 'light') document.body.classList.add('light-theme');
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', () => {
      const isDark = document.body.dataset.theme === 'dark';
      document.body.dataset.theme = isDark ? 'light' : 'dark';
      document.body.classList.toggle('light-theme', isDark);
      localStorage.setItem('adse-c1-theme', isDark ? 'light' : 'dark');
    });
  }
}

// ============================================================
// 4. TOAST NOTIFICATIONS
// ============================================================
function showToast(message, type = 'info', duration = 3000) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type} animate-fadeIn`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => { toast.classList.add('animate-fadeOut'); setTimeout(() => toast.remove(), 400); }, duration);
}

// ============================================================
// 5. DASHBOARD
// ============================================================
function updateDashboard() {
  const visited = APP.modulesVisited.size;
  const total = MODULES.length - 1; // exclude dashboard
  const pct = Math.round(((visited - (APP.modulesVisited.has('dashboard') ? 1 : 0)) / total) * 100);
  const el = document.getElementById('dashboard-progress-pct');
  if (el) el.textContent = pct + '%';
  const fill = document.getElementById('global-progress-fill');
  if (fill) fill.style.width = pct + '%';
  const lbl = document.getElementById('global-progress-label');
  if (lbl) lbl.textContent = pct + '%';
  // Stats
  const totalQ = APP.testHistory.reduce((s, t) => s + t.total, 0);
  const correctQ = APP.testHistory.reduce((s, t) => s + t.correct, 0);
  const acc = totalQ > 0 ? Math.round((correctQ / totalQ) * 100) : 0;
  const qEl = document.getElementById('dash-total-questions');
  if (qEl) qEl.textContent = totalQ;
  const aEl = document.getElementById('dash-accuracy');
  if (aEl) aEl.textContent = totalQ > 0 ? acc + '%' : '--';
  const sc = document.getElementById('stat-score');
  if (sc) sc.textContent = totalQ > 0 ? acc + '%' : '--';
  const comp = document.getElementById('stat-completed');
  if (comp) comp.textContent = APP.testHistory.length;
  // Progress ring
  drawProgressRing('dashboard-progress-ring', pct / 100);
}

function drawProgressRing(canvasId, pct) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  const cx = w / 2, cy = h / 2, r = Math.min(w, h) / 2 - 15;
  ctx.clearRect(0, 0, w, h);
  // Background ring
  ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(255,255,255,0.1)'; ctx.lineWidth = 12; ctx.stroke();
  // Progress ring
  ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * pct);
  const grad = ctx.createLinearGradient(0, 0, w, h);
  grad.addColorStop(0, '#00d4ff'); grad.addColorStop(1, '#a855f7');
  ctx.strokeStyle = grad; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.stroke();
}

// ============================================================
// 6. MODULE INITIALIZERS
// ============================================================
const moduleInited = new Set();

function initModuleIfNeeded(id) {
  if (moduleInited.has(id)) return;
  moduleInited.add(id);
  switch (id) {
    case 'mod2': initMod2Charts(); break;
    case 'mod3': initMod3Charts(); break;
    case 'mod4': initMod4Interactive(); break;
    case 'mod5': initMod5Matrix(); break;
    case 'mod6': initMod6Buildings(); break;
    case 'mod7': initMod7Spectrum(); break;
    // mod8: handled by initMod8Enhanced in modules.js via initNewFeatures
    case 'mod9': initTestSystem(); break;
    case 'dashboard': initDashboardChart(); break;
  }
}

// ============================================================
// 7. MODULE 2 — Force-Deformation Chart
// ============================================================
function initMod2Charts() {
  const canvas = document.getElementById('mod2-force-deformation-chart');
  if (!canvas) return;
  // Generate data for elastic, ductile, brittle
  const elastic = [], ductile = [], brittle = [];
  for (let d = 0; d <= 50; d += 0.5) {
    elastic.push({ x: d, y: d * 2 }); // k=2
    if (d <= 15) ductile.push({ x: d, y: d * 2 });
    else if (d <= 45) ductile.push({ x: d, y: 30 + (d - 15) * 0.1 });
    else ductile.push({ x: d, y: 33 - (d - 45) * 2 });
    if (d <= 12) brittle.push({ x: d, y: d * 3 });
    else if (d <= 15) brittle.push({ x: d, y: 36 - (d - 12) * 12 });
    else brittle.push({ x: d, y: 0 });
  }

  APP.charts.mod2FD = new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: [
        { label: 'Elástico lineal', data: elastic, borderColor: '#00d4ff', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: 'Dúctil (HA confinado)', data: ductile, borderColor: '#22c55e', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: 'Frágil (sin confinar)', data: brittle, borderColor: '#ef4444', showLine: true, pointRadius: 0, borderWidth: 2 },
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Curvas Fuerza-Deformación', color: '#e0e0e0' },
        legend: { labels: { color: '#ccc' } }
      },
      scales: {
        x: { title: { display: true, text: 'Deformación δ (mm)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } },
        y: { title: { display: true, text: 'Fuerza F (kN)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0 }
      }
    }
  });
  // Checkbox toggles
  ['elastic', 'ductile', 'brittle'].forEach((key, i) => {
    const cb = document.getElementById(`mod2-show-${key}`);
    if (cb) cb.addEventListener('change', () => {
      APP.charts.mod2FD.data.datasets[i].hidden = !cb.checked;
      APP.charts.mod2FD.update();
    });
  });
}

// ============================================================
// 8. MODULE 3 — Spectrum + Isolation
// ============================================================
function initMod3Charts() {
  const canvas = document.getElementById('mod3-spectrum-chart');
  if (!canvas) return;
  function generateSpectrum(damping) {
    const xi = damping / 100;
    const factor = Math.sqrt(0.05 / xi);
    const points = [];
    for (let T = 0.01; T <= 4; T += 0.02) {
      let Sa;
      if (T <= 0.15) Sa = 0.4 * (1 + (2.5 * factor - 1) * T / 0.15);
      else if (T <= 0.6) Sa = 0.4 * 2.5 * factor;
      else Sa = 0.4 * 2.5 * factor * (0.6 / T);
      points.push({ x: T, y: Sa });
    }
    return points;
  }
  function generateIsolated() {
    const points = [];
    for (let T = 0.01; T <= 4; T += 0.02) {
      let Sa;
      if (T <= 0.15) Sa = 0.4 * (1 + 1.5 * T / 0.15);
      else if (T <= 0.6) Sa = 0.4 * 1.5;
      else Sa = 0.4 * 1.5 * (0.6 / T);
      points.push({ x: T, y: Sa });
    }
    return points;
  }
  APP.charts.mod3Spec = new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: [
        { label: 'Espectro ξ=5%', data: generateSpectrum(5), borderColor: '#00d4ff', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: 'Espectro con aislación', data: generateIsolated(), borderColor: '#a855f7', showLine: true, pointRadius: 0, borderWidth: 2, hidden: true }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Espectro de Diseño NCh433', color: '#e0e0e0' },
        legend: { labels: { color: '#ccc' } }
      },
      scales: {
        x: { title: { display: true, text: 'Período T (s)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0, max: 4 },
        y: { title: { display: true, text: 'Sa (g)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0 }
      }
    }
  });
  // Damping slider
  const slider = document.getElementById('mod3-damping-slider');
  const valEl = document.getElementById('mod3-damping-value');
  if (slider) slider.addEventListener('input', () => {
    const v = parseInt(slider.value);
    if (valEl) valEl.textContent = v + '%';
    APP.charts.mod3Spec.data.datasets[0].data = generateSpectrum(v);
    APP.charts.mod3Spec.data.datasets[0].label = `Espectro ξ=${v}%`;
    APP.charts.mod3Spec.update();
  });
  // Show isolated
  const isoCheck = document.getElementById('mod3-show-isolated');
  if (isoCheck) isoCheck.addEventListener('change', () => {
    APP.charts.mod3Spec.data.datasets[1].hidden = !isoCheck.checked;
    APP.charts.mod3Spec.update();
  });
  // 3D Isolation simulation
  initIsolation3D();
}

// ============================================================
// 9. MODULE 3 — 3D Isolation Simulation
// ============================================================
function initIsolation3D() {
  const canvas = document.getElementById('mod3-isolation-3d');
  if (!canvas || !window.THREE) return;
  const w = canvas.parentElement.clientWidth || 500;
  const h = 350;
  canvas.width = w; canvas.height = h;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a1a);
  const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
  camera.position.set(8, 6, 8);
  camera.lookAt(0, 2, 0);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(w, h);
  // Lights
  scene.add(new THREE.AmbientLight(0x404040, 0.8));
  const dirLight = new THREE.DirectionalLight(0xffffff, 1);
  dirLight.position.set(5, 10, 5); scene.add(dirLight);
  // Ground
  const ground = new THREE.Mesh(new THREE.BoxGeometry(16, 0.3, 8), new THREE.MeshPhongMaterial({ color: 0x333333 }));
  ground.position.y = -0.15; scene.add(ground);
  // Conventional building (left)
  const convGroup = new THREE.Group();
  const convMat = new THREE.MeshPhongMaterial({ color: 0x00d4ff, transparent: true, opacity: 0.7 });
  for (let i = 0; i < 5; i++) {
    const floor = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.15, 2), convMat);
    floor.position.set(-3, i * 0.8 + 0.4, 0);
    convGroup.add(floor);
    if (i < 4) {
      [[-1, 0, -0.8], [1, 0, -0.8], [-1, 0, 0.8], [1, 0, 0.8]].forEach(p => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.65, 0.15), new THREE.MeshPhongMaterial({ color: 0x666666 }));
        col.position.set(p[0] - 3, i * 0.8 + 0.75, p[2]);
        convGroup.add(col);
      });
    }
  }
  scene.add(convGroup);
  // Label
  const convLabel = createTextSprite('CONVENCIONAL');
  convLabel.position.set(-3, 4.5, 0); scene.add(convLabel);
  // Isolated building (right)
  const isoGroup = new THREE.Group();
  const isoMat = new THREE.MeshPhongMaterial({ color: 0xa855f7, transparent: true, opacity: 0.7 });
  // Isolators
  const isoBaseMat = new THREE.MeshPhongMaterial({ color: 0xff6b35 });
  [[-1, 0, -0.8], [1, 0, -0.8], [-1, 0, 0.8], [1, 0, 0.8]].forEach(p => {
    const iso = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.25, 16), isoBaseMat);
    iso.position.set(p[0] + 3, 0.12, p[2]);
    isoGroup.add(iso);
  });
  for (let i = 0; i < 5; i++) {
    const floor = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.15, 2), isoMat);
    floor.position.set(3, i * 0.8 + 0.65, 0);
    isoGroup.add(floor);
    if (i < 4) {
      [[-1, 0, -0.8], [1, 0, -0.8], [-1, 0, 0.8], [1, 0, 0.8]].forEach(p => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.65, 0.15), new THREE.MeshPhongMaterial({ color: 0x666666 }));
        col.position.set(p[0] + 3, i * 0.8 + 1.0, p[2]);
        isoGroup.add(col);
      });
    }
  }
  scene.add(isoGroup);
  const isoLabel = createTextSprite('AISLADO');
  isoLabel.position.set(3, 4.8, 0); scene.add(isoLabel);

  APP.threeScenes.isolation = { scene, camera, renderer, convGroup, isoGroup, ground, animating: false, time: 0 };
  renderer.render(scene, camera);

  // Play button
  const playBtn = document.getElementById('mod3-play-seismic');
  const resetBtn = document.getElementById('mod3-reset-seismic');
  if (playBtn) playBtn.addEventListener('click', () => startIsolationAnim());
  if (resetBtn) resetBtn.addEventListener('click', () => resetIsolationAnim());
}

function startIsolationAnim() {
  const s = APP.threeScenes.isolation;
  if (!s || s.animating) return;
  s.animating = true; s.time = 0;
  function animate() {
    if (!s.animating) return;
    s.time += 0.05;
    if (s.time > 12) { s.animating = false; return; }
    const quake = Math.sin(s.time * 3) * Math.exp(-s.time * 0.15) * 0.3;
    s.ground.position.x = quake;
    // Conventional: each floor amplifies
    s.convGroup.children.forEach((child, i) => {
      const floorIdx = Math.floor(i / 5);
      const amp = 1 + floorIdx * 0.4;
      child.position.x += (quake * amp - (child.position.x - child.userData.origX || 0)) * 0.1;
      if (!child.userData.origX) child.userData.origX = child.position.x;
      child.position.x = (child.userData.origX || child.position.x) + quake * amp;
    });
    // Isolated: moves as rigid body with small displacement
    s.isoGroup.children.forEach(child => {
      if (!child.userData.origX) child.userData.origX = child.position.x;
      child.position.x = child.userData.origX + quake * 0.15;
    });
    s.renderer.render(s.scene, s.camera);
    requestAnimationFrame(animate);
  }
  // Store original positions
  s.convGroup.children.forEach(c => { c.userData.origX = c.position.x; });
  s.isoGroup.children.forEach(c => { c.userData.origX = c.position.x; });
  animate();
}

function resetIsolationAnim() {
  const s = APP.threeScenes.isolation;
  if (!s) return;
  s.animating = false;
  s.convGroup.children.forEach(c => { if (c.userData.origX !== undefined) c.position.x = c.userData.origX; });
  s.isoGroup.children.forEach(c => { if (c.userData.origX !== undefined) c.position.x = c.userData.origX; });
  s.ground.position.x = 0;
  s.renderer.render(s.scene, s.camera);
}

function createTextSprite(text) {
  const canvas = document.createElement('canvas');
  canvas.width = 256; canvas.height = 64;
  const ctx = canvas.getContext('2d');
  ctx.font = 'bold 24px Inter, sans-serif';
  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'center';
  ctx.fillText(text, 128, 40);
  const texture = new THREE.CanvasTexture(canvas);
  const mat = new THREE.SpriteMaterial({ map: texture });
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(3, 0.75, 1);
  return sprite;
}

// ============================================================
// 10. MODULE 4 — CM/CR Interactive
// ============================================================
function initMod4Interactive() {
  const canvas = document.getElementById('mod4-cmcr-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = 600, H = 400;
  canvas.width = W; canvas.height = H;
  // Building floor plan with walls
  const walls = [
    { x: 50, y: 50, w: 10, h: 120, kx: 0, ky: 500 },
    { x: 540, y: 50, w: 10, h: 120, kx: 0, ky: 300 },
    { x: 150, y: 50, w: 150, h: 10, kx: 600, ky: 0 },
    { x: 150, y: 330, w: 200, h: 10, kx: 800, ky: 0 },
    { x: 300, y: 100, w: 10, h: 80, kx: 0, ky: 400 },
  ];
  let dragIdx = -1;

  function draw() {
    ctx.clearRect(0, 0, W, H);
    // Floor plan outline
    ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1;
    ctx.strokeRect(30, 30, W - 60, H - 60);
    ctx.fillStyle = 'rgba(255,255,255,0.02)';
    ctx.fillRect(30, 30, W - 60, H - 60);
    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    for (let x = 30; x <= W - 30; x += 30) { ctx.beginPath(); ctx.moveTo(x, 30); ctx.lineTo(x, H - 30); ctx.stroke(); }
    for (let y = 30; y <= H - 30; y += 30) { ctx.beginPath(); ctx.moveTo(30, y); ctx.lineTo(W - 30, y); ctx.stroke(); }
    // Walls
    walls.forEach((wall, i) => {
      ctx.fillStyle = dragIdx === i ? '#ff6b35' : '#00d4ff';
      ctx.globalAlpha = 0.7;
      ctx.fillRect(wall.x, wall.y, wall.w, wall.h);
      ctx.globalAlpha = 1;
      ctx.strokeStyle = '#00d4ff'; ctx.lineWidth = 1;
      ctx.strokeRect(wall.x, wall.y, wall.w, wall.h);
    });
    // Calculate CM (assume uniform mass distribution — center of floor)
    const cmX = W / 2, cmY = H / 2;
    // Calculate CR (weighted by stiffness)
    let sumKy = 0, sumKx = 0, sumKyX = 0, sumKxY = 0;
    walls.forEach(w => {
      const cx = w.x + w.w / 2, cy = w.y + w.h / 2;
      sumKy += w.ky; sumKx += w.kx;
      sumKyX += w.ky * cx; sumKxY += w.kx * cy;
    });
    const crX = sumKy > 0 ? sumKyX / sumKy : cmX;
    const crY = sumKx > 0 ? sumKxY / sumKx : cmY;
    // Draw CM
    ctx.beginPath(); ctx.arc(cmX, cmY, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#22c55e'; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Inter'; ctx.fillText('CM', cmX + 12, cmY + 4);
    // Draw CR
    ctx.beginPath(); ctx.arc(crX, crY, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#ef4444'; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.fillText('CR', crX + 12, crY + 4);
    // Eccentricity line
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(cmX, cmY); ctx.lineTo(crX, crY); ctx.stroke();
    ctx.setLineDash([]);
    const ex = Math.abs(crX - cmX).toFixed(0);
    const ey = Math.abs(crY - cmY).toFixed(0);
    ctx.fillStyle = '#ff6b35'; ctx.font = '11px Inter';
    ctx.fillText(`e = (${ex}, ${ey})`, (cmX + crX) / 2, (cmY + crY) / 2 - 10);
    // Update info panel
    const cmEl = document.getElementById('mod4-cm-pos');
    const crEl = document.getElementById('mod4-cr-pos');
    const eccEl = document.getElementById('mod4-ecc-value');
    const torEl = document.getElementById('mod4-torsion-value');
    if (cmEl) cmEl.textContent = `(${cmX.toFixed(0)}, ${cmY.toFixed(0)})`;
    if (crEl) crEl.textContent = `(${crX.toFixed(0)}, ${crY.toFixed(0)})`;
    const ecc = Math.sqrt((crX - cmX) ** 2 + (crY - cmY) ** 2).toFixed(1);
    if (eccEl) eccEl.textContent = ecc + ' px';
    if (torEl) torEl.textContent = ecc > 30 ? 'SIGNIFICATIVA' : ecc > 10 ? 'Moderada' : 'Baja';
  }

  // Drag walls
  canvas.addEventListener('mousedown', e => {
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const my = (e.clientY - rect.top) * (H / rect.height);
    walls.forEach((w, i) => {
      if (mx >= w.x && mx <= w.x + w.w && my >= w.y && my <= w.y + w.h) dragIdx = i;
    });
  });
  canvas.addEventListener('mousemove', e => {
    if (dragIdx < 0) return;
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const my = (e.clientY - rect.top) * (H / rect.height);
    walls[dragIdx].x = mx - walls[dragIdx].w / 2;
    walls[dragIdx].y = my - walls[dragIdx].h / 2;
    draw();
  });
  canvas.addEventListener('mouseup', () => { dragIdx = -1; });
  canvas.addEventListener('mouseleave', () => { dragIdx = -1; });
  draw();
}

// ============================================================
// 11. MODULE 5 — Matrix Builder
// ============================================================
function initMod5Matrix() {
  const buildBtn = document.getElementById('mod5-build-matrix');
  if (!buildBtn) return;
  buildBtn.addEventListener('click', () => {
    const n = parseInt(document.getElementById('mod5-num-floors')?.value || '3');
    if (n < 1 || n > 10) return;
    buildStiffnessMatrix(n);
  });
  buildStiffnessMatrix(3);
}

function buildStiffnessMatrix(n) {
  const result = document.getElementById('mod5-matrix-result');
  if (!result) return;
  // Create tridiagonal stiffness matrix for shear building
  const k = Array.from({ length: n }, () => Array(n).fill(0));
  const stiffnesses = Array.from({ length: n }, (_, i) => Math.round(1000 * (n - i) / n));
  for (let i = 0; i < n; i++) {
    if (i === 0) {
      k[0][0] = stiffnesses[0] + (n > 1 ? stiffnesses[1] : 0);
      if (n > 1) k[0][1] = -stiffnesses[1];
    } else if (i === n - 1) {
      k[i][i] = stiffnesses[i];
      k[i][i - 1] = -stiffnesses[i];
    } else {
      k[i][i] = stiffnesses[i] + stiffnesses[i + 1];
      k[i][i - 1] = -stiffnesses[i];
      k[i][i + 1] = -stiffnesses[i + 1];
    }
  }
  let html = '<h4>Matriz de Rigidez Lateral (kN/m)</h4>';
  html += '<div class="matrix-display"><table class="matrix-table">';
  for (let i = 0; i < n; i++) {
    html += '<tr>';
    for (let j = 0; j < n; j++) {
      const val = k[i][j];
      const cls = val === 0 ? 'zero' : (i === j ? 'diagonal' : 'off-diagonal');
      html += `<td class="${cls}">${val}</td>`;
    }
    html += '</tr>';
  }
  html += '</table></div>';
  html += `<div class="matrix-info"><p><strong>Rigideces por piso:</strong> ${stiffnesses.map((s, i) => `k${i + 1}=${s}`).join(', ')} kN/m</p>`;
  html += `<p><strong>Tamaño:</strong> ${n}×${n} (${n} pisos, diafragma rígido simétrico → solo traslación)</p>`;
  html += `<p><strong>Estructura:</strong> Tridiagonal (cada piso interactúa solo con pisos adyacentes)</p></div>`;
  result.innerHTML = html;
}

// ============================================================
// 12. MODULE 6 — Building Classification 3D
// ============================================================
function initMod6Buildings() {
  const canvas = document.getElementById('mod6-building-3d');
  if (!canvas || !window.THREE) return;
  const w = canvas.parentElement?.clientWidth || 500;
  const h = 400;
  canvas.width = w; canvas.height = h;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a1a);
  const camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 1000);
  camera.position.set(6, 5, 6); camera.lookAt(0, 2, 0);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(w, h);
  scene.add(new THREE.AmbientLight(0x404040, 0.6));
  const dl = new THREE.DirectionalLight(0xffffff, 1); dl.position.set(5, 10, 5); scene.add(dl);
  // Ground
  const gnd = new THREE.Mesh(new THREE.BoxGeometry(10, 0.1, 6), new THREE.MeshPhongMaterial({ color: 0x222222 }));
  scene.add(gnd);

  APP.threeScenes.building = { scene, camera, renderer, currentGroup: null };
  showBuildingType(1);

  // Type buttons
  document.querySelectorAll('#section-mod6 .type-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#section-mod6 .type-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      showBuildingType(parseInt(btn.dataset.type));
    });
  });
  // Slow rotation
  function rotateBuilding() {
    const s = APP.threeScenes.building;
    if (s && s.currentGroup) {
      s.currentGroup.rotation.y += 0.005;
      s.renderer.render(s.scene, s.camera);
    }
    requestAnimationFrame(rotateBuilding);
  }
  rotateBuilding();
}

function showBuildingType(type) {
  const s = APP.threeScenes.building;
  if (!s) return;
  if (s.currentGroup) s.scene.remove(s.currentGroup);
  const group = new THREE.Group();
  const colors = { frame: 0x00d4ff, wall: 0xa855f7, slab: 0x333344, coupling: 0xff6b35, tube: 0x22c55e };
  const floors = [5, 8, 8, 12, 16][type - 1];
  const fh = 0.3;
  const info = document.getElementById('mod6-type-info');
  const typeNames = ['Marcos Rígidos', 'Muros Simples', 'Muros Acoplados', 'Marcos + Muros (Dual)', 'Tubo'];
  const maxFloors = ['20-22', '30-35', '30-35', '45-50', '50-65'];
  const descriptions = [
    'Resistencia lateral por flexión de vigas y columnas rígidamente conectadas.',
    'Muros de hormigón armado aislados. Sistema dominante en Chile.',
    'Muros conectados por vigas de acoplamiento que disipan energía.',
    'Combinación de marcos y muros. Mayor eficiencia estructural.',
    'Perímetro del edificio actúa como tubo rígido. Para rascacielos.'
  ];

  for (let i = 0; i < floors; i++) {
    const y = i * fh + 0.2;
    // Slab
    const slab = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.05, 2), new THREE.MeshPhongMaterial({ color: colors.slab, transparent: true, opacity: 0.5 }));
    slab.position.y = y; group.add(slab);

    if (type === 1) { // Marcos
      [[-1, -0.8], [0, -0.8], [1, -0.8], [-1, 0.8], [0, 0.8], [1, 0.8]].forEach(p => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.1, fh - 0.05, 0.1), new THREE.MeshPhongMaterial({ color: colors.frame }));
        col.position.set(p[0], y + fh / 2, p[1]); group.add(col);
      });
    } else if (type === 2) { // Muros simples
      [[-1.2, 0], [1.2, 0]].forEach(p => {
        const wall = new THREE.Mesh(new THREE.BoxGeometry(0.08, fh - 0.05, 1.6), new THREE.MeshPhongMaterial({ color: colors.wall }));
        wall.position.set(p[0], y + fh / 2, p[1]); group.add(wall);
      });
      const wallX = new THREE.Mesh(new THREE.BoxGeometry(1.5, fh - 0.05, 0.08), new THREE.MeshPhongMaterial({ color: colors.wall }));
      wallX.position.set(0, y + fh / 2, -0.9); group.add(wallX);
    } else if (type === 3) { // Muros acoplados
      [[-0.7, 0], [0.7, 0]].forEach(p => {
        const wall = new THREE.Mesh(new THREE.BoxGeometry(0.08, fh - 0.05, 1.4), new THREE.MeshPhongMaterial({ color: colors.wall }));
        wall.position.set(p[0], y + fh / 2, p[1]); group.add(wall);
      });
      // Coupling beams
      const beam = new THREE.Mesh(new THREE.BoxGeometry(1.32, 0.08, 0.15), new THREE.MeshPhongMaterial({ color: colors.coupling }));
      beam.position.set(0, y + fh * 0.8, 0); group.add(beam);
    } else if (type === 4) { // Dual
      [[-1, -0.8], [1, -0.8], [-1, 0.8], [1, 0.8]].forEach(p => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.1, fh - 0.05, 0.1), new THREE.MeshPhongMaterial({ color: colors.frame }));
        col.position.set(p[0], y + fh / 2, p[1]); group.add(col);
      });
      const wallC = new THREE.Mesh(new THREE.BoxGeometry(0.08, fh - 0.05, 1.5), new THREE.MeshPhongMaterial({ color: colors.wall }));
      wallC.position.set(0, y + fh / 2, 0); group.add(wallC);
    } else if (type === 5) { // Tubo
      // Perimeter columns close together
      for (let j = -1.2; j <= 1.2; j += 0.3) {
        const c1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, fh - 0.05, 0.06), new THREE.MeshPhongMaterial({ color: colors.tube }));
        c1.position.set(j, y + fh / 2, -0.95); group.add(c1);
        const c2 = c1.clone(); c2.position.z = 0.95; group.add(c2);
      }
      for (let j = -0.8; j <= 0.8; j += 0.3) {
        const c3 = new THREE.Mesh(new THREE.BoxGeometry(0.06, fh - 0.05, 0.06), new THREE.MeshPhongMaterial({ color: colors.tube }));
        c3.position.set(-1.2, y + fh / 2, j); group.add(c3);
        const c4 = c3.clone(); c4.position.x = 1.2; group.add(c4);
      }
    }
  }
  group.position.y = 0.1;
  s.scene.add(group);
  s.currentGroup = group;
  s.renderer.render(s.scene, s.camera);

  if (info) {
    info.innerHTML = `<h4>Tipo ${type}: ${typeNames[type - 1]}</h4>
    <p>${descriptions[type - 1]}</p>
    <p><strong>Altura máxima:</strong> ${maxFloors[type - 1]} pisos</p>
    <p><strong>Pisos mostrados:</strong> ${floors}</p>`;
  }
}

// ============================================================
// 13. MODULE 7 — NCh433 Spectrum Generator
// ============================================================
function initMod7Spectrum() {
  const canvas = document.getElementById('mod7-spectrum-chart');
  if (!canvas) return;
  // Zone/Soil parameters from DS61
  const zones = { '1': 0.2, '2': 0.3, '3': 0.4 };
  const soilParams = {
    'A': { S: 0.90, Tp: 0.15, n: 1.00 },
    'B': { S: 1.00, Tp: 0.30, n: 1.33 },
    'C': { S: 1.05, Tp: 0.40, n: 1.40 },
    'D': { S: 1.20, Tp: 0.75, n: 1.80 },
    'E': { S: 1.30, Tp: 1.20, n: 2.00 },
  };

  function calcSpectrum(zone, soil, Ro) {
    const Ao = zones[zone] || 0.4;
    const params = soilParams[soil] || soilParams['C'];
    const { S, Tp, n } = params;
    const g = 9.81;
    const points = [];
    for (let T = 0.01; T <= 4; T += 0.02) {
      const alpha = (1 + 4.5 * (Tp / T)) / (1 + (Tp / T) ** 3);
      const Rstar = 1 + (Ro - 1) * (T / (0.1 * Ro + T));
      const Sa = (S * Ao * alpha) / Rstar;
      points.push({ x: T, y: Sa });
    }
    return points;
  }

  APP.charts.mod7Spec = new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: [
        { label: 'Sa diseño (g)', data: calcSpectrum('3', 'C', 7), borderColor: '#00d4ff', showLine: true, pointRadius: 0, borderWidth: 2, fill: true, backgroundColor: 'rgba(0,212,255,0.1)' }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Espectro de Diseño NCh433 + DS61', color: '#e0e0e0' },
        legend: { labels: { color: '#ccc' } }
      },
      scales: {
        x: { title: { display: true, text: 'Período T (s)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0, max: 4 },
        y: { title: { display: true, text: 'Sa (g)', color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' }, min: 0 }
      }
    }
  });

  // Listen for controls (they might be selects in the HTML)
  document.querySelectorAll('#section-mod7 select').forEach(sel => {
    sel.addEventListener('change', () => updateMod7Spectrum());
  });
}

function updateMod7Spectrum() {
  const zone = document.querySelector('#section-mod7 select[name="zone"]')?.value || '3';
  const soil = document.querySelector('#section-mod7 select[name="soil"]')?.value || 'C';
  const Ro = parseFloat(document.querySelector('#section-mod7 select[name="Ro"]')?.value || '7');
  const zones = { '1': 0.2, '2': 0.3, '3': 0.4 };
  const soilParams = {
    'A': { S: 0.90, Tp: 0.15, n: 1.00 },
    'B': { S: 1.00, Tp: 0.30, n: 1.33 },
    'C': { S: 1.05, Tp: 0.40, n: 1.40 },
    'D': { S: 1.20, Tp: 0.75, n: 1.80 },
    'E': { S: 1.30, Tp: 1.20, n: 2.00 },
  };
  const Ao = zones[zone] || 0.4;
  const params = soilParams[soil] || soilParams['C'];
  const points = [];
  for (let T = 0.01; T <= 4; T += 0.02) {
    const alpha = (1 + 4.5 * (params.Tp / T)) / (1 + (params.Tp / T) ** 3);
    const Rstar = 1 + (Ro - 1) * (T / (0.1 * Ro + T));
    const Sa = (params.S * Ao * alpha) / Rstar;
    points.push({ x: T, y: Sa });
  }
  if (APP.charts.mod7Spec) {
    APP.charts.mod7Spec.data.datasets[0].data = points;
    APP.charts.mod7Spec.data.datasets[0].label = `Z${zone} Suelo ${soil} Ro=${Ro}`;
    APP.charts.mod7Spec.update();
  }
}

// ============================================================
// 14. MODULE 8 — Mode Shape Visualization
// ============================================================
function initMod8Modes() {
  const canvas = document.getElementById('mod8-modes-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.parentElement?.clientWidth || 600;
  const H = 400;
  canvas.width = W; canvas.height = H;
  let currentMode = 1;

  // Mode shapes for a 5-story shear building (approximate)
  const modeShapes = {
    1: [0.2, 0.4, 0.6, 0.8, 1.0],
    2: [0.5, 0.8, 0.5, -0.3, -1.0],
    3: [0.8, 0.3, -0.8, -0.3, 0.8],
  };

  function drawMode(mode) {
    ctx.clearRect(0, 0, W, H);
    const shape = modeShapes[mode] || modeShapes[1];
    const n = shape.length;
    const baseX = W / 2, baseY = H - 40;
    const floorH = (H - 80) / n;
    const maxDisp = 80;

    // Title
    ctx.fillStyle = '#e0e0e0'; ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'center';
    ctx.fillText(`Modo ${mode} de vibración — Edificio 5 pisos`, W / 2, 25);

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
      const x = baseX + shape[i] * maxDisp;
      const y = baseY - (i + 1) * floorH;
      ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Floor markers and labels
    for (let i = 0; i < n; i++) {
      const x = baseX + shape[i] * maxDisp;
      const y = baseY - (i + 1) * floorH;
      // Floor line
      ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(baseX - maxDisp - 20, y); ctx.lineTo(baseX + maxDisp + 20, y); ctx.stroke();
      // Node
      ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fillStyle = '#00d4ff'; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
      // Label
      ctx.fillStyle = '#aaa'; ctx.font = '11px Inter'; ctx.textAlign = 'right';
      ctx.fillText(`Piso ${i + 1}`, baseX - maxDisp - 25, y + 4);
      ctx.textAlign = 'left';
      ctx.fillText(`φ = ${shape[i].toFixed(2)}`, baseX + maxDisp + 25, y + 4);
    }

    // Ground
    ctx.fillStyle = '#444'; ctx.fillRect(baseX - maxDisp - 20, baseY, maxDisp * 2 + 40, 3);
    // Hatching
    for (let i = 0; i < 15; i++) {
      const sx = baseX - maxDisp - 20 + i * 12;
      ctx.strokeStyle = '#555'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(sx, baseY + 3); ctx.lineTo(sx - 8, baseY + 12); ctx.stroke();
    }
  }

  drawMode(1);

  // Mode selector buttons (create dynamically)
  const container = canvas.parentElement;
  if (container) {
    const btnRow = document.createElement('div');
    btnRow.className = 'flex gap-sm justify-center mt-md';
    [1, 2, 3].forEach(m => {
      const btn = document.createElement('button');
      btn.className = `btn ${m === 1 ? 'btn-primary' : 'btn-secondary'}`;
      btn.textContent = `Modo ${m}`;
      btn.addEventListener('click', () => {
        currentMode = m;
        drawMode(m);
        btnRow.querySelectorAll('.btn').forEach(b => b.className = 'btn btn-secondary');
        btn.className = 'btn btn-primary';
      });
      btnRow.appendChild(btn);
    });
    container.appendChild(btnRow);
  }
}

// ============================================================
// 15. DASHBOARD CHART
// ============================================================
function initDashboardChart() {
  const canvas = document.getElementById('dashboard-stats-chart');
  if (!canvas) return;
  const labels = ['M1','M2','M3','M4','M5','M6','M7','M8'];
  const data = labels.map((_, i) => {
    const modTests = APP.testHistory.filter(t => t.module === `mod${i + 1}` || t.module === 'all');
    const total = modTests.reduce((s, t) => s + t.total, 0);
    const correct = modTests.reduce((s, t) => s + t.correct, 0);
    return total > 0 ? Math.round((correct / total) * 100) : 0;
  });
  APP.charts.dashStats = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Precisión (%)',
        data,
        backgroundColor: ['#00d4ff','#22c55e','#a855f7','#ff6b35','#ec4899','#eab308','#06b6d4','#f43f5e'],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false }, title: { display: true, text: 'Rendimiento por Módulo', color: '#e0e0e0' } },
      scales: {
        y: { min: 0, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#aaa' } },
        x: { grid: { display: false }, ticks: { color: '#aaa' } }
      }
    }
  });
}

// ============================================================
// 16. TEST SYSTEM (matches HTML structure exactly)
// ============================================================
let testTimer = null;
let testSeconds = 0;
let selectedCount = 10;
let selectedDiff = 'all';

function initTestSystem() {
  // Start button
  const startBtn = document.getElementById('test-start-btn');
  if (startBtn) startBtn.addEventListener('click', () => startTest());

  // Count buttons
  document.querySelectorAll('.count-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedCount = btn.dataset.count === 'all' ? 999 : parseInt(btn.dataset.count);
    });
  });

  // Difficulty buttons
  document.querySelectorAll('.diff-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedDiff = btn.dataset.diff;
    });
  });

  // Quick practice buttons
  document.querySelectorAll('.btn-quick-practice').forEach(btn => {
    btn.addEventListener('click', () => startTest(btn.dataset.type, btn.dataset.module || 'all', 10));
  });

  // Retry button
  const retryBtn = document.getElementById('test-retry-btn');
  if (retryBtn) retryBtn.addEventListener('click', () => showPanel('config'));

  // Submit answer button
  const submitBtn = document.getElementById('test-submit-btn');
  if (submitBtn) submitBtn.addEventListener('click', () => submitCurrentAnswer());

  // Skip button
  const skipBtn = document.getElementById('test-skip-btn');
  if (skipBtn) skipBtn.addEventListener('click', () => skipQuestion());

  // Next button
  const nextBtn = document.getElementById('test-next-btn');
  if (nextBtn) nextBtn.addEventListener('click', () => goNextQuestion());
}

function showPanel(panel) {
  const config = document.getElementById('test-config-panel');
  const active = document.getElementById('test-active-panel');
  const results = document.getElementById('test-results-panel');
  const practice = document.getElementById('test-quick-practice');
  if (config) config.style.display = panel === 'config' ? 'block' : 'none';
  if (active) active.style.display = panel === 'active' ? 'block' : 'none';
  if (results) results.style.display = panel === 'results' ? 'block' : 'none';
  if (practice) practice.style.display = (panel === 'config' || panel === 'results') ? 'block' : 'none';
}

function startTest(filterType, filterModule, count) {
  let questions = window.QUESTIONS || [];
  if (!questions.length) { showToast('Cargando preguntas...', 'warning'); return; }

  // Module filter
  if (filterModule && filterModule !== 'all') {
    questions = questions.filter(q => q.module === filterModule);
  } else {
    const modChecks = document.querySelectorAll('.test-module-filter');
    const allCheck = document.querySelector('.test-module-filter[value="all"]');
    if (modChecks.length > 0 && !(allCheck && allCheck.checked)) {
      const activeMods = [];
      modChecks.forEach(cb => { if (cb.checked && cb.value !== 'all') activeMods.push(cb.value); });
      if (activeMods.length > 0) questions = questions.filter(q => activeMods.includes(q.module));
    }
  }

  // Type filter
  if (filterType && filterType !== 'all') {
    questions = questions.filter(q => q.type === filterType);
  } else {
    const typeChecks = document.querySelectorAll('.test-type-filter');
    const allTypeCheck = document.querySelector('.test-type-filter[value="all"]');
    if (typeChecks.length > 0 && !(allTypeCheck && allTypeCheck.checked)) {
      const activeTypes = [];
      typeChecks.forEach(cb => { if (cb.checked && cb.value !== 'all') activeTypes.push(cb.value); });
      if (activeTypes.length > 0) questions = questions.filter(q => activeTypes.includes(q.type));
    }
  }

  // Difficulty filter
  const diff = selectedDiff;
  if (diff && diff !== 'all') {
    const diffMap = { easy: 'facil', medium: 'medio', hard: 'dificil' };
    questions = questions.filter(q => q.difficulty === (diffMap[diff] || diff));
  }

  // Shuffle and limit
  const qty = count || selectedCount;
  questions = shuffleArray(questions).slice(0, Math.min(qty, questions.length));
  if (!questions.length) { showToast('No hay preguntas con esos filtros', 'warning'); return; }

  APP.quizState = {
    questions, current: 0,
    answers: Array(questions.length).fill(null),
    correct: 0, skipped: 0,
    startTime: Date.now(), finished: false,
    currentAnswer: null
  };

  // Timer
  testSeconds = 0;
  if (testTimer) clearInterval(testTimer);
  testTimer = setInterval(() => {
    testSeconds++;
    const m = String(Math.floor(testSeconds / 60)).padStart(2, '0');
    const s = String(testSeconds % 60).padStart(2, '0');
    const el = document.getElementById('test-timer');
    if (el) el.textContent = m + ':' + s;
  }, 1000);

  showPanel('active');
  renderQuestion(0);
}

function renderQuestion(idx) {
  const qs = APP.quizState;
  if (!qs || idx >= qs.questions.length) return;
  qs.current = idx;
  qs.currentAnswer = null;
  const q = qs.questions[idx];
  const answered = qs.answers[idx] !== null;

  // Progress
  const fill = document.getElementById('test-progress-fill');
  if (fill) fill.style.width = ((idx + 1) / qs.questions.length * 100) + '%';
  const counter = document.getElementById('test-question-counter');
  if (counter) counter.textContent = `Pregunta ${idx + 1} de ${qs.questions.length}`;
  const score = document.getElementById('test-score-live');
  if (score) score.textContent = `Aciertos: ${qs.correct}/${qs.answers.filter(a => a !== null).length}`;

  // Badges
  const modNames = { mod1:'Riesgo', mod2:'Diseño', mod3:'Protección', mod4:'Diafragmas', mod5:'Matrices', mod6:'Clasificación', mod7:'Normativa', mod8:'Modal' };
  const modBadge = document.getElementById('test-q-module');
  if (modBadge) modBadge.textContent = modNames[q.module] || q.module;
  const typeBadge = document.getElementById('test-q-type');
  if (typeBadge) typeBadge.textContent = typeLabel(q.type);
  const diffBadge = document.getElementById('test-q-diff');
  if (diffBadge) diffBadge.textContent = q.difficulty;

  // Question text
  const qText = document.getElementById('test-q-text');
  if (qText) qText.innerHTML = q.question;

  // Hide all answer areas
  document.querySelectorAll('.answer-area').forEach(a => a.style.display = 'none');
  // Hide feedback
  const feedback = document.getElementById('test-feedback');
  if (feedback) feedback.style.display = 'none';

  // Show/hide buttons
  const submitBtn = document.getElementById('test-submit-btn');
  const skipBtn = document.getElementById('test-skip-btn');
  const nextBtn = document.getElementById('test-next-btn');
  if (submitBtn) submitBtn.style.display = answered ? 'none' : 'inline-flex';
  if (skipBtn) skipBtn.style.display = answered ? 'none' : 'inline-flex';
  if (nextBtn) nextBtn.style.display = answered ? 'inline-flex' : 'none';
  if (nextBtn) nextBtn.textContent = idx < qs.questions.length - 1 ? 'Siguiente ▶' : 'Ver Resultados ▶';

  // Render answer by type
  switch (q.type) {
    case 'multiple-choice': renderMC(q, idx, answered); break;
    case 'true-false': renderTF(q, idx, answered); break;
    case 'calculation': renderCalc(q, idx, answered); break;
    case 'fill-blank': renderFill(q, idx, answered); break;
    case 'matching': renderMatch(q, idx, answered); break;
    case 'ordering': renderOrder(q, idx, answered); break;
  }

  // Show feedback if already answered
  if (answered) showFeedback(qs.answers[idx].correct, q.explanation, q);

  // MathJax
  if (window.MathJax && MathJax.typesetPromise) {
    const section = document.getElementById('test-active-panel');
    MathJax.typesetPromise([section]).catch(() => {});
  }
}

// --- Multiple Choice ---
function renderMC(q, idx, answered) {
  const area = document.getElementById('answer-multiple-choice');
  if (!area) return;
  area.style.display = 'block';
  const container = document.getElementById('test-mc-options');
  if (!container) return;
  const prev = APP.quizState.answers[idx];
  let html = '';
  q.options.forEach((opt, i) => {
    let cls = 'mc-option';
    if (answered && i === q.correct) cls += ' correct';
    if (answered && prev.selected === i && i !== q.correct) cls += ' wrong';
    if (!answered && APP.quizState.currentAnswer === i) cls += ' selected';
    html += `<button class="${cls}" data-idx="${i}" ${answered ? 'disabled' : ''}><span class="option-letter">${String.fromCharCode(65 + i)}</span><span class="option-text">${opt}</span></button>`;
  });
  container.innerHTML = html;
  if (!answered) {
    container.querySelectorAll('.mc-option').forEach(btn => {
      btn.addEventListener('click', () => {
        container.querySelectorAll('.mc-option').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        APP.quizState.currentAnswer = parseInt(btn.dataset.idx);
      });
    });
  }
}

// --- True/False ---
function renderTF(q, idx, answered) {
  const area = document.getElementById('answer-true-false');
  if (!area) return;
  area.style.display = 'block';
  const prev = APP.quizState.answers[idx];
  area.querySelectorAll('.btn-tf').forEach(btn => {
    const val = btn.dataset.answer === 'true';
    btn.classList.remove('selected', 'correct', 'wrong');
    if (answered && val === q.correct) btn.classList.add('correct');
    if (answered && prev.selected === val && val !== q.correct) btn.classList.add('wrong');
    if (!answered && APP.quizState.currentAnswer === val) btn.classList.add('selected');
    btn.disabled = answered;
    if (!answered) {
      btn.onclick = () => {
        area.querySelectorAll('.btn-tf').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        APP.quizState.currentAnswer = val;
      };
    }
  });
}

// --- Calculation ---
function renderCalc(q, idx, answered) {
  const area = document.getElementById('answer-calculation');
  if (!area) return;
  area.style.display = 'block';
  const input = document.getElementById('test-calc-input');
  const unit = document.getElementById('test-calc-unit');
  const hint = document.getElementById('test-calc-hint');
  if (input) { input.value = answered ? APP.quizState.answers[idx].value : ''; input.disabled = answered; }
  if (unit) unit.textContent = q.unit || '';
  if (hint) hint.textContent = q.hint || '';
  if (!answered && input) {
    input.oninput = () => { APP.quizState.currentAnswer = parseFloat(input.value); };
  }
}

// --- Fill Blank ---
function renderFill(q, idx, answered) {
  const area = document.getElementById('answer-fill-blank');
  if (!area) return;
  area.style.display = 'block';
  const group = area.querySelector('.fill-blank-group');
  if (!group) return;
  const prev = APP.quizState.answers[idx];
  let html = '<label>Completa los espacios:</label>';
  (q.blanks || ['']).forEach((_, i) => {
    html += `<input type="text" class="input-fill fill-input-${idx}" data-blank="${i}" placeholder="Espacio ${i + 1}" ${answered ? 'disabled' : ''} value="${prev ? (prev.values?.[i] || '') : ''}">`;
  });
  group.innerHTML = html;
  if (!answered) {
    group.querySelectorAll('input').forEach(inp => {
      inp.oninput = () => {
        const vals = [...group.querySelectorAll('input')].map(i => i.value.trim());
        APP.quizState.currentAnswer = vals;
      };
    });
  }
}

// --- Matching ---
function renderMatch(q, idx, answered) {
  const area = document.getElementById('answer-matching');
  if (!area) return;
  area.style.display = 'block';
  const leftCol = document.getElementById('test-match-left');
  const rightCol = document.getElementById('test-match-right');
  if (!leftCol || !rightCol) return;
  const prev = APP.quizState.answers[idx];
  const rightItems = prev ? prev.rightOrder : shuffleArray(q.pairs.map(p => p.right));
  if (!prev && !APP.quizState.matchOrders) APP.quizState.matchOrders = {};
  if (!prev) APP.quizState.matchOrders[idx] = [...rightItems];

  leftCol.innerHTML = q.pairs.map((p, i) => `<div class="match-item">${i + 1}. ${p.left}</div>`).join('');
  rightCol.innerHTML = rightItems.map((r, i) => `<div class="match-item" draggable="${!answered}" data-idx="${i}">${r}</div>`).join('');

  if (!answered) {
    APP.quizState.currentAnswer = rightItems;
    initDragReorder2(rightCol, () => {
      const items = [...rightCol.querySelectorAll('.match-item')].map(el => el.textContent);
      APP.quizState.currentAnswer = items;
      if (APP.quizState.matchOrders) APP.quizState.matchOrders[idx] = items;
    });
  }
}

// --- Ordering ---
function renderOrder(q, idx, answered) {
  const area = document.getElementById('answer-ordering');
  if (!area) return;
  area.style.display = 'block';
  const list = document.getElementById('test-ordering-list');
  if (!list) return;
  const prev = APP.quizState.answers[idx];
  const items = prev ? prev.order : shuffleArray([...q.items]);

  list.innerHTML = items.map((item, i) => `<div class="order-item" draggable="${!answered}" data-idx="${i}"><span class="order-num">${i + 1}</span><span class="order-text">${item}</span></div>`).join('');

  if (!answered) {
    APP.quizState.currentAnswer = items;
    initDragReorder2(list, () => {
      const ordered = [...list.querySelectorAll('.order-text')].map(el => el.textContent);
      APP.quizState.currentAnswer = ordered;
      list.querySelectorAll('.order-num').forEach((n, i) => n.textContent = i + 1);
    });
  }
}

function initDragReorder2(container, onChange) {
  let dragItem = null;
  container.querySelectorAll('[draggable="true"]').forEach(item => {
    item.addEventListener('dragstart', () => { dragItem = item; item.style.opacity = '0.4'; });
    item.addEventListener('dragend', () => { item.style.opacity = '1'; dragItem = null; });
    item.addEventListener('dragover', e => { e.preventDefault(); item.classList.add('drag-over'); });
    item.addEventListener('dragleave', () => item.classList.remove('drag-over'));
    item.addEventListener('drop', e => {
      e.preventDefault(); item.classList.remove('drag-over');
      if (dragItem && dragItem !== item) {
        const all = [...container.children];
        const from = all.indexOf(dragItem), to = all.indexOf(item);
        if (from < to) container.insertBefore(dragItem, item.nextSibling);
        else container.insertBefore(dragItem, item);
        if (onChange) onChange();
      }
    });
  });
}

// --- Submit / Skip / Next ---
function submitCurrentAnswer() {
  const qs = APP.quizState;
  if (!qs || qs.answers[qs.current] !== null) return;
  const q = qs.questions[qs.current];
  const ans = qs.currentAnswer;
  if (ans === null || ans === undefined) { showToast('Selecciona una respuesta', 'warning'); return; }

  let correct = false;
  let result = {};

  switch (q.type) {
    case 'multiple-choice':
      correct = ans === q.correct;
      result = { selected: ans, correct };
      break;
    case 'true-false':
      correct = ans === q.correct;
      result = { selected: ans, correct };
      break;
    case 'calculation':
      const tol = q.tolerance || 0.05;
      correct = Math.abs(ans - q.answer) <= Math.abs(q.answer * tol) + 0.001;
      result = { value: ans, correct };
      break;
    case 'fill-blank':
      const vals = Array.isArray(ans) ? ans : [ans];
      correct = q.blanks.every((b, i) => (vals[i] || '').toLowerCase().trim() === b.toLowerCase().trim());
      result = { values: vals, correct };
      break;
    case 'matching':
      const rightOrder = Array.isArray(ans) ? ans : (qs.matchOrders?.[qs.current] || []);
      correct = q.pairs.every((p, i) => rightOrder[i] === p.right);
      result = { rightOrder, correct };
      break;
    case 'ordering':
      const order = Array.isArray(ans) ? ans : [];
      correct = q.items.every((it, i) => order[i] === it);
      result = { order, correct };
      break;
  }

  qs.answers[qs.current] = result;
  if (correct) qs.correct++;

  // Re-render with feedback
  renderQuestion(qs.current);
  showFeedback(correct, q.explanation, q);
}

function skipQuestion() {
  const qs = APP.quizState;
  if (!qs) return;
  qs.answers[qs.current] = { skipped: true, correct: false };
  qs.skipped++;
  goNextQuestion();
}

function goNextQuestion() {
  const qs = APP.quizState;
  if (!qs) return;
  if (qs.current < qs.questions.length - 1) {
    renderQuestion(qs.current + 1);
  } else {
    finishTest();
  }
}

function showFeedback(correct, explanation, q) {
  const fb = document.getElementById('test-feedback');
  if (!fb) return;
  fb.style.display = 'block';
  const icon = document.getElementById('test-feedback-icon');
  const text = document.getElementById('test-feedback-text');
  const expl = document.getElementById('test-feedback-explanation');
  if (icon) { icon.textContent = correct ? '✓' : '✗'; icon.className = 'feedback-icon ' + (correct ? 'feedback-correct' : 'feedback-wrong'); }
  if (text) { text.textContent = correct ? '¡Correcto!' : 'Incorrecto'; text.className = 'feedback-text ' + (correct ? 'text-success' : 'text-danger'); }
  let explHtml = explanation || '';
  if (!correct && q.type === 'calculation') explHtml = `Respuesta correcta: ${q.answer} ${q.unit || ''}. ` + explHtml;
  if (!correct && q.type === 'fill-blank') explHtml = `Respuestas: ${q.blanks.join(', ')}. ` + explHtml;
  if (expl) expl.innerHTML = explHtml;
  fb.classList.add('animate-fadeIn');
}

// ============================================================
// 17. ANSWER HANDLERS
// ============================================================
window.selectMC = function(idx, choice) {
  const q = APP.quizState.questions[idx];
  const correct = choice === q.correct;
  APP.quizState.answers[idx] = { selected: choice, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.selectTF = function(idx, value) {
  const q = APP.quizState.questions[idx];
  const correct = value === q.correct;
  APP.quizState.answers[idx] = { selected: value, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.submitCalc = function(idx) {
  const q = APP.quizState.questions[idx];
  const input = document.getElementById(`calc-input-${idx}`);
  const val = parseFloat(input?.value);
  if (isNaN(val)) { showToast('Ingresa un número', 'warning'); return; }
  const tol = q.tolerance || 0.01;
  const correct = Math.abs(val - q.answer) <= Math.abs(q.answer * tol);
  APP.quizState.answers[idx] = { value: val, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.submitFill = function(idx) {
  const q = APP.quizState.questions[idx];
  const values = q.blanks.map((_, i) => document.getElementById(`fill-${idx}-${i}`)?.value?.trim().toLowerCase() || '');
  const correct = q.blanks.every((b, i) => values[i] === b.toLowerCase());
  APP.quizState.answers[idx] = { values, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.submitMatch = function(idx) {
  const q = APP.quizState.questions[idx];
  const rightOrder = APP.quizState.matchOrders?.[idx] || [];
  const correct = q.pairs.every((p, i) => rightOrder[i] === p.right);
  APP.quizState.answers[idx] = { rightOrder, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.submitOrder = function(idx) {
  const q = APP.quizState.questions[idx];
  const list = document.getElementById('order-list-' + idx);
  if (!list) return;
  const items = [...list.querySelectorAll('.order-item .order-text')].map(el => el.textContent);
  const correct = q.items.every((it, i) => items[i] === it);
  APP.quizState.answers[idx] = { order: items, correct };
  if (correct) APP.quizState.correct++;
  renderQuestion(idx);
};

window.renderQuestion = renderQuestion;

window.finishTest = function() {
  const qs = APP.quizState;
  if (!qs) return;
  qs.finished = true;
  if (testTimer) { clearInterval(testTimer); testTimer = null; }
  const elapsed = testSeconds;
  const pct = Math.round((qs.correct / qs.questions.length) * 100);
  APP.testHistory.push({
    date: new Date().toISOString(),
    total: qs.questions.length,
    correct: qs.correct,
    pct, elapsed, module: 'all'
  });
  saveProgress();
  showResults(qs, elapsed, pct);
  updateDashboard();
};

function showResults(qs, elapsed, pct) {
  showPanel('results');
  const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const secs = String(elapsed % 60).padStart(2, '0');
  // Score ring
  drawProgressRing('test-results-ring', pct / 100);
  const pctEl = document.getElementById('test-results-pct');
  if (pctEl) pctEl.textContent = pct + '%';
  // Stats
  const el = (id, val) => { const e = document.getElementById(id); if (e) e.textContent = val; };
  el('results-correct', qs.correct);
  el('results-incorrect', qs.questions.length - qs.correct - (qs.skipped || 0));
  el('results-skipped', qs.skipped || 0);
  el('results-time', mins + ':' + secs);
  // Review list
  const reviewList = document.getElementById('test-review-list');
  if (reviewList) {
    reviewList.innerHTML = qs.questions.map((q, i) => {
      const ans = qs.answers[i];
      const isCorrect = ans && ans.correct;
      const isSkipped = ans && ans.skipped;
      const cls = isSkipped ? 'review-skipped' : (isCorrect ? 'review-correct' : 'review-wrong');
      const icon = isSkipped ? '–' : (isCorrect ? '✓' : '✗');
      return `<div class="review-item ${cls}" data-review-status="${isSkipped ? 'skipped' : (isCorrect ? 'correct' : 'incorrect')}">
        <span class="review-icon">${icon}</span>
        <span class="review-num">${i + 1}</span>
        <span class="review-text">${q.question.substring(0, 100)}${q.question.length > 100 ? '...' : ''}</span>
        <span class="badge badge-${q.type}">${typeLabel(q.type)}</span>
      </div>`;
    }).join('');
  }
  // Review filter buttons
  document.querySelectorAll('.review-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.review-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      document.querySelectorAll('.review-item').forEach(item => {
        if (filter === 'all') item.style.display = '';
        else item.style.display = item.dataset.reviewStatus === filter ? '' : 'none';
      });
    });
  });
  // Results by module chart
  const modCanvas = document.getElementById('test-results-by-module');
  if (modCanvas) {
    const modLabels = ['M1','M2','M3','M4','M5','M6','M7','M8'];
    const modData = modLabels.map((_, i) => {
      const mod = `mod${i + 1}`;
      const modQs = qs.questions.filter(q => q.module === mod);
      const modCorrect = modQs.filter((q, qi) => {
        const origIdx = qs.questions.indexOf(q);
        return qs.answers[origIdx] && qs.answers[origIdx].correct;
      }).length;
      return modQs.length > 0 ? Math.round((modCorrect / modQs.length) * 100) : 0;
    });
    new Chart(modCanvas, {
      type: 'bar', data: { labels: modLabels, datasets: [{ data: modData, backgroundColor: '#00d4ff', borderRadius: 6 }] },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { min: 0, max: 100, ticks: { color: '#aaa' } }, x: { ticks: { color: '#aaa' } } } }
    });
  }
  // Results by type chart
  const typeCanvas = document.getElementById('test-results-by-type');
  if (typeCanvas) {
    const types = ['multiple-choice','true-false','calculation','fill-blank','matching','ordering'];
    const typeLabelsArr = types.map(t => typeLabel(t));
    const typeData = types.map(t => {
      const tQs = qs.questions.filter(q => q.type === t);
      const tCorrect = tQs.filter(q => { const idx = qs.questions.indexOf(q); return qs.answers[idx] && qs.answers[idx].correct; }).length;
      return tQs.length > 0 ? Math.round((tCorrect / tQs.length) * 100) : 0;
    });
    new Chart(typeCanvas, {
      type: 'bar', data: { labels: typeLabelsArr, datasets: [{ data: typeData, backgroundColor: '#a855f7', borderRadius: 6 }] },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { min: 0, max: 100, ticks: { color: '#aaa' } }, x: { ticks: { color: '#aaa', font: { size: 10 } } } } }
    });
  }
}

window.renderQuestion = renderQuestion;

// ============================================================
// 18. UTILITIES
// ============================================================
function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function typeLabel(type) {
  const labels = {
    'multiple-choice': 'Opción Múltiple',
    'true-false': 'V/F',
    'calculation': 'Cálculo',
    'fill-blank': 'Completar',
    'matching': 'Asociar',
    'ordering': 'Ordenar'
  };
  return labels[type] || type;
}

function initDragReorder(listId) {
  const list = document.getElementById(listId);
  if (!list) return;
  let dragItem = null;
  list.querySelectorAll('.order-item').forEach(item => {
    item.addEventListener('dragstart', () => { dragItem = item; item.style.opacity = '0.4'; });
    item.addEventListener('dragend', () => { dragItem = null; item.style.opacity = '1'; });
    item.addEventListener('dragover', e => { e.preventDefault(); item.classList.add('drag-over'); });
    item.addEventListener('dragleave', () => item.classList.remove('drag-over'));
    item.addEventListener('drop', e => {
      e.preventDefault(); item.classList.remove('drag-over');
      if (dragItem && dragItem !== item) {
        const items = [...list.children];
        const fromIdx = items.indexOf(dragItem);
        const toIdx = items.indexOf(item);
        if (fromIdx < toIdx) list.insertBefore(dragItem, item.nextSibling);
        else list.insertBefore(dragItem, item);
        // Renumber
        list.querySelectorAll('.order-num').forEach((num, i) => num.textContent = i + 1);
      }
    });
  });
}

// ============================================================
// 19. SCROLL TO TOP
// ============================================================
function initScrollTop() {
  const btn = document.getElementById('scroll-top');
  const main = document.getElementById('main-content');
  if (!btn || !main) return;
  main.addEventListener('scroll', () => {
    btn.style.display = main.scrollTop > 300 ? 'flex' : 'none';
  });
  btn.addEventListener('click', () => main.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ============================================================
// 20. RESET
// ============================================================
function initReset() {
  const btn = document.getElementById('reset-progress');
  if (btn) btn.addEventListener('click', () => {
    if (confirm('¿Reiniciar todo el progreso? Se borrarán tests e historial.')) {
      localStorage.removeItem('adse-c1-progress');
      localStorage.removeItem('adse-c1-visited');
      localStorage.removeItem('adse-c1-tests');
      location.reload();
    }
  });
}

// ============================================================
// 21. INIT
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initScrollTop();
  initReset();
  updateDashboard();
  initModuleIfNeeded('dashboard');
  // Questions loaded via <script defer> in HTML
  if (window.QUESTIONS) showToast('250 preguntas cargadas', 'success');
});
