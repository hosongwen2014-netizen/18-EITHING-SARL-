const header = document.querySelector('.site-header');
const toggle = document.querySelector('.nav-toggle');

if (toggle) {
  toggle.addEventListener('click', () => {
    const isOpen = header.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
}

const links = document.querySelectorAll('.main-nav a, .footer-wrap a');
links.forEach((link) => {
  link.addEventListener('click', () => {
    if (header) {
      header.classList.remove('nav-open');
    }
    if (toggle) {
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
});
