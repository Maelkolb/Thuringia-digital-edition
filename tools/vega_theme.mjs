// Shared Vega config for every chart in the edition (light + dark).
// Categorical slots are ink and pigment hues (Prussian blue, rust, verdigris, plum, olive, indigo, ochre, crimson),
// validated with the dataviz validator against the paper #fbf8f1 and the dark ground #1d1b18:
// lightness band, chroma floor, adjacent CVD separation >= 8.7, normal-vision floor >= 15 and 3:1 contrast all pass.
export const PALETTE = {
  light: ['#2f6aa6', '#c0582c', '#278a6c', '#8e4f9a', '#6a7f1c', '#3a4f8f', '#b07d0c', '#b8393f'],
  dark: ['#5288c8', '#d06a36', '#36a07f', '#a46cb2', '#86993a', '#6e7fc8', '#b88b22', '#d4566a'],
};
const BLUES = ['#e6edf4', '#c7d7e8', '#a8c1db', '#8aabce', '#6d95c1', '#4f7fb4', '#2f6aa6', '#295e94', '#235282', '#1e4671', '#183b60', '#133050', '#0e2540'];
const BLUES_DARK = ['#dbe6f2', '#bcd1e9', '#9ebce0', '#80a7d7', '#6192cd', '#4c7eb9', '#3f6a9c', '#345680', '#284466', '#1d324c'];
const DIVERGING = ['#17365c', '#2f6aa6', '#9db8d3', '#ece6db', '#e3a99a', '#b8393f', '#6e1c22'];
const DIVERGING_DARK = ['#a9c3df', '#5288c8', '#2a4d78', '#3a3630', '#7a2a2f', '#d4566a', '#efaab2'];

// Colour tokens usable in specs ("@accent", "@context" ...): replaced per light/dark mode at compile time,
// so highlight-and-context designs keep working in dark mode.
export const TOKENS = {
  light: { ink: '#1e1b17', ink2: '#4a443b', muted: '#8a8274', context: '#cbc2b1', accent: PALETTE.light[0], accent2: PALETTE.light[1], accent3: PALETTE.light[2],
    paper: '#fbf8f1', land: '#e4dccb', river: '#8eacc8', positive: PALETTE.light[0], negative: PALETTE.light[7] },
  dark: { ink: '#ede6d8', ink2: '#cdc4b4', muted: '#9c9382', context: '#4f4a42', accent: PALETTE.dark[0], accent2: PALETTE.dark[1], accent3: PALETTE.dark[2],
    paper: '#1d1b18', land: '#3a352e', river: '#3d6386', positive: PALETTE.dark[0], negative: PALETTE.dark[7] },
};

export function applyTokens(node, mode = 'light') {
  const t = TOKENS[mode === 'dark' ? 'dark' : 'light'];
  if (Array.isArray(node)) return node.map((n) => applyTokens(n, mode));
  if (node && typeof node === 'object') {
    const o = {};
    for (const [k, v] of Object.entries(node)) o[k] = applyTokens(v, mode);
    return o;
  }
  if (typeof node === 'string' && /^@[a-z0-9]+$/.test(node) && t[node.slice(1)]) return t[node.slice(1)];
  return node;
}

export function theme(mode = 'light') {
  const dark = mode === 'dark';
  const tk = TOKENS[dark ? 'dark' : 'light'];
  const ink2 = tk.ink2;
  const muted = tk.muted;
  const grid = dark ? '#2e2a25' : '#ebe5d9';
  const axis = dark ? '#4a443b' : '#c9c0ae';
  const font = '"Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif';
  return {
    background: null,
    font,
    padding: 4,
    autosize: { type: 'fit-x', contains: 'padding' },
    view: { stroke: null, continuousHeight: 300 },
    title: { color: tk.ink, font, fontSize: 14, fontWeight: 600, anchor: 'start', offset: 10 },
    axis: {
      labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font,
      labelFontSize: 12, titleFontSize: 12, titleFontWeight: 500,
      gridColor: grid, gridWidth: 1, domainColor: axis, tickColor: axis, tickSize: 4,
      labelPadding: 4, titlePadding: 8,
    },
    axisX: { grid: false },
    axisY: { grid: true, domain: false, ticks: false },
    axisBand: { grid: false },
    legend: {
      labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font, labelFontSize: 12, titleFontSize: 12,
      orient: 'top', direction: 'horizontal', symbolType: 'circle', symbolSize: 80, columnPadding: 14, titlePadding: 6, labelLimit: 240,
    },
    header: { labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font, labelFontSize: 12 },
    range: {
      category: dark ? PALETTE.dark : PALETTE.light,
      ordinal: dark ? BLUES_DARK.slice(1, 9).reverse() : BLUES.slice(3, 12),
      ramp: dark ? BLUES_DARK.slice().reverse() : BLUES,
      heatmap: dark ? BLUES_DARK.slice().reverse() : BLUES,
      diverging: dark ? DIVERGING_DARK : DIVERGING,
    },
    line: { strokeWidth: 2, strokeCap: 'round', strokeJoin: 'round' },
    point: { size: 64, filled: true, strokeWidth: 2, stroke: dark ? '#1d1b18' : '#fbf8f1' },
    circle: { size: 64, strokeWidth: 2, stroke: dark ? '#1d1b18' : '#fbf8f1' },
    bar: { cornerRadiusEnd: 3, stroke: dark ? '#1d1b18' : '#fbf8f1', strokeWidth: 1 },
    area: { opacity: 0.25, line: true },
    rect: { stroke: dark ? '#1d1b18' : '#fbf8f1', strokeWidth: 1 },
    arc: { stroke: dark ? '#1d1b18' : '#fbf8f1', strokeWidth: 1.5 },
    rule: { color: muted },
    text: { color: ink2, font, fontSize: 12 },
    geoshape: { stroke: dark ? '#1d1b18' : '#fbf8f1', strokeWidth: 0.5 },
    style: {
      annotation: { fontSize: 12, fill: ink2, font },
      label: { fontSize: 12, fill: ink2, font, fontWeight: 600 },
      'label-muted': { fontSize: 12, fill: muted, font },
      'place-halo': { fontSize: 12, fill: dark ? '#1d1b18' : '#fbf8f1', font, fontWeight: 600, stroke: dark ? '#1d1b18' : '#fbf8f1', strokeWidth: 3.5, strokeJoin: 'round', opacity: 0.9 },
      'place-label': { fontSize: 12, fill: dark ? '#ede6d8' : '#1e1b17', font, fontWeight: 600 },
    },
    mark: { color: dark ? PALETTE.dark[0] : PALETTE.light[0] },
  };
}

// faceted / concatenated / repeated views cannot use autosize "fit"; they keep their own sizes
export function isComposite(spec) {
  if (!spec || typeof spec !== 'object') return false;
  if (spec.facet || spec.hconcat || spec.vconcat || spec.concat || spec.repeat) return true;
  const enc = spec.encoding || {};
  if (enc.row || enc.column || enc.facet) return true;
  return Array.isArray(spec.layer) && spec.layer.some((l) => l.encoding && (l.encoding.row || l.encoding.column || l.encoding.facet));
}
