const menuButton = document.querySelector(".menu-button");
const mobileMenu = document.querySelector(".mobile-menu");

function setMenu(open) {
  if (!menuButton || !mobileMenu) return;
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  mobileMenu.hidden = !open;
  document.body.classList.toggle("menu-open", open);
}

menuButton?.addEventListener("click", () => {
  setMenu(menuButton.getAttribute("aria-expanded") !== "true");
});

mobileMenu?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setMenu(false));
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setMenu(false);
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 940) setMenu(false);
});

// A lightweight, dependency-free synapse field for the hero. It pauses outside
// the viewport, caps pixel density, and becomes static when reduced motion is
// requested.
(() => {
  const canvas = document.querySelector("#synapse-canvas");
  const stage = canvas?.closest(".synapse-stage");
  const context = canvas?.getContext("2d");
  if (!canvas || !stage || !context) return;
  const interactionSurface = stage.closest(".hero") || stage;

  let seed = 397;
  const random = () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  };

  function zoneFor(x, y) {
    const column = Math.min(2, Math.floor((x + 1) * 1.5));
    return (column + (y > 0 ? 3 : 0)) % 5;
  }

  const points = [];
  const edges = [];

  function addPoint(x, y, z) {
    points.push({
      x,
      y,
      z,
      size: 0.45 + random() * 0.9,
      accent: random() > 0.94,
      zone: zoneFor(x, y),
    });
  }

  const pointTarget = 1280;
  while (points.length < pointTarget) {
    addPoint(random() * 2 - 1, random() * 2 - 1, random() * 0.62 - 0.31);
  }

  const degree = new Uint8Array(points.length);
  for (const [from, to] of edges) {
    degree[from] += 1;
    degree[to] += 1;
  }
  // A higher local degree makes the network read as densely connected
  // synapses while the radius keeps the lines visually local.
  const maximumDegree = 10;
  const connectionRadius = 0.165;
  for (let i = 0; i < points.length; i += 1) {
    const candidates = [];
    for (let j = i + 1; j < points.length; j += 1) {
      const dx = points[i].x - points[j].x;
      const dy = points[i].y - points[j].y;
      const dz = points[i].z - points[j].z;
      const distance = Math.hypot(dx, dy, dz);
      if (distance < connectionRadius) candidates.push([distance, j]);
    }
    candidates.sort((a, b) => a[0] - b[0]);
    for (const [, j] of candidates) {
      if (degree[i] >= maximumDegree) break;
      if (degree[j] >= maximumDegree) continue;
      edges.push([i, j]);
      degree[i] += 1;
      degree[j] += 1;
    }
  }

  let width = 0;
  let height = 0;
  let frame = 0;
  let visible = true;
  let lastPaint = 0;
  const pointer = { active: false, x: 0, y: 0 };
  const pastel = [
    [244, 164, 194],
    [145, 213, 230],
    [181, 224, 166],
    [250, 196, 148],
    [190, 174, 235],
  ];
  const motionQuery = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)")
    : { matches: false };

  function resize() {
    const bounds = stage.getBoundingClientRect();
    width = Math.max(1, Math.round(bounds.width));
    height = Math.max(1, Math.round(bounds.height));
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    paint(performance.now(), true);
  }

  function project(point, time) {
    const rotation = motionQuery.matches ? 0 : Math.sin(time * 0.00016) * 0.055;
    const depth = point.z + point.x * rotation;
    const x = width * 0.5 + (point.x + point.z * rotation) * width * 0.52;
    const y = height * 0.5 + (point.y + point.z * 0.035) * height * 0.52;
    const radius = Math.max(92, Math.min(165, width * 0.145));
    const hoverDistance = Math.hypot(x - pointer.x, y - pointer.y);
    const glow = pointer.active ? Math.max(0, 1 - hoverDistance / radius) ** 1.7 : 0;
    return {
      x,
      y,
      z: depth,
      size: point.size * (0.9 + (depth + 0.35) * 0.35),
      accent: point.accent,
      glow,
      zone: point.zone,
    };
  }

  function paint(time, force = false) {
    if (!force && time - lastPaint < 32) {
      frame = requestAnimationFrame(paint);
      return;
    }
    lastPaint = time;
    context.clearRect(0, 0, width, height);
    const projected = points.map((point) => project(point, time));

    context.shadowBlur = 0;
    context.lineWidth = 0.68;
    for (const [fromIndex, toIndex] of edges) {
      const from = projected[fromIndex];
      const to = projected[toIndex];
      const [red, green, blue] = pastel[from.zone];
      const opacity = Math.max(0.2, Math.min(0.38, 0.28 + (from.z + to.z) * 0.09));
      context.strokeStyle = `rgba(${red}, ${green}, ${blue}, ${opacity})`;
      context.beginPath();
      context.moveTo(from.x, from.y);
      context.lineTo(to.x, to.y);
      context.stroke();
    }

    // Redraw only the activated local network with a pastel halo.
    for (const [fromIndex, toIndex] of edges) {
      const from = projected[fromIndex];
      const to = projected[toIndex];
      const glow = Math.max(from.glow, to.glow);
      if (glow < 0.02) continue;
      const source = from.glow >= to.glow ? from : to;
      const [red, green, blue] = pastel[source.zone];
      context.lineWidth = 0.8 + glow * 2.2;
      context.shadowBlur = 5 + glow * 16;
      context.shadowColor = `rgb(${red}, ${green}, ${blue})`;
      context.strokeStyle = `rgba(${red}, ${green}, ${blue}, ${0.2 + glow * 0.78})`;
      context.beginPath();
      context.moveTo(from.x, from.y);
      context.lineTo(to.x, to.y);
      context.stroke();
    }

    context.shadowBlur = 0;
    const depthSorted = [...projected].sort((a, b) => a.z - b.z);
    for (const point of depthSorted) {
      const opacity = Math.max(0.68, Math.min(0.96, 0.8 + point.z * 0.35));
      context.fillStyle = point.accent
        ? `rgba(36, 88, 211, ${opacity})`
        : `rgba(20, 22, 27, ${opacity})`;
      context.beginPath();
      context.arc(point.x, point.y, point.size, 0, Math.PI * 2);
      context.fill();
    }

    for (const point of depthSorted) {
      if (point.glow < 0.02) continue;
      const [red, green, blue] = pastel[point.zone];
      context.shadowBlur = 8 + point.glow * 20;
      context.shadowColor = `rgb(${red}, ${green}, ${blue})`;
      context.fillStyle = `rgba(${red}, ${green}, ${blue}, ${0.45 + point.glow * 0.55})`;
      context.beginPath();
      context.arc(point.x, point.y, point.size + 1 + point.glow * 2.4, 0, Math.PI * 2);
      context.fill();
    }
    context.shadowBlur = 0;

    if (!motionQuery.matches && visible && !document.hidden) {
      frame = requestAnimationFrame(paint);
    }
  }

  function updateAnimation() {
    cancelAnimationFrame(frame);
    frame = 0;
    if (visible && !document.hidden && !motionQuery.matches) {
      frame = requestAnimationFrame(paint);
    } else {
      paint(performance.now(), true);
    }
  }

  function updatePointer(event) {
    const bounds = stage.getBoundingClientRect();
    pointer.x = event.clientX - bounds.left;
    pointer.y = event.clientY - bounds.top;
    pointer.active = true;
    if (motionQuery.matches) paint(performance.now(), true);
  }

  function clearPointer() {
    pointer.active = false;
    if (motionQuery.matches) paint(performance.now(), true);
  }

  interactionSurface.addEventListener("pointermove", updatePointer, { passive: true });
  interactionSurface.addEventListener("pointerleave", clearPointer, { passive: true });

  if ("ResizeObserver" in window) {
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(stage);
  } else {
    window.addEventListener("resize", resize, { passive: true });
  }

  if ("IntersectionObserver" in window) {
    const intersectionObserver = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      updateAnimation();
    }, { rootMargin: "80px" });
    intersectionObserver.observe(stage);
  } else {
    updateAnimation();
  }

  document.addEventListener("visibilitychange", updateAnimation);
  motionQuery.addEventListener?.("change", updateAnimation);
  resize();
})();

// Register the public, read-only catalog with browsers that expose WebMCP.
// The feature is progressive enhancement; ordinary browsers ignore it.
(() => {
  const models = [
    {
      name: "Qwen3.6 35B A3B — Abliterated",
      repository: "huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated",
      apiModelId: "huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated",
      priceUsdPerHour: 5.45,
    },
    {
      name: "Ornith 1.0 35B — Abliterated",
      repository: "YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated",
      apiModelId: "YuYu1015/YuYu1015-Ornith-1.0-35B-abliterated",
      priceUsdPerHour: 5.45,
    },
    {
      name: "Qwythos 9B Claude Mythos 5 — Abliterated",
      repository: "huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated",
      apiModelId: "huihui-ai/Huihui-Qwythos-9B-Claude-Mythos-5-1M-abliterated",
      priceUsdPerHour: 2.34,
    },
    {
      name: "Ornith 1.0 397B W4A16 — Abliterated",
      repository: "cebeuq/Ornith-1.0-397B-abliterated-W4A16",
      apiModelId: "cebeuq/Ornith-1.0-397B-abliterated-W4A16",
      priceUsdPerHour: 10.9,
    },
  ];
  const registeredContexts = new WeakSet();

  function toolResult(value) {
    return {
      content: [{ type: "text", text: JSON.stringify(value, null, 2) }],
      structuredContent: value,
    };
  }

  const tools = [
    {
      name: "get_site_summary",
      description: "Explain ABLITERATED.cloud and its current private-beta status.",
      inputSchema: { type: "object", properties: {} },
      execute: async () => toolResult({
        name: "ABLITERATED.cloud",
        summary: "Token-protected, OpenAI-compatible managed access to exact abliterated Hugging Face models.",
        access: "Private beta through Signal",
        billingLive: false,
      }),
    },
    {
      name: "list_models",
      description: "List the four exact Hugging Face repositories, status and managed price.",
      inputSchema: { type: "object", properties: {} },
      execute: async () => toolResult({ models }),
    },
    {
      name: "read_public_documentation",
      description: "Read the complete public ABLITERATED.cloud documentation as text.",
      inputSchema: { type: "object", properties: {} },
      execute: async () => {
        const response = await fetch("llms-full.txt", { headers: { accept: "text/plain" } });
        const text = await response.text();
        return { content: [{ type: "text", text }], structuredContent: { text } };
      },
    },
  ];

  window.__webmcp_tools = tools;

  function registerTools() {
    const context = navigator.modelContext || document.modelContext || window.modelContext;
    if (!context || registeredContexts.has(context)) return Boolean(context);
    const registerTool = context.registerTool || context.register;
    if (typeof registerTool !== "function") return false;

    for (const tool of tools) {
      try {
        registerTool.call(context, tool);
      } catch (error) {
        const message = String(error?.message || error || "");
        if (!/already|duplicate|registered/i.test(message)) {
          console.warn("ABLITERATED.cloud WebMCP registration failed", tool.name, error);
        }
      }
    }
    registeredContexts.add(context);
    window.__abliteratedWebMcpRegistered = true;
    return true;
  }

  let attempts = 0;
  function registerWhenReady() {
    if (registerTools() || attempts >= 30) return;
    attempts += 1;
    window.setTimeout(registerWhenReady, 100);
  }

  registerWhenReady();
  document.addEventListener("DOMContentLoaded", registerWhenReady, { once: true });
  window.addEventListener("load", registerWhenReady, { once: true });
})();
