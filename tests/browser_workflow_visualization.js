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

  const pageUrl = `file://${path.resolve(__dirname, "../docs/visualizations/standard-workflow.html")}`;
  const indexUrl = `file://${path.resolve(__dirname, "../docs/index.html")}`;

  await call("Page.enable");
  await call("Network.enable");
  await call("Network.setCacheDisabled", { cacheDisabled: true });
  await call("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  await call("Page.navigate", { url: pageUrl });
  await delay(350);

  let value = await evaluate(`document.title.includes('main · 分支 · tmp')`);
  assert(value, "page has the expected title");
  value = await evaluate(`Array.from(document.querySelectorAll('section')).map(section => section.id).join(',') === 'directories,tmp,readme,value'`);
  assert(value, "page has the four intended sections");
  value = await evaluate(`Array.from(document.querySelectorAll('h2')).every(heading => heading.getBoundingClientRect().width > 0 && heading.getBoundingClientRect().height > 0)`);
  assert(value, "all section headings are rendered");
  value = await evaluate(`document.documentElement.scrollWidth <= document.documentElement.clientWidth`);
  assert(value, "desktop page has no horizontal overflow");
  value = await evaluate(`document.getAnimations({ subtree: true }).length === 0`);
  assert(value, "page has no motion animations competing with content");
  value = await evaluate(`(() => {
    const intersects = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    const cards = Array.from(document.querySelectorAll('.grid > .card')).map(card => card.getBoundingClientRect());
    return cards.every((card, index) => cards.slice(index + 1).every(other => !intersects(card, other)));
  })()`);
  assert(value, "directory cards do not overlap");
  value = await evaluate(`Array.from(document.querySelectorAll('.card, .check, .zoom-step')).every(el => {
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0 && rect.left >= 0 && rect.right <= document.documentElement.clientWidth;
  })`);
  assert(value, "desktop content remains within the viewport");
  value = await evaluate(`document.querySelector('.directory-tree').scrollWidth <= document.querySelector('.directory-tree').clientWidth + 1 || getComputedStyle(document.querySelector('.directory-tree')).overflowX === 'auto'`);
  assert(value, "directory tree is readable or horizontally scrollable");

  await call("Page.navigate", { url: indexUrl });
  await delay(500);
  value = await evaluate(`document.title.includes('main · 分支 · tmp')`);
  assert(value, "docs root redirects to the workflow page");

  await call("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await call("Page.navigate", { url: pageUrl });
  await delay(350);
  value = await evaluate(`document.documentElement.scrollWidth <= document.documentElement.clientWidth`);
  assert(value, "mobile page has no horizontal overflow");
  value = await evaluate(`getComputedStyle(document.querySelector('.grid')).gridTemplateColumns.split(' ').length === 1`);
  assert(value, "mobile directory cards stack in one column");
  value = await evaluate(`Array.from(document.querySelectorAll('h1,h2,h3,p,li,td')).every(el => parseFloat(getComputedStyle(el).fontSize) >= 12)`);
  assert(value, "mobile text stays at a readable size");
  value = await evaluate(`(() => {
    const tree = document.querySelector('.directory-tree');
    tree.scrollLeft = 24;
    return tree.scrollLeft === 24 || tree.scrollWidth <= tree.clientWidth;
  })()`);
  assert(value, "mobile directory tree is accessible without clipping content");
  value = await evaluate(`Array.from(document.querySelectorAll('.card, .check, .zoom-step')).every(el => el.getBoundingClientRect().right <= document.documentElement.clientWidth + 1)`);
  assert(value, "mobile content remains within the viewport");

  socket.close();
  process.exit(0);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
