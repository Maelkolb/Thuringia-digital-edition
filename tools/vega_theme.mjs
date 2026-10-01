// Shared Vega config for every chart in the edition (light + dark).
// Categorical slots: reference palette validated against the edition's paper
// surface #fbf8f1 (light) and #1d1b18 (dark) with the dataviz validator:
// all checks pass (adjacent CVD dE >= 9.1 light / 8.4 dark). Three light slots
// sit below 3:1 contrast -> charts always ship a data table (relief rule).
export const PALETTE = {
  light: ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948'],
  dark: ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9', '#e66767'],
};
const BLUES = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6', '#256abf', '#1c5cab', '#184f95', '#104281', '#0d366b'];
const DIVERGING = ['#104281', '#2a78d6', '#86b6ef', '#f0efec', '#f19a99', '#e34948', '#a8282a'];
const DIVERGING_DARK = ['#86b6ef', '#3987e5', '#1c5cab', '#383835', '#b13b3b', '#e66767', '#f2a7a7'];

export function theme(mode = 'light') {
  const dark = mode === 'dark';
  const ink2 = dark ? '#c3c2b7' : '#52514e';
  const muted = '#898781';
  const grid = dark ? '#2c2c2a' : '#e8e3d8';
  const axis = dark ? '#383835' : '#c9c2b2';
  const font = '"Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif';
  return {
    background: null,
    font,
    padding: 4,
    autosize: { type: 'fit-x', contains: 'padding' },
    view: { stroke: null, continuousHeight: 300 },
    title: { color: dark ? '#ffffff' : '#0b0b0b', font, fontSize: 14, fontWeight: 600, anchor: 'start', offset: 10 },
    axis: {
      labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font,
      labelFontSize: 11, titleFontSize: 12, titleFontWeight: 500,
      gridColor: grid, gridWidth: 1, domainColor: axis, tickColor: axis, tickSize: 4,
      labelPadding: 4, titlePadding: 8,
    },
    axisX: { grid: false },
    axisY: { grid: true, domain: false, ticks: false },
    axisBand: { grid: false },
    legend: {
      labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font, labelFontSize: 11, titleFontSize: 11,
      orient: 'top', direction: 'horizontal', symbolType: 'circle', symbolSize: 80, columnPadding: 14, titlePadding: 6,
    },
    header: { labelColor: ink2, titleColor: ink2, labelFont: font, titleFont: font, labelFontSize: 12 },
    range: {
      category: dark ? PALETTE.dark : PALETTE.light,
      ordinal: BLUES.slice(3, 12),
      ramp: dark ? BLUES.slice(2).reverse() : BLUES,
      heatmap: dark ? BLUES.slice(2).reverse() : BLUES,
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
    text: { color: ink2, font, fontSize: 11 },
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
