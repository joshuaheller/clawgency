'use strict';

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

// NAV: SCROLL EFFECT & MOBILE MENU
(function initNav() {
  const nav = $('#nav');
  const burger = $('#navBurger');

  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  burger?.addEventListener('click', () => {
    nav.classList.toggle('mobile-open');
    burger.setAttribute('aria-label',
      nav.classList.contains('mobile-open') ? 'Menü schließen' : 'Menü öffnen'
    );
  });

  $$('.nav__mobile .nav__link, .nav__mobile .btn').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('mobile-open');
    });
  });
})();

// SMOOTH SCROLL
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

// REVEAL ON SCROLL
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

// COUNTER ANIMATION
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

// AGENT TABS
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
    tabs.forEach((t, i) => t.classList.toggle('agents__tab--active', i === index));

    vizItems.forEach((v, i) => {
      v.classList.toggle('agent-viz--active', i === index);
      if (i === index) {
        const lines = $$('.agent-viz__line', v);
        lines.forEach(l => {
          l.style.animation = 'none';
          l.offsetHeight;
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

    infoItems.forEach((info, i) => info.classList.toggle('agent-info--active', i === index));

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

  let currentAgent = 0;
  let autoTimer = setInterval(() => {
    currentAgent = (currentAgent + 1) % tabs.length;
    switchAgent(currentAgent);
  }, 5000);

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => {
      clearInterval(autoTimer);
      currentAgent = i;
      autoTimer = setInterval(() => {
        currentAgent = (currentAgent + 1) % tabs.length;
        switchAgent(currentAgent);
      }, 5000);
    });
  });
})();

// FAQ ACCORDION
(function initFAQ() {
  const items = $$('.faq__item');

  items.forEach(item => {
    const question = $('.faq__question', item);
    question?.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      items.forEach(i => {
        i.classList.remove('open');
        $('.faq__question', i)?.setAttribute('aria-expanded', 'false');
      });

      if (!isOpen) {
        item.classList.add('open');
        question.setAttribute('aria-expanded', 'true');
      }
    });
  });
})();

// CONTACT FORM – opens email app with pre-filled content
(function initContactForm() {
  const form = $('#contactForm');
  if (!form) return;

  const EMAIL_TO = 'clawgency@theaisoftwarecompany.com';

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = (form.querySelector('#name')?.value || '').trim();
    const company = (form.querySelector('#company')?.value || '').trim();
    const email = (form.querySelector('#email')?.value || '').trim();
    const challenge = (form.querySelector('#challenge')?.value || '').trim();

    if (!name || !company || !email) {
      const btn = form.querySelector('button[type="submit"]');
      const orig = btn.innerHTML;
      btn.innerHTML = '<span class="btn__icon">🦀</span> Bitte alle Pflichtfelder ausfüllen';
      btn.disabled = true;
      setTimeout(() => {
        btn.innerHTML = orig;
        btn.disabled = false;
      }, 2000);
      return;
    }

    const subject = encodeURIComponent(`Kontaktanfrage von ${name} (${company})`);
    const bodyLines = [
      `Name: ${name}`,
      `Unternehmen: ${company}`,
      `E-Mail: ${email}`,
      challenge ? `\nGrößte Herausforderung:\n${challenge}` : ''
    ].filter(Boolean);
    const body = encodeURIComponent(bodyLines.join('\n'));

    const mailto = `mailto:${EMAIL_TO}?subject=${subject}&body=${body}`;
    window.location.href = mailto;
  });
})();

// HERO GRID PARALLAX
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

// CURSOR GLOW EFFECT (desktop only)
(function initCursorGlow() {
  if (window.matchMedia('(hover: none)').matches) return;

  const glow = document.createElement('div');
  glow.style.cssText = `
    position: fixed;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(230,57,70,0.06) 0%, transparent 70%);
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

// ACTIVE NAV LINK HIGHLIGHT
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

// STAGGER CHILDREN ANIMATION
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

// MARQUEE PAUSE ON HOVER
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

// LAZY-LOAD CTA VIDEO
(function initLazyVideos() {
  const videos = $$('video[preload="none"]');
  if (!videos.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const video = entry.target;
      const sources = $$('source[data-src]', video);
      sources.forEach(s => {
        s.src = s.dataset.src;
        s.removeAttribute('data-src');
      });
      if (sources.length) video.load();
      video.play().catch(() => {});
      observer.unobserve(video);
    });
  }, { rootMargin: '200px' });

  videos.forEach(v => observer.observe(v));
})();

console.log('%cClawgency 🦀', 'color: #e63946; font-size: 1.5rem; font-weight: bold;');
console.log('%cKI-Agenten für den DACH-Mittelstand', 'color: #8892a4;');
