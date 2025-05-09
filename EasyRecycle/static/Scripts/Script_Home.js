document.addEventListener("DOMContentLoaded", function () {
  const profileImg = document.getElementById("Profile");
  
  profileImg.addEventListener("error", function () {
      this.src = "{{ url_for('static', filename='Images/Profile.jpg') }}";
  });
});

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

document.addEventListener('DOMContentLoaded', function() {
  const itemSelect = document.getElementById('categorySelect');

  fetch('/get-itens')
    .then(response => response.json())
    .then(data => {
      data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        itemSelect.appendChild(option);
      });
    })
    .catch(error => console.error('Erro ao carregar categorias:', error));
});

document.addEventListener('DOMContentLoaded', function() {
  const itemSelect = document.getElementById('categorySelect');

  fetch('/get-itens')
    .then(response => response.json())
    .then(data => {
      data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        itemSelect.appendChild(option);
      });

      // Ativa o Tom Select
      new TomSelect("#categorySelect", {
        placeholder: "Selecione um item...",
        persist: false,
        create: false,
        onFocus: function() {
          this.input.placeholder = '';
        },
        onBlur: function() {
          if (this.getValue() === '') {
            this.input.placeholder = 'Selecione um item...';
          }
        }
      });
    })
    .catch(error => console.error('Erro ao carregar itens:', error));
});

fetch('/get-collection-points')
  .then(response => response.json())
  .then(data => {
    const selectCollection = document.getElementById('collection_point');
    data.forEach(point => {
      const option = document.createElement('option');
      option.value = point.id;
      option.text = point.name;
      selectCollection.appendChild(option);
    });

    // Inicializar o TomSelect depois que carregar os dados
    new TomSelect("#collection_point", {
      placeholder: "Selecione um ponto de coleta...",
      persist: false,
      create: false,
      onFocus: function() {
        this.input.placeholder = '';
      },
      onBlur: function() {
        if (this.getValue() === '') {
          this.input.placeholder = 'Selecione um ponto de coleta...';
        }
      }
    });
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

 

  document.querySelectorAll('.category-header').forEach(header => {
    header.style.backgroundColor = header.getAttribute('data-color');
  });


  sessionStorage.clear();
  localStorage.clear();

  // Impede voltar para páginas anteriores
  window.history.pushState(null, "", window.location.href);
  window.onpopstate = function () {
    window.history.pushState(null, "", window.location.href);
  };

  // Força recarregamento se o usuário tentar voltar
  window.addEventListener("pageshow", function (event) {
    if (event.persisted || window.performance.getEntriesByType("navigation")[0].type === "back_forward") {
      location.reload(); // força recarregar para evitar acesso à página protegida via cache
    }
  });

  


  document.getElementById('formCadastro').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o reload da página
  
    const category = document.getElementById('categorySelect').value;
    let collection_point = document.getElementById('collection_point').value;
    const peso = document.getElementById('peso').value;
    const errorMessage = document.getElementById('error-message'); // O <p> onde será exibida a mensagem de erro
    console.log(collection_point)
    // Limpa a mensagem de erro ao tentar submeter
    errorMessage.textContent = '';
  
    // Verifica se category e peso foram preenchidos corretamente
    if (!category || category === "id" || !peso || isNaN(peso) || Number(peso) <= 0) {
      errorMessage.textContent = 'Por favor, preencha os campos obrigatórios corretamente (matéria e peso).';
      errorMessage.style.color = 'red';
      return;
    }
  
    // Se collection_point não for preenchido corretamente, define como 0
    if (!collection_point || collection_point === "id") {
      collection_point = 1;
    }
    console.log(collection_point)
    // Envia os dados
    fetch('/cadastrar-reciclagem', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ category, collection_point, peso })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Mensagem de sucesso ou erro
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  });
