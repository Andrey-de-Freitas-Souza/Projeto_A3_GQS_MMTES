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

const sidebar_direito = document.getElementById('sidebar_direito');
const hamburgerIcon_direito = document.getElementById('Profile');

let menu_direito_Aberto = false;

hamburgerIcon_direito.addEventListener('click', () => {
  menu_direito_Aberto = !menu_direito_Aberto;

  if (menu_direito_Aberto) {
    sidebar_direito.classList.add('translate-x-0');
    sidebar_direito.classList.remove('translate-x-full');
  } else {
    sidebar_direito.classList.remove('translate-x-0');
    sidebar_direito.classList.add('translate-x-full');
  }
});

// Fecha o menu ao clicar fora
document.addEventListener('click', (event) => {
  const isClickInsideSidebar = sidebar_direito.contains(event.target);
  const isClickOnHamburger = hamburgerIcon_direito.contains(event.target);

  if (!isClickInsideSidebar && !isClickOnHamburger && menu_direito_Aberto) {
    sidebar_direito.classList.remove('translate-x-0');
    sidebar_direito.classList.add('translate-x-full');
    menu_direito_Aberto = false;
  }
});


const btnAdicionar = document.getElementById('btnAdicionar');
const fecharModal = document.getElementById('fecharModal');
const modalOverlay = document.getElementById('modalOverlay');
const modal = document.querySelector('.modal');

btnAdicionar.addEventListener('click', function() {
  modalOverlay.style.display = 'flex';
  modal.style.animation = 'slideUp 0.4s forwards'; // Garante a animação
});

fecharModal.addEventListener('click', function() {
  modalOverlay.style.display = 'none';
});

modalOverlay.addEventListener('click', function(event) {
  if (event.target === modalOverlay) {
    modalOverlay.style.display = 'none';
  }
});

document.getElementById('fecharModal').addEventListener('click', function() {
const popOut = document.getElementById('pop_out');
const overlay = document.getElementById('overlay');

popOut.style.transition = "bottom 0.5s ease";
popOut.style.bottom = "-100%";

setTimeout(() => {
    overlay.style.display = 'none';
    popOut.style.display = 'none';
}, 500);
});

async function enviarConvite(event) {
    // Impede o envio do formulário
    event.preventDefault();

    const email = document.getElementById('email').value;

    if (!email) {
        alert("Por favor, preencha um e-mail.");
        return;
    }

    const resposta = await fetch('/verificar-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    });

    const resultado = await resposta.json();
    

    if (resultado.existe) {
        // Exibe o pop-up de sucesso ou erro com base na resposta da API
        alert(resultado.mensagem);
    } else {
        // Caso o e-mail não esteja cadastrado, exibe a mensagem de erro
        alert(resultado.mensagem);
    }
}






  