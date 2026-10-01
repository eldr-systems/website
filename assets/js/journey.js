/* The journey: one ember dot carries a measurement down the homepage, from
   the device in the hero to The Keep's live chart.

   Progressive enhancement only. The CSS that makes room for it is gated on
   (scripting: enabled), every meaning stays in the HTML, and scroll is only
   ever read, never written. The trace is built from the real positions of
   the section dividers and the station ports, and rebuilt when the layout
   changes, never on scroll.

   No library: the trace is straight segments and 45° chamfers, so a point
   at a given length is plain arithmetic. That is all GSAP's MotionPath and
   ScrollTrigger would have done here, at a fraction of the weight. */

const CHAMFER = 10; //    px. PCB corners are cut at 45°, never rounded.
const CROSS = 420; //     desktop: scroll px per horizontal crossing (at most
//                        CROSS_VH of the viewport, so the dot stays on screen)
const CROSS_VH = 0.45;
const WAVE_W = 120; //    desktop: length of the wave packet the line turns into, px
const WAVE_A = 7; //      and its amplitude, px
const WAVE_RAMP = 80; //  path px over which the dot opens into the wave
const STUB = 40; //       rail: scroll px for its short horizontal stubs
const LINGER = 200; //    desktop: extra scroll px the dot spends in a station
const RADIO_STUB = 28; // desktop: wire left at each end of the radio gap
const RAIL_X = 14; //     rail distance from the left edge
const BAND = 0.5; //      where in the viewport the dot rides
const TAU = 0.09; //      scroll smoothing time constant, s
const ORDER = ['modem', 'tower', 'backend', 'analysis'];
const NS = 'http://www.w3.org/2000/svg';

const root = document.querySelector('[data-journey]');
const svg = root && root.querySelector('.j-overlay');
const mq = {
  desk: matchMedia('(scripting: enabled) and (min-width: 1280px)'),
  rail: matchMedia('(scripting: enabled) and (max-width: 1279.98px)'),
  still: matchMedia('(prefers-reduced-motion: reduce)'),
  coarse: matchMedia('(pointer: coarse)'),
};

if (svg && (mq.desk.matches || mq.rail.matches)) init();

function init() {
  let g = null; //    geometry from the last measure
  let vw = innerWidth;
  let vh = innerHeight;
  let cur = scrollY;
  let target = cur;
  let raf = 0;
  let last = 0;
  let queued = 0;

  const measureSoon = () => {
    if (!queued) queued = requestAnimationFrame(() => { queued = 0; measure(); });
  };

  function measure() {
    const desk = mq.desk.matches;
    g = null;
    // Dividers the overlay redraws (see build) give up their own border, but
    // only while it is drawn; reset first so a failed build leaves the CSS.
    for (const e of root.querySelectorAll('.j-div')) e.classList.remove('j-div');
    if (desk || mq.rail.matches) {
      const o = root.getBoundingClientRect();
      const route = (desk ? routeDesktop : routeRail)(o);
      if (route) g = build(route, o, desk);
    }
    if (!g) { svg.replaceChildren(); return; }
    cur = target = scrollY;
    render();
  }

  function build(raw, o, desk) {
    const pts = chamfer(raw);
    const n = pts.length;
    const L = [0];
    for (let k = 1; k < n; k++) L[k] = L[k - 1] + dist(pts[k - 1], pts[k]);
    const mainEnd = pts.findIndex((p) => p.end);

    // Scroll position at which the dot reaches each vertex. By default the dot
    // rides at BAND of the viewport, so S = y − band. Horizontal runs get a
    // fixed share of scroll centred on that, stations get extra, and the
    // result is forced monotonic and reachable.
    const band = vh * BAND;
    const S = pts.map((p) => p.y - band);
    const flat = (k) => pts[k].s !== 'gap' && Math.abs(pts[k].y - pts[k - 1].y) < 0.5 && L[k] > L[k - 1];
    // Per segment: the crossing it belongs to, and how the dot rides it.
    // Wire crossings carry it as a wave in the line; the radio link as a
    // wavefront in the air, opening toward the tower.
    const wave = [];
    for (let k = 1; k < n; k++) {
      if (!flat(k)) continue;
      const a = k - 1;
      while (k + 1 < n && flat(k + 1)) k++;
      const share = desk ? Math.min(CROSS, vh * CROSS_VH) : STUB;
      const s0 = pts[a].y - band - share / 2;
      for (let j = a; j <= k; j++) S[j] = s0 + (share * (L[j] - L[a])) / (L[k] - L[a]);
      if (desk) {
        const seg = pts.slice(a + 1, k + 1);
        const kind = seg.every((p) => p.s === 'wire') ? 'wave' : seg.some((p) => p.s === 'radio') ? 'radio' : null;
        const run = { kind, L0: L[a], L1: L[k], dir: Math.sign(pts[k].x - pts[a].x) || 1 };
        if (kind) for (let j = a; j < k; j++) wave[j] = run;
      }
    }
    if (desk) {
      for (let k = 1; k < n; k++) {
        if (pts[k].s === 'station') { S[k - 1] -= LINGER / 2; S[k] += LINGER / 2; }
      }
    }
    S[0] = Math.max(S[0], 0);
    for (let k = 1; k < n; k++) S[k] = Math.max(S[k], S[k - 1] + 0.01);
    // Mobile toolbars change the real maximum by up to ~100px; stay inside it.
    const maxS = document.documentElement.scrollHeight - vh - (mq.coarse.matches ? 120 : 4);
    if (S[n - 1] > maxS) {
      S[n - 1] = maxS;
      for (let k = n - 2; k >= 0; k--) S[k] = Math.min(S[k], S[k + 1] - 0.01);
    }

    // Draw. Untravelled and travelled copies of every run; the travelled copy
    // is revealed with stroke-dashoffset. Station interiors, the radio gap and
    // the jump from the chart to the epilogue are not drawn.
    const el = (tag, attrs, parent) => {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(e);
      return e;
    };
    const d = (k0, k1) => pts.slice(k0, k1 + 1).map((p, i) => `${i ? 'L' : 'M'}${r(p.x)} ${r(p.y)}`).join('');
    const defs = el('defs', {});
    const under = el('g', {});
    const over = el('g', {});
    const runs = [];
    let run = null;
    for (let k = 1; k < n; k++) {
      const kind = pts[k].s === 'wire' || pts[k].s === 'epi' ? pts[k].s : null;
      if (!kind) { run = null; continue; }
      if (!run || run.kind !== kind) runs.push((run = { kind, k0: k - 1, k1: k }));
      else run.k1 = k;
    }
    runs.forEach((run, i) => {
      const len = L[run.k1] - L[run.k0];
      const path = d(run.k0, run.k1);
      const reveal = { d: path, pathLength: r(len), 'stroke-dasharray': `${r(len)} ${r(len + 1)}`, 'stroke-dashoffset': r(len) };
      run.L0 = L[run.k0];
      run.len = len;
      if (run.kind === 'wire') {
        el('path', { d: path, class: 'j-u' }, under);
        run.el = el('path', { ...reveal, class: 'j-t' }, over);
      } else {
        // A dotted line cannot be revealed by its own dash pattern, so the
        // reveal runs on a solid path inside a mask over the dotted ink copy.
        const id = `j-mask-${i}`;
        const mask = el('mask', { id, maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: r(o.width), height: r(o.height) }, defs);
        run.el = el('path', { ...reveal, stroke: '#fff', 'stroke-width': 8 }, mask);
        el('path', { d: path, class: 'j-u-epi' }, under);
        el('path', { d: path, class: 'j-t-epi', mask: `url(#${id})` }, over);
      }
      run.v = len;
    });

    // Marks: a station plays once the dot reaches it, and its via (desktop)
    // or stub (rail) switches to the travelled colour.
    const marks = [];
    pts.forEach((p, k) => {
      if (!p.reach && !p.via && !p.stub) return;
      const lit = [];
      if (p.via) {
        el('circle', { cx: r(p.x), cy: r(p.y), r: 4, class: 'j-via j-u' }, under);
        lit.push(el('circle', { cx: r(p.x), cy: r(p.y), r: 4, class: 'j-via j-t j-lit' }, over));
      }
      if (p.stub) {
        const sd = `M${r(p.x)} ${r(p.y)}H${r(p.stub.x)}`;
        el('path', { d: sd, class: 'j-u' }, under);
        lit.push(el('path', { d: sd, class: 'j-t j-lit' }, over));
      }
      marks.push({ L: L[k], els: [].concat(p.reach || []), lit, on: null });
    });

    // Dividers the dot crosses are redrawn here, in the overlay, so the wave
    // can replace the line and the radio wavefront can sit on top of it: a
    // section's own border paints above the overlay. Same 2px ink, same place.
    const lines = el('g', {});
    for (const { host, dashed } of raw.divs || []) {
      const y = host.getBoundingClientRect().top - o.top + 1;
      el('path', { d: `M0 ${r(y)}H${r(o.width)}`, class: dashed ? 'j-divider j-dashed' : 'j-divider' }, lines);
      host.classList.add('j-div');
    }

    // The wave packet: three cycles of a sine under a cosine envelope, drawn
    // once at unit scale. The envelope meets the line with zero slope, so the
    // joint is smooth, without the long flat tails a squared envelope leaves.
    // On a crossing the dot opens into it and the line under it is cut away,
    // exactly as wide as the wave, so the line itself seems to turn into it.
    // Moved and morphed by transform and opacity alone.
    const wp = [];
    for (let i = 0; i <= 96; i++) {
      const u = (i / 96) * 2 - 1;
      const env = Math.cos((u * Math.PI) / 2);
      wp.push(`${i ? 'L' : 'M'}${r((u * WAVE_W) / 2)} ${r(-Math.sin(u * Math.PI * 3) * env * WAVE_A)}`);
    }
    const cut = el('rect', { x: r(-WAVE_W / 2), y: -3, width: WAVE_W, height: 6, class: 'j-cut' });
    const waveEl = el('path', { d: wp.join(''), class: 'j-wave' });
    // The radio wavefront: three concentric arcs opening along +x (flipped
    // by scale when the tower is to the left). It leaves the line, so the
    // dashed divider under it is not cut.
    const arcs = [6, 11, 16].map((R) => {
      const dy = r(R * Math.SQRT1_2);
      const dx = r(R * Math.SQRT1_2 - 8);
      return `M${dx} ${-dy}A${R} ${R} 0 0 1 ${dx} ${dy}`;
    });
    const radioEl = el('path', { d: arcs.join(''), class: 'j-wave j-radio' });
    const dot = el('circle', { r: 5, class: 'j-dot' });
    svg.setAttribute('viewBox', `0 0 ${r(o.width)} ${r(o.height)}`);
    svg.classList.toggle('j-rail', !desk);
    svg.replaceChildren(defs, under, over, lines, cut, waveEl, radioEl, dot);
    return { pts, L, S, mainEnd, runs, marks, dot, wave, waveEl, radioEl, cut, m: -1, kind: null };
  }

  // Scroll position → length along the trace. Reduced motion: the end, so
  // the whole trace is travelled and every station final.
  function lenAt(s) {
    const { L, S } = g;
    const n = L.length;
    if (mq.still.matches || s >= S[n - 1]) return L[n - 1];
    if (s <= S[0]) return 0;
    let lo = 0;
    let hi = n - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (S[m] <= s) lo = m; else hi = m; }
    return L[lo] + ((s - S[lo]) / (S[lo + 1] - S[lo])) * (L[lo + 1] - L[lo]);
  }

  function render() {
    if (!g) return;
    const { pts, L, mainEnd } = g;
    const len = lenAt(cur);
    let lo = 0;
    let hi = L.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (L[m] <= len) lo = m; else hi = m; }
    let k = lo;
    let t = L[k + 1] > L[k] ? Math.min((len - L[k]) / (L[k + 1] - L[k]), 1) : 1;

    // The dot stops at the chart; only the line carries on into the epilogue.
    if (k >= mainEnd) { k = mainEnd - 1; t = 1; }
    const a = pts[k];
    const b = pts[k + 1];
    const x = a.x + (b.x - a.x) * t;
    const y = a.y + (b.y - a.y) * t;
    // On a crossing, open into the wave or the radio wavefront away from the
    // corners: m runs 0 → 1 over WAVE_RAMP px after the start and back to 0
    // before the end.
    const w = g.wave[k];
    let m = 0;
    if (w) {
      const ramp = Math.min(WAVE_RAMP, (w.L1 - w.L0) / 3);
      const e = Math.min(Math.max(Math.min(len - w.L0, w.L1 - len) / ramp, 0), 1);
      m = e * e * (3 - 2 * e);
    }
    const kind = m ? w.kind : null;
    const at = `translate(${r(x)}px,${r(y)}px)`;
    g.dot.style.transform = m ? `${at} scale(${(1 - 0.6 * m).toFixed(3)})` : at;
    if (m !== g.m || kind !== g.kind) {
      const o = m.toFixed(3);
      g.dot.style.opacity = (1 - m).toFixed(3);
      g.waveEl.style.opacity = g.cut.style.opacity = kind === 'wave' ? o : 0;
      g.radioEl.style.opacity = kind === 'radio' ? o : 0;
      g.m = m;
      g.kind = kind;
    }
    if (kind === 'wave') {
      const sx = (0.15 + 0.85 * m).toFixed(3);
      g.waveEl.style.transform = `${at} scale(${sx},${m.toFixed(3)})`;
      g.cut.style.transform = `${at} scale(${sx},1)`;
    } else if (kind === 'radio') {
      const sc = 0.2 + 0.8 * m;
      g.radioEl.style.transform = `${at} scale(${(sc * w.dir).toFixed(3)},${sc.toFixed(3)})`;
    }

    for (const run of g.runs) {
      const v = r(run.len - Math.min(Math.max(len - run.L0, 0), run.len));
      if (v !== run.v) { run.v = v; run.el.style.strokeDashoffset = v; }
    }
    for (const m of g.marks) {
      const on = len >= m.L - 0.5;
      if (on === m.on) continue;
      m.on = on;
      for (const e of m.els) e.classList.toggle('is-reached', on);
      for (const e of m.lit) e.classList.toggle('is-on', on);
    }
  }

  // Runs only while the dot is catching up with the scroll position, then
  // stops: nothing animates while the reader is not scrolling.
  function tick(now) {
    const dt = last ? Math.min((now - last) / 1000, 0.05) : 1 / 60;
    last = now;
    cur += (target - cur) * (1 - Math.exp(-dt / TAU));
    if (Math.abs(target - cur) < 0.25) cur = target;
    render();
    if (cur !== target) raf = requestAnimationFrame(tick);
    else { raf = 0; last = 0; }
  }

  addEventListener('scroll', () => {
    target = scrollY;
    if (!g) return;
    if (mq.still.matches) { cur = target; render(); return; }
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });

  // Rebuild on anything that moves the layout: width, fonts, images. Mobile
  // browsers change the height as their toolbar slides; that is ignored so
  // the dot does not jump.
  new ResizeObserver(measureSoon).observe(root);
  addEventListener('resize', () => {
    if (innerWidth !== vw || (!mq.coarse.matches && innerHeight !== vh)) {
      vw = innerWidth;
      vh = innerHeight;
      measureSoon();
    }
  });
  if (document.fonts) document.fonts.ready.then(measureSoon);
  addEventListener('load', measureSoon);
  for (const q of [mq.desk, mq.rail, mq.still]) q.addEventListener('change', measureSoon);
  measure();

  // Desktop: device → (divider, gutter) → modem → … → analysis → chart, then
  // a dotted epilogue from the chart down the left gutter to the contact
  // outline beside the booking button.
  function routeDesktop(o) {
    const at = rel(o);
    const port = svgPort(o);
    const st = (name) => root.querySelector(`[data-station="${name}"]`);
    const top = (e) => e.getBoundingClientRect().top - o.top + 1;
    const land = root.querySelector('[data-j-land]');
    const fig = document.getElementById('keep-live');
    let prev = port('device-port-out');
    if (!prev || !land || !fig) return null;

    const divs = [];
    const pts = [];
    const go = (p, s, extra) => pts.push({ x: p.x, y: p.y, s, ...extra });
    go(prev, null, { via: true, reach: st('device') });
    for (const name of ORDER) {
      const pin = port(`${name}-port-in`);
      const pout = port(`${name}-port-out`);
      if (!pin || !pout) return null;
      const host = st(name).closest('[data-j-host]');
      const y = top(host);
      divs.push({ host, dashed: name === 'tower' });
      go({ x: prev.x, y }, 'wire');
      if (name === 'tower') {
        // The radio link: an interrupted run the dot crosses as a wavefront.
        const dir = Math.sign(pin.x - prev.x);
        go({ x: prev.x + dir * RADIO_STUB, y }, 'wire');
        go({ x: pin.x - dir * RADIO_STUB, y }, 'radio');
      }
      go({ x: pin.x, y }, 'wire');
      go(pin, 'wire', { via: true, reach: st(name) });
      go(pout, 'station', { via: true });
      prev = pout;
    }

    // Into The Keep: across to the end of the chart's line.
    const end = at(land);
    const ey = Math.max(end.y, prev.y + 3 * CHAMFER);
    go({ x: prev.x, y: ey }, 'wire');
    go({ x: end.x, y: ey }, 'wire');
    if (ey !== end.y) go(end, 'wire');
    Object.assign(pts[pts.length - 1], { end: true, reach: fig });

    // Epilogue: out of the chart's frame, down the right gutter, across on
    // the next divider and down the left gutter to the contact outline.
    const cin = port('contact-port-in');
    const svc = document.getElementById('services');
    if (cin && svc) {
      const f = fig.getBoundingClientRect();
      const fy = f.bottom - o.top - 28;
      const y = top(svc);
      const lane = cin.x - 24;
      go({ x: f.right - o.left, y: fy }, 'gap');
      go({ x: prev.x, y: fy }, 'epi');
      go({ x: prev.x, y }, 'epi');
      go({ x: lane, y }, 'epi');
      go({ x: lane, y: cin.y }, 'epi');
      go(cin, 'epi', { via: true, reach: st('contact') });
    }
    pts.divs = divs;
    return pts;
  }

  // Rail: one vertical line at the left edge. Strips hang off it on short
  // stubs; the dot only ever travels the rail. It starts at the hero device,
  // which on these widths sits below the headline and buttons.
  function routeRail(o) {
    const port = svgPort(o);
    const strip = (name) => root.querySelector(`[data-strip="${name}"]`);
    // A strip's port is its left-centre edge. A stub is drawn only when the
    // strip starts at the content edge: on wide tablets some sections are
    // still two columns, and a stub into the right one would cross text.
    const left = (e) => {
      const b = e && e.getBoundingClientRect();
      if (!b || !b.height) return null;
      const p = { x: b.left - o.left, y: b.top + b.height / 2 - o.top };
      return { ...p, stub: p.x < 64 ? p : null };
    };
    const dev = port('device-port-out');
    const hero = root.querySelector('[data-station="device"]');
    if (!dev || !hero) return null;

    const pts = [];
    const go = (p, s, extra) => pts.push({ x: p.x, y: p.y, s, ...extra });
    // Down out of the device, then left to the rail below everything else in
    // the hero, so the run never crosses the headline column beside it.
    const text = hero.closest('[data-j-host]').firstElementChild.getBoundingClientRect();
    const y0 = Math.max(dev.y, text.bottom - o.top) + 20;
    go(dev, null, { reach: hero });
    go({ x: dev.x, y: y0 }, 'wire');
    go({ x: RAIL_X, y: y0 }, 'wire');
    for (const name of ORDER) {
      const p = left(strip(name));
      if (!p) return null;
      go({ x: RAIL_X, y: p.y }, 'wire', { reach: strip(name), stub: p.stub });
    }
    // The dot stops level with the dashboard strip, above the chart.
    const fig = document.getElementById('keep-live');
    const d = left(strip('dashboard'));
    if (!d || !fig) return null;
    go({ x: RAIL_X, y: d.y }, 'wire', { end: true, reach: [strip('dashboard'), fig], stub: d.stub });

    const c = left(strip('contact'));
    if (c) {
      go({ x: RAIL_X, y: c.y }, 'epi');
      go(c, 'epi', { reach: strip('contact') });
    }
    return pts;
  }
}

// Ports are r=0 circles inside the station SVGs, which have no layout box of
// their own; map their centre through the SVG's transform instead.
function svgPort(o) {
  return (id) => {
    const c = document.getElementById(id);
    const m = c && c.getScreenCTM();
    if (!m) return null;
    const p = new DOMPoint(+c.getAttribute('cx'), +c.getAttribute('cy')).matrixTransform(m);
    return { x: p.x - o.left, y: p.y - o.top };
  };
}

// Centre of an element, in the journey container's coordinates.
function rel(o) {
  return (e) => {
    const b = e.getBoundingClientRect();
    return { x: b.left + b.width / 2 - o.left, y: b.top + b.height / 2 - o.top };
  };
}

// Cut every corner at 45°. A corner is replaced by two points; the flags of
// the original point travel with the second.
function chamfer(pts) {
  const out = [pts[0]];
  for (let i = 1; i < pts.length - 1; i++) {
    const a = pts[i - 1];
    const b = pts[i];
    const c = pts[i + 1];
    const l1 = dist(a, b);
    const l2 = dist(b, c);
    const u1 = { x: (b.x - a.x) / l1, y: (b.y - a.y) / l1 };
    const u2 = { x: (c.x - b.x) / l2, y: (c.y - b.y) / l2 };
    const straight = Math.abs(u1.x * u2.y - u1.y * u2.x) < 1e-3;
    if (b.s === 'gap' || c.s === 'gap' || !l1 || !l2 || straight) { out.push(b); continue; }
    const k = Math.min(CHAMFER, l1 / 2, l2 / 2);
    out.push({ x: b.x - u1.x * k, y: b.y - u1.y * k, s: b.s });
    out.push({ ...b, x: b.x + u2.x * k, y: b.y + u2.y * k });
  }
  out.push(pts[pts.length - 1]);
  return out;
}

function dist(a, b) {
  return Math.hypot(b.x - a.x, b.y - a.y);
}

function r(v) {
  return Math.round(v * 10) / 10;
}
