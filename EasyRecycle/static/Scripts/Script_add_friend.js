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

function toggleSolicitacoes() {
    const lista = document.getElementById("lista-solicitacoes");
    const seta = document.getElementById("seta");

    if (lista.style.display === "none") {
        lista.style.display = "block";
        seta.innerHTML = "&#9650;"; // seta para cima
    } else {
        lista.style.display = "none";
        seta.innerHTML = "&#9660;"; // seta para baixo
    }
}

function toggleAmigos() {
  const lista = document.getElementById("lista-amigos");
  const seta = document.getElementById("seta2");

  if (lista.style.display === "none") {
      lista.style.display = "block";
      seta.innerHTML = "&#9650;"; // seta para cima
  } else {
      lista.style.display = "none";
      seta.innerHTML = "&#9660;"; // seta para baixo
  }
}

window.onload = function() {
  var img = document.getElementById('Profile');

  // Função que será chamada se a imagem falhar ao carregar
  img.onerror = function() {
    this.src = "{{ url_for('static', filename='Images/Profile.jpg') }}";
  };
};

document.addEventListener("DOMContentLoaded", function() {
  // Lógica para o botão aceitar
  document.querySelectorAll(".btn-aceitar").forEach(button => {
    button.addEventListener("click", function() {
      const conviteId = this.closest(".botoes-amizade").getAttribute("data-id");

      // Envia para o backend para aceitar o convite
      fetch("/amizade/aceitar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          convite_id: conviteId
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          alert("Convite aceito com sucesso!");
        } else {
          alert(data.message);
        }
      });
    });
  });

  // Lógica para o botão recusar
  document.querySelectorAll(".btn-recusar").forEach(button => {
    button.addEventListener("click", function() {
      const conviteId = this.closest(".botoes-amizade").getAttribute("data-id");

      // Envia para o backend para recusar o convite
      fetch("/amizade/recusar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          convite_id: conviteId
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          alert("Convite recusado com sucesso!");
        } else {
          alert(data.message);
        }
      });
    });
  });

  // Lógica para o botão remover (mesma rota de recusar)
  document.querySelectorAll(".btn-remover").forEach(button => {
    button.addEventListener("click", function() {
      const amizadeId = this.closest(".botoes-amizade").getAttribute("data-id");

      // Envia para o backend para remover o amigo
      fetch("/amizade/recusar", {  // Reutilizando a rota de recusar
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          convite_id: amizadeId
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          alert("Amigo removido com sucesso!");
          // Você pode adicionar lógica para remover o item da tela, por exemplo
        } else {
          alert(data.message);
        }
      });
    });
  });
});




