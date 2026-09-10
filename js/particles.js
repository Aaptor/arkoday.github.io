/**
 * Lightweight, high-performance background particle constellation.
 * Zero dependencies (< 3KB), 60 FPS, battery-friendly, auto-adapts to light/dark themes.
 */
(function () {
  "use strict";

  // Check prefers-reduced-motion
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Configuration
  var isMobile = window.innerWidth < 768;
  var PARTICLE_COUNT = isMobile ? 24 : 46;
  var MAX_DISTANCE = isMobile ? 90 : 130;
  var MOUSE_RADIUS = 130;

  // Theme palettes [violet, cyan, indigo]
  var THEMES = {
    light: {
      particles: [
        { r: 124, g: 58, b: 237 },  // Electric Violet
        { r: 2, g: 132, b: 199 },   // Azure Cyan
        { r: 79, g: 70, b: 229 }    // Indigo
      ],
      particleAlpha: 0.45,
      lineAlpha: 0.14,
      glowAlpha: 0.28
    },
    dark: {
      particles: [
        { r: 215, g: 220, b: 232 },  // Crisp silvery starlight
        { r: 170, g: 178, b: 198 },  // Monochromatic slate
        { r: 195, g: 200, b: 218 }   // Soft luminous zinc
      ],
      particleAlpha: 0.50,
      lineAlpha: 0.15,
      glowAlpha: 0.30
    }
  };

  function getCurrentTheme() {
    var themeAttr = document.documentElement.getAttribute("data-theme");
    if (themeAttr === "dark") return "dark";
    if (themeAttr === "light") return "light";
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  // Create or attach canvas
  var canvas = document.getElementById("particle-canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.id = "particle-canvas";
    canvas.className = "particle-canvas";
    canvas.setAttribute("aria-hidden", "true");
    document.body.prepend(canvas);
  }

  var ctx = canvas.getContext("2d");
  if (!ctx) return;

  var width = 0;
  var height = 0;
  var dpr = 1;
  var particles = [];
  var animationFrameId = null;
  var isRunning = true;
  var mouse = { x: -9999, y: -9999, active: false };

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Adjust particle count on resize
    var nowMobile = width < 768;
    var targetCount = nowMobile ? 24 : 46;
    MAX_DISTANCE = nowMobile ? 90 : 130;
    while (particles.length < targetCount) {
      particles.push(createParticle(Math.random() * width, Math.random() * height));
    }
    if (particles.length > targetCount) {
      particles.length = targetCount;
    }
  }

  function createParticle(x, y) {
    var angle = Math.random() * Math.PI * 2;
    var speed = 0.18 + Math.random() * 0.32; // gentle, relaxing drift
    return {
      x: x !== undefined ? x : Math.random() * width,
      y: y !== undefined ? y : Math.random() * height,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      radius: 1.3 + Math.random() * 1.8,
      colorIndex: Math.floor(Math.random() * 3),
      pulseSpeed: 0.015 + Math.random() * 0.02,
      pulseOffset: Math.random() * Math.PI * 2,
      hasGlow: Math.random() < 0.35
    };
  }

  function initParticles() {
    particles = [];
    for (var i = 0; i < PARTICLE_COUNT; i++) {
      particles.push(createParticle());
    }
  }

  // Mouse interaction
  window.addEventListener("mousemove", function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  }, { passive: true });

  window.addEventListener("mouseleave", function () {
    mouse.active = false;
    mouse.x = -9999;
    mouse.y = -9999;
  }, { passive: true });

  // Pause when tab is not visible to preserve battery
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      isRunning = false;
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    } else {
      if (!isRunning) {
        isRunning = true;
        lastTime = performance.now();
        tick(lastTime);
      }
    }
  });

  var lastTime = performance.now();

  function tick(now) {
    if (!isRunning) return;

    var dt = Math.min((now - lastTime) / 1000, 0.1);
    lastTime = now;

    var themeKey = getCurrentTheme();
    var theme = THEMES[themeKey];

    ctx.clearRect(0, 0, width, height);

    var len = particles.length;

    // Update positions
    for (var i = 0; i < len; i++) {
      var p = particles[i];

      if (!prefersReducedMotion) {
        p.x += p.vx * dt * 60;
        p.y += p.vy * dt * 60;

        // Gentle organic wave
        p.y += Math.sin(now * 0.0012 + p.pulseOffset) * 0.12;

        // Interactive mouse repulsion/flow
        if (mouse.active) {
          var dx = p.x - mouse.x;
          var dy = p.y - mouse.y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < MOUSE_RADIUS && dist > 0) {
            var force = (1 - dist / MOUSE_RADIUS) * 0.85;
            p.x += (dx / dist) * force;
            p.y += (dy / dist) * force;
          }
        }

        // Screen wrapping with smooth margin
        var pad = 24;
        if (p.x < -pad) p.x = width + pad;
        if (p.x > width + pad) p.x = -pad;
        if (p.y < -pad) p.y = height + pad;
        if (p.y > height + pad) p.y = -pad;
      }
    }

    // Draw connecting lines between close particles
    for (var i = 0; i < len; i++) {
      var p1 = particles[i];
      var c1 = theme.particles[p1.colorIndex];

      // Connect to mouse if active and close
      if (mouse.active && !prefersReducedMotion) {
        var mdx = p1.x - mouse.x;
        var mdy = p1.y - mouse.y;
        var mdist = Math.sqrt(mdx * mdx + mdy * mdy);
        if (mdist < MOUSE_RADIUS) {
          var mAlpha = (1 - mdist / MOUSE_RADIUS) * theme.lineAlpha * 1.6;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = "rgba(" + c1.r + "," + c1.g + "," + c1.b + "," + mAlpha + ")";
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }

      for (var j = i + 1; j < len; j++) {
        var p2 = particles[j];
        var dx = p1.x - p2.x;
        var dy = p1.y - p2.y;
        var dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < MAX_DISTANCE) {
          var lineAlpha = (1 - dist / MAX_DISTANCE) * theme.lineAlpha;
          var c2 = theme.particles[p2.colorIndex];
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = "rgba(" + Math.round((c1.r + c2.r) / 2) + "," +
                                      Math.round((c1.g + c2.g) / 2) + "," +
                                      Math.round((c1.b + c2.b) / 2) + "," +
                                      lineAlpha + ")";
          ctx.lineWidth = 0.85;
          ctx.stroke();
        }
      }
    }

    // Draw particles
    for (var i = 0; i < len; i++) {
      var p = particles[i];
      var c = theme.particles[p.colorIndex];
      var alpha = theme.particleAlpha;

      // Subtle pulse
      var pulse = Math.sin(now * 0.002 * p.pulseSpeed * 100 + p.pulseOffset);
      var currentRadius = p.radius + pulse * 0.35;
      if (currentRadius < 0.8) currentRadius = 0.8;

      ctx.beginPath();
      ctx.arc(p.x, p.y, currentRadius, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(" + c.r + "," + c.g + "," + c.b + "," + alpha + ")";

      if (p.hasGlow) {
        ctx.shadowBlur = 8;
        ctx.shadowColor = "rgba(" + c.r + "," + c.g + "," + c.b + "," + theme.glowAlpha + ")";
      } else {
        ctx.shadowBlur = 0;
      }

      ctx.fill();
    }
    ctx.shadowBlur = 0;

    if (!prefersReducedMotion) {
      animationFrameId = requestAnimationFrame(tick);
    }
  }

  // Initialize
  window.addEventListener("resize", function () {
    resize();
  }, { passive: true });

  resize();
  initParticles();
  lastTime = performance.now();
  tick(lastTime);
})();
