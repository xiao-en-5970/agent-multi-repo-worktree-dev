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
  await call("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  await call("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
  await call("Page.navigate", { url: `file://${path.resolve(__dirname, "../docs/visualizations/standard-workflow.html")}` });
  await delay(500);

  let value = await evaluate(`Array.from(document.querySelectorAll('svg')).every(svg => !svg.animationsPaused())`);
  assert(value, "default SMIL animations run");
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
