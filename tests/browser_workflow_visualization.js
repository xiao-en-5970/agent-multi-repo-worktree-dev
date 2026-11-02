// Optional real-browser check. Start Chrome with --remote-debugging-port=9222,
// then run `node tests/browser_workflow_visualization.js`.
// This does not run during the standard-library suite or CI.
const http = require("http");

const path = require("path");

function get(pathname) {
  return new Promise((resolve, reject) => http.get({ host: "127.0.0.1", port: 9222, path: pathname }, (response) => {
    let body = "";
    response.on("data", (chunk) => { body += chunk; });
    response.on("end", () => resolve(JSON.parse(body)));
  }).on("error", reject));
}

function connect(url) {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket(url);
    socket.onopen = () => resolve(socket);
    socket.onerror = reject;
  });
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

(async () => {
  const pages = await get("/json/list");
  const socket = await connect(pages.find((page) => page.type === "page").webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const handlers = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) handlers.reject(message.error);
    else handlers.resolve(message.result);
  };
  function call(method, params = {}) {
    return new Promise((resolve, reject) => {
      const key = ++id;
      pending.set(key, { resolve, reject });
      socket.send(JSON.stringify({ id: key, method, params }));
    });
  }
  async function evaluate(expression) {
    const response = await call("Runtime.evaluate", { expression, returnByValue: true });
    if (response.exceptionDetails) throw new Error(JSON.stringify(response.exceptionDetails));
    return response.result.value;
  }
  function assert(value, message) {
    if (!value) throw new Error(message);
    console.log("PASS", message);
  }

  await call("Page.enable");
  await call("Network.enable");
  await call("Network.setCacheDisabled", { cacheDisabled: true });
  await call("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  await call("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
  await call("Page.navigate", { url: `file://${path.resolve(__dirname, "../docs/visualizations/standard-workflow.html")}` });
  await delay(500);

  let value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => !svg.animationsPaused())`);
  assert(value, "default SMIL animations run");
  value = await evaluate(`(() => {
    const scene = document.querySelector('header.hero > svg');
    const lineY = scene.querySelector('path').getBoundingClientRect().y;
    const label = Array.from(scene.querySelectorAll('text')).find(el => el.textContent === '统一基座').getBoundingClientRect();
    return lineY < label.top || lineY > label.bottom;
  })()`);
  assert(value, "hero connector stays outside primary-checkout label");
  value = await evaluate(`(() => {
    const intersects = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    const scene = document.querySelector('header.hero > svg');
    const note = Array.from(scene.querySelectorAll('text')).find(el => el.textContent === '同一基线，不同工作现场').getBoundingClientRect();
    return Array.from(scene.querySelectorAll('rect')).every(el => !intersects(note, el.getBoundingClientRect()));
  })()`);
  assert(value, "hero note stays in separate whitespace");
  value = await evaluate(`(() => {
    const intersects = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    const scene = document.querySelector('#boundary svg');
    const cards = Array.from(scene.querySelectorAll(':scope > g > rect'));
    return cards.every((card, index) => cards.slice(index + 1).every(other => !intersects(card.getBoundingClientRect(), other.getBoundingClientRect())));
  })()`);
  assert(value, "boundary cards do not overlap");
  value = await evaluate(`(() => {
    const scene = document.querySelector('#preflight svg');
    const path = Array.from(scene.querySelectorAll('path')).find(el => el.getAttribute('d') === 'M205 180h100M395 180h100M585 180h100M775 180h100');
    const strokeWidth = Number(getComputedStyle(path).strokeWidth);
    const ctm = path.getScreenCTM();
    const intersects = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    const labels = Array.from(scene.querySelectorAll('text')).map(el => el.getBoundingClientRect());
    return Array.from({ length: 101 }, (_, index) => {
      const point = path.getPointAtLength(path.getTotalLength() * index / 100).matrixTransform(ctm);
      const box = { left: point.x - strokeWidth / 2 - 2, right: point.x + strokeWidth / 2 + 2, top: point.y - strokeWidth / 2 - 2, bottom: point.y + strokeWidth / 2 + 2 };
      return labels.every(label => !intersects(box, label));
    }).every(Boolean);
  })()`);
  assert(value, "segmented preflight connector strokes avoid every checkpoint label");
  value = await evaluate(`(() => {
    const scene = document.querySelector('#preflight svg');
    const check = scene.querySelector('path[d="M900 70l15 15 28-32"]');
    if (!check) return false;
    const point = check.getPointAtLength(check.getTotalLength() * 0.9).matrixTransform(check.getScreenCTM());
    const label = Array.from(scene.querySelectorAll('text')).find(el => el.textContent.includes('重复键')).getBoundingClientRect();
    const strokeWidth = Number(getComputedStyle(check).strokeWidth);
    return point.x < label.left || point.x > label.right || point.y - strokeWidth / 2 > label.bottom || point.y + strokeWidth / 2 < label.top;
  })()`);
  assert(value, "preflight checkmark does not cross warning text");
  await delay(3600);
  value = await evaluate(`(() => {
    const scene = document.querySelector('header.hero > svg');
    const lineY = scene.querySelector('path').getBoundingClientRect().y;
    const label = Array.from(scene.querySelectorAll('text')).find(el => el.textContent === '统一基座').getBoundingClientRect();
    return lineY < label.top || lineY > label.bottom;
  })()`);
  assert(value, "hero connector remains outside label at a later animation phase");
  value = await evaluate(`(() => {
    const card = document.querySelector('#handoff svg > g > rect').getBoundingClientRect();
    const indicator = document.querySelector('#handoff svg > g.pulse > circle').getBoundingClientRect();
    return indicator.right < card.left || indicator.left > card.right || indicator.bottom < card.top || indicator.top > card.bottom;
  })()`);
  assert(value, "handoff status indicator stays outside document frame");
  await evaluate(`document.getElementById('motion-toggle').click()`);
  value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => svg.animationsPaused()) && document.body.classList.contains('paused')`);
  assert(value, "pause stops SMIL and CSS");
  await evaluate(`document.getElementById('motion-toggle').click()`);
  value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => !svg.animationsPaused()) && !document.body.classList.contains('paused')`);
  assert(value, "resume restarts SMIL and CSS");
  await call("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
  await delay(100);
  value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => svg.animationsPaused()) && document.getElementById('motion-toggle').getAttribute('aria-pressed') === 'true'`);
  assert(value, "live reduced-motion pauses SMIL");
  await call("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
  await delay(100);
  value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => !svg.animationsPaused())`);
  assert(value, "live preference removal resumes SMIL");
  await call("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
  await call("Page.reload");
  await delay(400);
  value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => svg.animationsPaused())`);
  assert(value, "initial reduced-motion pauses SMIL");
  await call("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  value = await evaluate(`Array.from(document.querySelectorAll('.diagram')).every(el => el.scrollWidth <= el.clientWidth || getComputedStyle(el).overflowX === 'auto')`);
  assert(value, "mobile diagrams accessible by horizontal scroll");
  value = await evaluate(`(() => { const el = document.querySelector('.diagram'); el.scrollLeft = 100; return el.scrollLeft === 100; })()`);
  assert(value, "mobile diagram supports actual horizontal scroll movement");
  value = await evaluate(`document.documentElement.scrollWidth <= document.documentElement.clientWidth`);
  assert(value, "no page-level horizontal overflow");
  value = await evaluate(`getComputedStyle(document.querySelector('.diagram svg')).width`);
  assert(value === "800px", `mobile diagram width: ${value}`);
  socket.close();
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
