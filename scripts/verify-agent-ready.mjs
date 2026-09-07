// Verify real static Pages surfaces; do not invent live inference/agent services.
import assert from "node:assert/strict";

const base = (process.argv.slice(2).find((x) => !x.startsWith("--")) || "http://localhost:8788").replace(/\/$/, "");
async function read(path, json = false) {
  const response = await fetch(`${base}${path}`, { signal: AbortSignal.timeout(15000) });
  assert.equal(response.status, 200, `${path}: HTTP ${response.status}`);
  return json ? response.json() : response.text();
}

const [html, status, schema, posts, llms, full, sitemap, feed] = await Promise.all([
  read("/"), read("/.well-known/project-status.json", true), read("/openapi.json", true),
  read("/blog/posts.json", true), read("/llms.txt"), read("/llms-full.txt"),
  read("/sitemap.xml"), read("/blog/feed.xml"),
]);
assert.equal(status.live_polling, false);
assert.equal(status.public_inference, false);
assert.equal(schema["x-public-inference"], false);
assert.equal(schema["x-public-mcp"], false);
assert.ok(html.includes(status.snapshot_at.slice(0, 10)));
assert.ok(!/<canvas|<script[^>]+src=/i.test(html));
assert.ok(!html.includes("hero-brain"));
const css = await read("/styles.css");
assert.ok(!/hero-brain|@import|url\(https?:/i.test(css));
for (const [path, methods] of Object.entries(schema.paths)) {
  assert.deepEqual(Object.keys(methods), ["get"]);
  await read(path);
}
assert.equal(new Set(posts.map((p) => p.slug)).size, posts.length);
for (const post of posts) {
  assert.equal(post.content_status, "editorial_archive");
  const route = `/blog/${post.slug}/`;
  const [article, markdown] = await Promise.all([read(route), read(`${route}index.md`)]);
  assert.ok(article.includes("Model research, dated at publication") && markdown.includes("Model research, dated at publication"), route);
  assert.ok(article.includes("https://signal.me/#p/+13103408213") && markdown.includes("https://signal.me/#p/+13103408213"), route);
  assert.ok(article.includes("Primary sources") && markdown.includes("Primary sources"), route);
  for (const index of [llms, full, sitemap, feed]) assert.ok(index.includes(route), route);
}
await Promise.all(["/auth.md", "/NOTICE.md", "/robots.txt", "/skills/abliterated-cloud/SKILL.md", "/releases/website-v0.12.0.md"].map((p) => read(p)));
for (const path of ["/app.js", "/.well-known/agent-card.json", "/.well-known/mcp/server-card.json", "/.well-known/oauth-authorization-server", "/.well-known/webmcp.json"]) {
  const response = await fetch(`${base}${path}`, { signal: AbortSignal.timeout(15000) });
  assert.equal(response.status, 404, `${path}: retired surface must return 404`);
}
const rates = status.current.running_quote_usd_per_hour;
for (const cost of [rates.total * 720, rates.gpu * 60 + rates.disk * 720]) {
  assert.ok(html.includes(`$${cost.toFixed(2)}`), "running-cost scenarios missing");
}
assert.ok(/<h1[^>]*>Intelligence, freed\.<\/h1>/.test(html), "preserve the approved headline");
assert.ok(html.includes("https://signal.me/#p/+13103408213"), "Signal service contact missing");
const catalog = await read("/.well-known/ai-catalog.json", true);
assert.equal(catalog.specVersion, "1.0");
assert.ok(catalog.entries.length > 0);
console.log(JSON.stringify({target:base, result:"passed", model_articles:posts.length, public_inference:false, live_status_polling:false, scope:"Service website and read-only discovery; no GPU or inference requests"}, null, 2));
