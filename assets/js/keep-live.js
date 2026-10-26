/* The Keep's live chart: 15-minute means from api.eldrsystems.com.

   The page ships a build-time snapshot (layouts/_partials/keep/live.html), so
   a chart is on screen before any request. Live data replaces it per metric,
   on first view and every 15 minutes while the tab is visible. A failed
   request keeps whatever is drawn and says how old it is; it never blanks
   the chart. The API answers CORS for eldrsystems.com only, so on localhost
   every request fails and the snapshot is what you see.

   Hand-rolled SVG, no library: two lines, a few ticks and a crosshair. */

const H = 220;
const M = { top: 24, right: 30, bottom: 26, left: 40 };
const REFRESH = 15 * 60 * 1000; // ms. The API's buckets are 15 minutes.
const NS = 'http://www.w3.org/2000/svg';

// Values arrive in the API's unit; `k` converts to the unit shown.
const METRICS = {
  battery: { title: 'Battery voltage', unit: 'V', k: 1 / 1000, dp: 2 },
  temp: { title: 'Temperature', unit: '°C', k: 1, dp: 1 },
  rssi: { title: 'Signal strength', unit: 'dBm', k: 1, dp: 0 },
};

const fig = document.querySelector('[data-keep-live]');
if (fig) init(fig);

function init(fig) {
  const $ = (s) => fig.querySelector(s);
  const cfg = JSON.parse($('[data-kl-data]').textContent);
  const api = fig.dataset.api;
  const days = fig.dataset.days;
  const devices = cfg.devices;
  const plot = $('[data-kl-plot]');
  const svg = $('[data-kl-svg]');
  const tip = $('[data-kl-tip]');
  const status = $('[data-kl-status]');

  // metric -> { start, end, bucket (s), series: { id: [[i, v], ...] }, live }
  const data = {};
  for (const [m, d] of Object.entries(cfg.snapshot || {})) {
    const series = {};
    for (const [id, s] of Object.entries(d.series)) series[id] = s.i.map((i, k) => [i, s.v[k]]);
    data[m] = { ...d, series, live: false };
  }
  const fetchedAt = {};
  let metric = 'battery';
  let view = null; // geometry of the current render, for the crosshair
  let cursor = -1; // index into view.times, for the keyboard

  const timeFmt = new Intl.DateTimeFormat('en-GB', { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
  const clockFmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit' });
  const stampFmt = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
  const dayFmt = new Intl.DateTimeFormat('en-GB', { weekday: 'short', day: 'numeric' });

  const fmt = (v, m = metric) => {
    const s = METRICS[m];
    return `${(v * s.k).toFixed(s.dp).replace('-', '−')} ${s.unit}`;
  };
  const tsOf = (d, i) => Date.parse(d.start) + i * d.bucket * 1000;

  async function load(m) {
    const one = async (dev) => {
      const r = await fetch(`${api}/public/v1/${m}?device=${encodeURIComponent(dev.id)}&days=${days}`);
      if (!r.ok) throw new Error(`${r.status}`);
      return r.json();
    };
    plot.classList.add('is-loading');
    try {
      const res = await Promise.all(devices.map(one));
      const start = Date.parse(res[0].start);
      const bucket = res[0].bucket_s;
      const series = {};
      res.forEach((j, n) => {
        series[devices[n].id] = j.points.map((p) => [Math.round((Date.parse(p.ts) - start) / 1000 / bucket), p.value]);
      });
      data[m] = { start: res[0].start, end: res[0].end, bucket, series, live: true };
      fetchedAt[m] = Date.now();
    } catch {
      // Keep what is drawn; the status line says it is a snapshot.
    } finally {
      plot.classList.remove('is-loading');
      if (m === metric) render();
    }
  }

  function render() {
    const d = data[metric];
    const s = METRICS[metric];
    $('[data-kl-title]').textContent = s.title;
    svg.setAttribute('aria-label', `Chart of ${s.title.toLowerCase()} from The Keep. The latest readings are listed below it.`);
    renderStatus(d);
    renderReadouts(d);
    renderChart(d);
  }

  function renderStatus(d) {
    if (!d) status.textContent = 'no data available';
    else if (d.live) status.textContent = `live · updated ${clockFmt.format(fetchedAt[metric])}`;
    else status.textContent = `snapshot · last updated ${stampFmt.format(Date.parse(d.end))}`;
  }

  function renderReadouts(d) {
    for (const dev of devices) {
      const row = fig.querySelector(`[data-kl-device="${CSS.escape(dev.id)}"]`);
      const pts = d?.series[dev.id] || [];
      const last = pts[pts.length - 1];
      row.querySelector('[data-kl-value]').textContent = last ? fmt(last[1]) : '—';
      row.querySelector('[data-kl-at]').textContent = last ? stampFmt.format(tsOf(d, last[0])) : `no reading in ${days} days`;
    }
  }

  function el(name, attrs, parent) {
    const e = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (parent) parent.appendChild(e);
    return e;
  }

  function renderChart(d) {
    const W = svg.clientWidth || 520;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.replaceChildren();
    view = null;
    hideTip();

    const all = d ? devices.flatMap((dev) => d.series[dev.id] || []) : [];
    if (!all.length) {
      el('text', { x: W / 2, y: H / 2, 'text-anchor': 'middle', class: 'kl-empty' }, svg).textContent = 'No readings to show';
      return;
    }

    const t0 = Date.parse(d.start);
    const t1 = Date.parse(d.end);
    const x = (t) => M.left + ((t - t0) / (t1 - t0)) * (W - M.left - M.right);
    const [lo, hi, step] = niceDomain(all.map((p) => p[1] * METRICS[metric].k));
    const y = (v) => H - M.bottom - ((v * METRICS[metric].k - lo) / (hi - lo)) * (H - M.top - M.bottom);

    // Grid and y ticks, in the shown unit.
    for (let v = lo; v <= hi + step / 2; v += step) {
      const py = H - M.bottom - ((v - lo) / (hi - lo)) * (H - M.top - M.bottom);
      if (v > lo) el('path', { d: `M${M.left},${py} H${W - M.right}`, class: 'kl-grid' }, svg);
      el('text', { x: M.left - 8, y: py + 4, 'text-anchor': 'end', class: 'kl-tick' }, svg).textContent = v
        .toFixed(METRICS[metric].dp)
        .replace('-', '−');
    }
    el('path', { d: `M${M.left},${H - M.bottom} H${W - M.right}`, class: 'kl-base' }, svg);
    // The unit sits above the axis rather than on a tick, so the tick
    // column stays narrow enough for a phone.
    el('text', { x: 0, y: 10, class: 'kl-tick' }, svg).textContent = METRICS[metric].unit;

    // Day ticks at local midnight; every other day when narrow.
    const every = W < 440 ? 2 : 1;
    const day = new Date(t0);
    day.setHours(24, 0, 0, 0);
    for (let n = 0; day.getTime() < t1; n++, day.setDate(day.getDate() + 1)) {
      if (n % every) continue;
      const px = x(day.getTime());
      el('path', { d: `M${px},${H - M.bottom} v4`, class: 'kl-base' }, svg);
      el('text', { x: px, y: H - 6, 'text-anchor': 'middle', class: 'kl-tick' }, svg).textContent = dayFmt.format(day);
    }

    // One path per device, broken where the device went quiet: a gap longer
    // than three of its usual reporting intervals is not drawn across.
    const ends = [];
    const lines = devices.map((dev, n) => {
      const pts = d.series[dev.id] || [];
      const gap = 3 * medianStep(pts);
      let path = '';
      pts.forEach(([i, v], k) => {
        const cmd = k && i - pts[k - 1][0] <= gap ? 'L' : 'M';
        path += `${cmd}${x(tsOf(d, i)).toFixed(1)},${y(v).toFixed(1)}`;
      });
      const stroke = `var(--kl-s${n})`;
      el('path', { d: path, fill: 'none', stroke, 'stroke-width': 2, 'stroke-linejoin': 'round', ...(n ? { 'stroke-dasharray': '5 3' } : {}) }, svg);
      const last = pts[pts.length - 1];
      if (last) {
        const px = x(tsOf(d, last[0]));
        const py = y(last[1]);
        el('circle', { cx: px, cy: py, r: 3.5, fill: stroke, stroke: 'var(--color-bone)', 'stroke-width': 2 }, svg);
        ends.push({ px, py, label: dev.label.replace(/^Device /, '') });
      }
      return { dev, pts, gap, stroke };
    });

    // Direct labels at the line ends, nudged apart when they would collide.
    ends.sort((a, b) => a.py - b.py);
    for (let k = 1; k < ends.length; k++) ends[k].py = Math.max(ends[k].py, ends[k - 1].py + 12);
    for (const e of ends) el('text', { x: e.px + 8, y: e.py + 4, class: 'kl-end' }, svg).textContent = e.label;

    const cross = el('path', { d: '', class: 'kl-cross', visibility: 'hidden' }, svg);
    const times = [...new Set(lines.flatMap((l) => l.pts.map((p) => p[0])))].sort((a, b) => a - b);
    view = { d, x, y, W, t0, t1, lines, cross, times };
    cursor = -1;
  }

  function showAt(i) {
    if (!view) return;
    const { d, x, y, lines, cross } = view;
    const px = x(tsOf(d, i));
    cross.setAttribute('d', `M${px},${M.top} V${H - M.bottom}`);
    cross.setAttribute('visibility', 'visible');

    const rows = [];
    for (const l of lines) {
      const p = nearest(l.pts, i);
      // Only a reading close to the cursor counts; otherwise the device was quiet.
      rows.push({ l, v: p && Math.abs(p[0] - i) <= Math.max(1, l.gap / 3) ? p[1] : null });
    }
    const time = document.createElement('div');
    time.className = 'kl-tip-time';
    time.textContent = timeFmt.format(tsOf(d, i));
    const kids = [time];
    for (const { l, v } of rows) {
      const row = document.createElement('div');
      row.className = 'kl-tip-row';
      const key = document.createElementNS(NS, 'svg');
      key.setAttribute('width', '14');
      key.setAttribute('height', '6');
      el('path', { d: 'M0,3 H14', stroke: l.stroke, 'stroke-width': 2 }, key);
      const val = document.createElement('b');
      val.textContent = v == null ? '—' : fmt(v);
      const name = document.createElement('span');
      name.textContent = l.dev.label;
      row.append(key, val, name);
      kids.push(row);
    }
    tip.replaceChildren(...kids);
    tip.hidden = false;
    const w = tip.offsetWidth;
    const scale = svg.clientWidth / view.W;
    const left = px * scale + 12 + w > svg.clientWidth ? px * scale - 12 - w : px * scale + 12;
    tip.style.left = `${Math.max(0, left)}px`;
  }

  function hideTip() {
    tip.hidden = true;
    view?.cross.setAttribute('visibility', 'hidden');
  }

  function indexAtPointer(ev) {
    const r = svg.getBoundingClientRect();
    const px = ((ev.clientX - r.left) / r.width) * view.W;
    const t = view.t0 + ((px - M.left) / (view.W - M.left - M.right)) * (view.t1 - view.t0);
    const i = (t - view.t0) / 1000 / view.d.bucket;
    // Snap to the nearest moment any device reported.
    let k = nearestIdx(view.times, i);
    cursor = k;
    return view.times[k];
  }

  svg.addEventListener('pointermove', (ev) => {
    if (view?.times.length) showAt(indexAtPointer(ev));
  });
  svg.addEventListener('pointerleave', hideTip);
  svg.addEventListener('blur', hideTip);
  svg.addEventListener('keydown', (ev) => {
    if (!view?.times.length) return;
    const n = view.times.length;
    const moves = { ArrowLeft: -1, ArrowRight: 1, Home: -n, End: n };
    if (ev.key === 'Escape') return hideTip();
    if (!(ev.key in moves)) return;
    ev.preventDefault();
    cursor = cursor < 0 ? n - 1 : Math.min(n - 1, Math.max(0, cursor + moves[ev.key]));
    showAt(view.times[cursor]);
  });

  for (const b of fig.querySelectorAll('[data-kl-metric]')) {
    b.addEventListener('click', () => {
      metric = b.dataset.klMetric;
      for (const o of fig.querySelectorAll('[data-kl-metric]')) o.setAttribute('aria-pressed', String(o === b));
      render();
      if (!fetchedAt[metric] || Date.now() - fetchedAt[metric] > REFRESH) load(metric);
    });
  }

  let width = 0;
  new ResizeObserver(() => {
    if (svg.clientWidth !== width) {
      width = svg.clientWidth;
      renderChart(data[metric]);
    }
  }).observe(svg);

  setInterval(() => {
    if (document.visibilityState === 'visible') load(metric);
  }, REFRESH);

  render();
  load(metric);
}

function medianStep(pts) {
  if (pts.length < 2) return 1;
  const d = [];
  for (let k = 1; k < pts.length; k++) d.push(pts[k][0] - pts[k - 1][0]);
  d.sort((a, b) => a - b);
  return d[d.length >> 1];
}

function nearestIdx(arr, i) {
  let lo = 0;
  let hi = arr.length - 1;
  while (hi - lo > 1) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] < i) lo = mid;
    else hi = mid;
  }
  return Math.abs(arr[lo] - i) <= Math.abs(arr[hi] - i) ? lo : hi;
}

function nearest(pts, i) {
  if (!pts.length) return null;
  return pts[nearestIdx(pts.map((p) => p[0]), i)];
}

// Pads the range and rounds it out to 1, 2, 2.5 or 5 × 10^n, about four ticks.
function niceDomain(vals) {
  let lo = Math.min(...vals);
  let hi = Math.max(...vals);
  if (hi - lo < 1e-9) {
    lo -= 1;
    hi += 1;
  }
  const raw = (hi - lo) / 4;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((f) => f * mag).find((s) => s >= raw);
  return [Math.floor(lo / step) * step, Math.ceil(hi / step) * step, step];
}
