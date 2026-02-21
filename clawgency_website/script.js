/* ============================================================
   CLAWGENCY – SCRIPT.JS
   Animations, Interactions, Scroll Effects
============================================================ */

'use strict';

// ── UTILITY ──────────────────────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

// ── NAV: SCROLL EFFECT & MOBILE MENU ─────────────────────────
(function initNav() {
  const nav = $('#nav');
  const burger = $('#navBurger');

  // Scroll class
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile burger
  burger?.addEventListener('click', () => {
    nav.classList.toggle('mobile-open');
    burger.setAttribute('aria-label',
      nav.classList.contains('mobile-open') ? 'Menü schließen' : 'Menü öffnen'
    );
  });

  // Close mobile menu on link click
  $$('.nav__mobile .nav__link, .nav__mobile .btn').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('mobile-open');
    });
  });
})();

// ── SMOOTH SCROLL FOR ANCHOR LINKS ───────────────────────────
(function initSmoothScroll() {
  $$('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = $(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const navHeight = $('#nav')?.offsetHeight || 80;
      const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 20;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
})();

// ── REVEAL ON SCROLL ─────────────────────────────────────────
(function initReveal() {
  const revealEls = $$('.reveal');
  if (!revealEls.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  revealEls.forEach(el => observer.observe(el));
})();

// ── COUNTER ANIMATION ─────────────────────────────────────────
(function initCounters() {
  const counters = $$('[data-target]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.target, 10);
      let current = 0;
      const step = Math.ceil(target / 40);
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current;
        if (current >= target) clearInterval(timer);
      }, 30);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
})();

// ── AGENT TABS ────────────────────────────────────────────────
(function initAgentTabs() {
  const tabs = $$('.agents__tab');
  const vizItems = $$('.agent-viz');
  const infoItems = $$('.agent-info');
  const headlineText = $('#agentTypeText');

  const agentLabels = [
    'Ihren Kundenservice',
    'Ihre Betriebsprozesse',
    'Ihren Vertrieb',
    'Ihre Buchhaltung',
    'Ihr HR-Team'
  ];

  function switchAgent(index) {
    // Update tabs
    tabs.forEach((t, i) => t.classList.toggle('agents__tab--active', i === index));

    // Update visuals
    vizItems.forEach((v, i) => {
      v.classList.toggle('agent-viz--active', i === index);
      // Re-trigger animations by removing and re-adding class
      if (i === index) {
        const lines = $$('.agent-viz__line', v);
        lines.forEach(l => {
          l.style.animation = 'none';
          l.offsetHeight; // reflow
          l.style.animation = '';
        });
        const cursor = $('.agent-viz__cursor', v);
        if (cursor) {
          cursor.style.opacity = '0';
          cursor.style.animation = 'none';
          cursor.offsetHeight;
          cursor.style.opacity = '';
          cursor.style.animation = '';
        }
      }
    });

    // Update info panels
    infoItems.forEach((info, i) => info.classList.toggle('agent-info--active', i === index));

    // Update headline
    if (headlineText) {
      headlineText.style.opacity = '0';
      headlineText.style.transform = 'translateY(8px)';
      setTimeout(() => {
        headlineText.textContent = agentLabels[index];
        headlineText.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        headlineText.style.opacity = '1';
        headlineText.style.transform = 'translateY(0)';
      }, 150);
    }
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => switchAgent(i));
  });

  // Auto-cycle every 5 seconds
  let currentAgent = 0;
  let autoTimer = setInterval(() => {
    currentAgent = (currentAgent + 1) % tabs.length;
    switchAgent(currentAgent);
  }, 5000);

  // Pause auto-cycle on manual interaction
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => {
      clearInterval(autoTimer);
      currentAgent = i;
      // Restart after 10 seconds of inactivity
      autoTimer = setInterval(() => {
        currentAgent = (currentAgent + 1) % tabs.length;
        switchAgent(currentAgent);
      }, 5000);
    });
  });
})();

// ── FAQ ACCORDION ─────────────────────────────────────────────
(function initFAQ() {
  const items = $$('.faq__item');

  items.forEach(item => {
    const question = $('.faq__question', item);
    question?.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all
      items.forEach(i => {
        i.classList.remove('open');
        $('.faq__question', i)?.setAttribute('aria-expanded', 'false');
      });

      // Open clicked (if it wasn't open)
      if (!isOpen) {
        item.classList.add('open');
        question.setAttribute('aria-expanded', 'true');
      }
    });
  });
})();

// ── CONTACT FORM ──────────────────────────────────────────────
(function initContactForm() {
  const form = $('#contactForm');
  const success = $('#formSuccess');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="btn__icon">⏳</span> Wird gesendet…';
    btn.disabled = true;

    // Simulate form submission (replace with real endpoint)
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Show success
    form.style.display = 'none';
    success.style.display = 'block';

    // Reset after 8 seconds
    setTimeout(() => {
      form.reset();
      form.style.display = 'flex';
      success.style.display = 'none';
      btn.innerHTML = originalText;
      btn.disabled = false;
    }, 8000);
  });
})();

// ── HERO GRID PARALLAX ────────────────────────────────────────
(function initParallax() {
  const grid = $('.hero__grid');
  if (!grid) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        grid.style.transform = `translateY(${scrollY * 0.15}px)`;
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
})();

// ── CURSOR GLOW EFFECT ────────────────────────────────────────
(function initCursorGlow() {
  // Only on non-touch devices
  if (window.matchMedia('(hover: none)').matches) return;

  const glow = document.createElement('div');
  glow.style.cssText = `
    position: fixed;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    transform: translate(-50%, -50%);
    transition: opacity 0.3s ease;
    opacity: 0;
  `;
  document.body.appendChild(glow);

  let mouseX = 0, mouseY = 0;
  let glowX = 0, glowY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    glow.style.opacity = '1';
  });

  document.addEventListener('mouseleave', () => {
    glow.style.opacity = '0';
  });

  function animateGlow() {
    glowX += (mouseX - glowX) * 0.08;
    glowY += (mouseY - glowY) * 0.08;
    glow.style.left = glowX + 'px';
    glow.style.top = glowY + 'px';
    requestAnimationFrame(animateGlow);
  }
  animateGlow();
})();

// ── ACTIVE NAV LINK HIGHLIGHT ─────────────────────────────────
(function initActiveNav() {
  const sections = $$('section[id]');
  const navLinks = $$('.nav__link');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          const href = link.getAttribute('href');
          link.style.color = href === `#${id}` ? 'var(--c-white)' : '';
        });
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(s => observer.observe(s));
})();

// ── STAGGER CHILDREN ANIMATION ────────────────────────────────
(function initStagger() {
  const staggerParents = $$('.results__grid, .process__steps');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const children = [...entry.target.children].filter(c => c.classList.contains('reveal'));
      children.forEach((child, i) => {
        setTimeout(() => child.classList.add('visible'), i * 120);
      });
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.1 });

  staggerParents.forEach(p => observer.observe(p));
})();

// ── MARQUEE PAUSE ON HOVER ────────────────────────────────────
(function initMarqueePause() {
  const track = $('.marquee__track');
  if (!track) return;

  const wrap = $('.marquee-wrap');
  wrap?.addEventListener('mouseenter', () => {
    track.style.animationPlayState = 'paused';
  });
  wrap?.addEventListener('mouseleave', () => {
    track.style.animationPlayState = 'running';
  });
})();

// ── INIT LOG ──────────────────────────────────────────────────
console.log('%cClawgency ⚡', 'color: #00e5ff; font-size: 1.5rem; font-weight: bold;');
console.log('%cKI-Agenten für den DACH-Mittelstand', 'color: #8892a4;');
