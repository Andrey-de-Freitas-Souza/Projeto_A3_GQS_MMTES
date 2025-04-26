const formContainer = document.getElementById('form-container');
const loginForm = document.getElementById('login-form');
const cadastroForm = document.getElementById('cadastro-form');
const cadastreSe = document.getElementById('cadastre-se');
const voltarLogin = document.getElementById('voltar-login');

cadastreSe.addEventListener('click', () => {
  // Move a caixa para o centro
  formContainer.style.right = '50%';
  formContainer.style.transform = 'translate(50%, -50%)';
  formContainer.style.borderRadius = '10px'
  formContainer.style.width = '50%';

  // Alterna o conteúdo
  loginForm.classList.remove('active');
  cadastroForm.classList.add('active');
});

voltarLogin.addEventListener('click', () => {
  // Volta a caixa para a direita
  formContainer.style.right = '0';
  formContainer.style.transform = 'translateY(-50%)';
  formContainer.style.borderRadius = '10px 0px 0px 10px';
  formContainer.style.width = '40%';

  // Alterna o conteúdo
  cadastroForm.classList.remove('active');
  loginForm.classList.add('active');
});

// ---- Scripts de máscaras Telefone e CEP ----
// Função para aplicar a máscara de telefone conforme o DDI selecionado
function mascaraTelefone(event) {
    let input = event.target;
    let valor = input.value;
  
    // Obter o DDI selecionado
    let ddi = document.getElementById('ddi').value;
  
    // Remove tudo que não é número
    valor = valor.replace(/\D/g, '');
  
    // Aplica a máscara dependendo do DDI selecionado
    if (ddi === '+55') { // Brasil
      if (valor.length <= 2) {
        valor = '(' + valor;
      } else if (valor.length <= 6) {
        valor = '(' + valor.slice(0, 2) + ') ' + valor.slice(2);
      } else if (valor.length <= 10) {
        valor = '(' + valor.slice(0, 2) + ') ' + valor.slice(2, 7) + '-' + valor.slice(7);
      } else {
        valor = '(' + valor.slice(0, 2) + ') ' + valor.slice(2, 7) + '-' + valor.slice(7, 11);
      }
    } else if (ddi === '+1') { // Estados Unidos
      if (valor.length <= 3) {
        valor = '(' + valor;
      } else if (valor.length <= 6) {
        valor = '(' + valor.slice(0, 3) + ') ' + valor.slice(3);
      } else {
        valor = '(' + valor.slice(0, 3) + ') ' + valor.slice(3, 6) + '-' + valor.slice(6);
      }
    } else if (ddi === '+44') { // Reino Unido
      if (valor.length <= 4) {
        valor = valor.slice(0, 4);
      } else if (valor.length <= 7) {
        valor = valor.slice(0, 4) + ' ' + valor.slice(4);
      } else {
        valor = valor.slice(0, 4) + ' ' + valor.slice(4, 7) + '-' + valor.slice(7);
      }
    }
  
    // Atualiza o valor do campo
    input.value = valor;
  }
  

// Função para aplicar a máscara de CEP
function mascaraCep(event) {
  let input = event.target;
  input.value = input.value
    .replace(/\D/g, '') // Remove tudo que não é número
    .replace(/^(\d{5})(\d)/, '$1-$2') // Adiciona o hífen ao CEP
    .slice(0, 9); // Limita o número de caracteres a 9
}

function mascaraData(event) {
    let input = event.target;
    let valor = input.value;
  
    // Remove tudo que não for número
    valor = valor.replace(/\D/g, '');
  
    // Aplica a máscara de data no formato dd/mm/yyyy
    if (valor.length <= 2) {
      valor = valor.slice(0, 2); // Dia
    } else if (valor.length <= 4) {
      valor = valor.slice(0, 2) + '/' + valor.slice(2, 4); // Mês
    } else if (valor.length <= 8) {
      valor = valor.slice(0, 2) + '/' + valor.slice(2, 4) + '/' + valor.slice(4, 8); // Ano
    } else {
      valor = valor.slice(0, 10); // Limita a 10 caracteres
    }
  
    // Atualiza o valor do campo
    input.value = valor;
  }
  
  // Adicionando o evento de 'input' aos campos de telefone e CEP
  document.getElementById('telefone').addEventListener('input', mascaraTelefone);
  document.getElementById('cep').addEventListener('input', mascaraCep);
  document.getElementById('data').addEventListener('input', mascaraData);

  $(document).ready(function(){
    // Obter o ano atual
    var anoAtual = new Date().getFullYear();
  
    // Inicializar o Datepicker com o limite de ano atual
    $("#data").datepicker({
      dateFormat: "dd/mm/yy",  // Formato da data
      changeMonth: true,        // Habilita a navegação por mês
      changeYear: true,         // Habilita a navegação por ano
      yearRange: "1900:" + anoAtual,   // Define o intervalo de anos de 1900 até o ano atual
      showButtonPanel: true,    // Adiciona o painel de botões (se necessário)
      maxDate: new Date()       // Impede que o usuário selecione uma data futura
    });
  });

  document.getElementById('btnCadastrar').addEventListener('click', function(e) {
    e.preventDefault();

    const form = document.getElementById('cadastro-form');
    const formData = new FormData(form);

    fetch('/register', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => console.log('Cadastro feito com sucesso:', data))
    .catch((error) => console.error('Erro:', error));
});

document.getElementById('btnLogin').addEventListener('click', function(e) {
    e.preventDefault();
  
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
  
    fetch('/login', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      console.log('Resposta do servidor:', data);
      if (data.message === "Login bem-sucedido") {
        // Se o login foi sucesso, redireciona
        window.location.href = '/home';  // <-- Coloque aqui a rota da sua página home
      } else {
        alert('Email ou senha inválidos!');
      }
    })
    .catch((error) => console.error('Erro:', error));
  });
  





