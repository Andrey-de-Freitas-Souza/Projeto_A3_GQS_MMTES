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

  document.getElementById('formCadastro').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o reload da página
  
    const category = document.getElementById('categorySelect').value;
    const collection_point = document.getElementById('collection_point').value;
    const peso = document.getElementById('peso').value;
  
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
