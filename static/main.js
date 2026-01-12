// Mobile sidebar toggle + accessibility
const hamburger = document.getElementById("hamburger");
const sidebar = document.getElementById("sidebar");

if (hamburger && sidebar) {
  const updateAria = (open) => {
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
    sidebar.setAttribute('aria-hidden', open ? 'false' : 'true');
  };

  hamburger.addEventListener('click', (e) => {
    const isOpen = sidebar.classList.toggle('open');
    updateAria(isOpen);
    if (isOpen) {
      // save previously focused element and focus first item in sidebar
      sidebar.__previouslyFocused = document.activeElement;
      const focusable = sidebar.querySelectorAll('a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])');
      if (focusable.length) focusable[0].focus();
      document.addEventListener('keydown', trapTab);
    } else {
      // restore focus
      if (sidebar.__previouslyFocused) sidebar.__previouslyFocused.focus();
      document.removeEventListener('keydown', trapTab);
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      updateAria(false);
      if (sidebar.__previouslyFocused) sidebar.__previouslyFocused.focus();
      document.removeEventListener('keydown', trapTab);
    }
  });

  // Click outside to close
  document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !hamburger.contains(e.target) && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      updateAria(false);
    }
  });
}

// Tab-trapping handler for sidebar when open
function trapTab(e) {
  if (e.key !== 'Tab' || !sidebar.classList.contains('open')) return;
  const focusable = Array.from(sidebar.querySelectorAll('a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])'));
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (e.shiftKey) {
    if (document.activeElement === first) {
      e.preventDefault();
      last.focus();
    }
  } else {
    if (document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
}

// Animate skill bars when they enter the viewport
const skillFills = document.querySelectorAll('.skill-fill[data-width]');
if (skillFills.length) {
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const w = el.getAttribute('data-width');
        if (w) el.style.width = w;
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.25 });

  skillFills.forEach(el => observer.observe(el));
}
