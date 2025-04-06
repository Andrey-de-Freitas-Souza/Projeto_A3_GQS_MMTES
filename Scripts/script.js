const sidebar = document.getElementById('sidebar');
const hamburgerIcon = document.getElementById('hamburger-icon');

let menuAberto = false;

hamburgerIcon.addEventListener('click', () => {
  menuAberto = !menuAberto;

  if (menuAberto) {
    sidebar.classList.add('translate-x-0');
    sidebar.classList.remove('-translate-x-full');
  } else {
    sidebar.classList.remove('translate-x-0');
    sidebar.classList.add('-translate-x-full');
  }
});

// Fecha o menu ao clicar fora
document.addEventListener('click', (event) => {
  const isClickInsideSidebar = sidebar.contains(event.target);
  const isClickOnHamburger = hamburgerIcon.contains(event.target);

  if (!isClickInsideSidebar && !isClickOnHamburger && menuAberto) {
    sidebar.classList.remove('translate-x-0');
    sidebar.classList.add('-translate-x-full');
    menuAberto = false;
  }
});