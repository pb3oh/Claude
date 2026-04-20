(() => {
  const nav = document.querySelector('[data-nav]');
  const burger = document.querySelector('[data-burger]');
  const body = document.body;

  // Scrolled nav state
  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile sheet
  if (burger) {
    // Build sheet once
    const links = document.querySelector('.nav__links');
    const cta = document.querySelector('.nav__cta');
    const sheet = document.createElement('div');
    sheet.className = 'nav__sheet';
    if (links) sheet.innerHTML += links.innerHTML;
    if (cta)   sheet.innerHTML += cta.innerHTML;
    nav.appendChild(sheet);

    burger.addEventListener('click', () => {
      const open = body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      sheet.style.display = open ? 'flex' : 'none';
    });

    // Close when clicking a link
    sheet.addEventListener('click', (e) => {
      if (e.target.closest('a')) {
        body.classList.remove('nav-open');
        sheet.style.display = 'none';
      }
    });
  }

  // Reveal on scroll
  const items = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && items.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    items.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 40, 240)}ms`;
      io.observe(el);
    });
  } else {
    items.forEach((el) => el.classList.add('is-in'));
  }

  // Year
  document.querySelectorAll('[data-year]').forEach((n) => {
    n.textContent = new Date().getFullYear();
  });

  // Quote form demo handler (no backend)
  document.querySelectorAll('[data-quote-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const note = form.querySelector('.submit small');
      if (note) note.textContent = "Thanks — we'll be in touch within one business day.";
      form.reset();
    });
  });

  // Simple smooth scroll for same-page anchors
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href').slice(1);
      if (!id) return;
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();
