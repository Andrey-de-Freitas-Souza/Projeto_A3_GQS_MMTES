document.addEventListener('DOMContentLoaded', function () {
  const formContainer = document.getElementById('form-container');
  const loginForm = document.getElementById('login-form');
  const cadastroForm = document.getElementById('cadastro-form');
  const cadastreSe = document.getElementById('cadastre-se');
  const voltarLogin = document.getElementById('voltar-login');
  const btnCadastrar = document.getElementById('btnCadastrar');
  const btnLogin = document.getElementById('btnLogin');
  const telefoneInput = document.getElementById('telefone');
  const cepInput = document.getElementById('cep');
  const nomeInput = document.getElementById('name');
  const sobrenomeInput = document.getElementById('sobrenome');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const confirmacaoSenhaInput = document.getElementById('confirmacao_senha');

  // Impedindo a digitação de números e caracteres especiais nos campos nome e sobrenome
  if (nomeInput) {
    nomeInput.addEventListener('input', function (e) {
      e.target.value = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s-]/g, '');
    });
  }

  if (sobrenomeInput) {
    sobrenomeInput.addEventListener('input', function (e) {
      e.target.value = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s-]/g, '');
    });
  }

  // Validação de e-mail
  if (emailInput) {
    emailInput.addEventListener('input', function (e) {
      const erroEmail = document.getElementById('erro-email');
      const emailValue = e.target.value;
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

      if (!emailRegex.test(emailValue)) {
        erroEmail.style.display = 'inline';
        erroEmail.textContent = 'Por favor, insira um e-mail válido.';
      } else {
        erroEmail.style.display = 'none';
      }
    });
  }

  // Validação de telefone (formato (99) 99999-9999)
  if (telefoneInput) {
    telefoneInput.addEventListener('input', function (e) {
      let telefoneValue = e.target.value.replace(/\D/g, ''); // Remove tudo que não for número

      // Aplica a máscara enquanto o usuário digita
      if (telefoneValue.length <= 2) {
        telefoneValue = '(' + telefoneValue;
      } else if (telefoneValue.length <= 6) {
        telefoneValue = '(' + telefoneValue.slice(0, 2) + ') ' + telefoneValue.slice(2);
      } else if (telefoneValue.length <= 10) {
        telefoneValue = '(' + telefoneValue.slice(0, 2) + ') ' + telefoneValue.slice(2, 7) + '-' + telefoneValue.slice(7);
      } else {
        telefoneValue = '(' + telefoneValue.slice(0, 2) + ') ' + telefoneValue.slice(2, 7) + '-' + telefoneValue.slice(7, 11);
      }

      e.target.value = telefoneValue;
    });
  }

  // Validação de senha (mínimo de 4 caracteres)
  if (senhaInput) {
    senhaInput.addEventListener('input', function (e) {
      const erroSenha = document.getElementById('erro-senha');
      const senhaValue = e.target.value;
      console.log(senhaValue)
      if (senhaValue.length <= 4) {
        erroSenha.style.display = 'inline';
        erroSenha.textContent = 'A senha deve ter no mínimo 4 caracteres.';
      } else {
        erroSenha.style.display = 'none';
      }
    });
  }

  // Validação de confirmação de senha
  if (confirmacaoSenhaInput) {
    confirmacaoSenhaInput.addEventListener('input', function () {
      const erroConfirmacaoSenha = document.getElementById('erro-confirmacao-senha');
      const senhaValue = senhaInput.value;
      const confirmacaoSenhaValue = confirmacaoSenhaInput.value;

      if (confirmacaoSenhaValue !== senhaValue) {
        erroConfirmacaoSenha.style.display = 'inline';
        erroConfirmacaoSenha.textContent = 'As senhas não correspondem.';
      } else {
        erroConfirmacaoSenha.style.display = 'none';
      }
    });
  }

  if (cadastreSe) {
    cadastreSe.addEventListener('click', () => {
      formContainer.style.right = '50%';
      formContainer.style.transform = 'translate(50%, -50%)';
      formContainer.style.borderRadius = '10px';
      formContainer.style.width = '50%';

      loginForm.classList.remove('active');
      cadastroForm.classList.add('active');
    });
  }

  if (voltarLogin) {
    voltarLogin.addEventListener('click', () => {
      formContainer.style.right = '0';
      formContainer.style.transform = 'translateY(-50%)';
      formContainer.style.borderRadius = '10px 0px 0px 10px';
      formContainer.style.width = '40%';

      cadastroForm.classList.remove('active');
      loginForm.classList.add('active');
    });
  }

  function mascaraCep(event) {
    let input = event.target;
    input.value = input.value.replace(/\D/g, '').replace(/^(\d{5})(\d)/, '$1-$2').slice(0, 9);
  }

  if (cepInput) cepInput.addEventListener('input', mascaraCep);

  // Máscara de data
  $(function () {
    const hoje = new Date();
    const anoAtual = hoje.getFullYear();

    $('#data').datepicker({
      dateFormat: 'dd/mm/yy',
      changeMonth: true,
      changeYear: true,
      yearRange: '1910:' + anoAtual,
      showButtonPanel: true,
      maxDate: hoje
    });

    $('#data').on('focus click', function () {
      $(this).datepicker('show');
    });
  });

  if (btnCadastrar) {
    btnCadastrar.addEventListener('click', function (e) {
      e.preventDefault();

      const form = document.getElementById('cadastro-form');
      const formData = new FormData(form);

      function tratarTexto(texto) {
        return texto.trim()
          .replace(/\s+/g, ' ')
          .replace(/[^a-zA-ZÀ-ÿ\s-]/g, '')
          .toLowerCase()
          .split(' ')
          .map(p => p.charAt(0).toUpperCase() + p.slice(1))
          .join(' ');
      }

      const nome = tratarTexto(formData.get('name') || '');
      const sobrenome = tratarTexto(formData.get('sobrenome') || '');
      const nomeCompleto = `${nome} ${sobrenome}`.trim();

      const erroNome = document.getElementById('erro-nome');
      const erroCep = document.getElementById('erro-cep');
      const erroEmail = document.getElementById('erro-email');
      const erroSenha = document.getElementById('erro-senha');
      const erroData = document.getElementById('erro-data');
      const erroTelefone = document.getElementById('erro-telefone');
      const erroConfirmacaoSenha = document.getElementById('erro-confirmacao-senha');

      // Ocultar todos os erros ao iniciar
      [erroNome, erroCep, erroEmail, erroSenha, erroData, erroTelefone, erroConfirmacaoSenha].forEach(erro => {
        if (erro) erro.style.display = 'none';
      });

      let valid = true;

      // Validação do nome completo
      if (nomeCompleto.length > 100) {
        erroNome.style.display = 'inline';
        erroNome.textContent = 'O nome completo não pode ter mais que 100 caracteres.';
        valid = false;
      }

      const cep = (formData.get('address') || '').replace(/\D/g, '');
      if (cep.length !== 8) {
        erroCep.style.display = 'inline';
        erroCep.textContent = 'Preencha o CEP completo.';
        valid = false;
      }

      // Validação do nome e sobrenome
      if ((nome.length + sobrenome.length) < 7) {
        erroNome.style.display = 'inline';
        erroNome.textContent = 'Nome e sobrenome devem ter no mínimo 7 caracteres no total.';
        valid = false;
      }

      // Validação da data
      const data = formData.get('birth_date') || '';
      if (!data.trim()) {
        erroData.style.display = 'inline';
        erroData.textContent = 'Adicione uma data';
        valid = false;
      }

      // Validação de e-mail
      const email = formData.get('email') || '';
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(email)) {
        erroEmail.style.display = 'inline';
        erroEmail.textContent = 'Por favor, insira um e-mail válido.';
        valid = false;
      }

      // Verificando se o e-mail já está cadastrado
      fetch(`/check-email?email=${email}`)
        .then(response => response.json())
        .then(data => {
          if (data.emailExists) {
            erroEmail.style.display = 'inline';
            erroEmail.textContent = 'Este e-mail já está cadastrado.';
            valid = false;
          }

          if (!valid) return;

          formData.set('name', nomeCompleto);

          fetch('/register', {
            method: 'POST',
            body: formData,
          })
            .then(async response => {
              const data = await response.json();
          
              if (response.ok) {
                // Cadastro bem-sucedido
                alert('Cadastro: ' + data.message);
                window.location.href = '/home';
              } else {
                // Erro tratado pelo backend (como e-mail já existente)
                const erroCadastro = document.getElementById('erro-cadastro');
                erroCadastro.style.display = 'inline';
                erroCadastro.textContent = 'Erro: ' + (data.message || 'Erro no cadastro.');
              }
            })
            .catch(error => {
              // Erro inesperado (como falta de conexão)
              console.error('Erro:', error);
              const erroCadastro = document.getElementById('erro-cadastro');
              erroCadastro.style.display = 'inline';
              erroCadastro.textContent = 'Erro: Ocorreu um erro inesperado. Tente novamente mais tarde.';
            });
        })
        .catch(error => {
          console.error('Erro:', error);
        });
    });
  }

  if (btnLogin) {
    btnLogin.addEventListener('click', function (e) {
      e.preventDefault();

      const form = document.getElementById('login-form');
      const formData = new FormData(form);

      fetch('/login', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === "Login bem-sucedido") {
            window.location.href = '/home';
          } else {
          }
        })
        .catch(error => {
          console.error('Erro:', error);
        });
    });
  }
});
document.getElementById('btnLogin').addEventListener('click', async function () {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const msg = document.getElementById('login-msg');
  msg.style.display = 'none';

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Validações
  if (!emailRegex.test(email)) {
      msg.innerText = 'Por favor, insira um e-mail válido.';
      msg.style.display = 'block';
      return;
  }

  if (password.length <= 3) {
      msg.innerText = 'A senha deve ter pelo menos 6 caracteres.';
      msg.style.display = 'block';
      return;
  }

  try {
      const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({ email, password })
      });

      const data = await response.json();

      if (response.status === 200) {
          // Sucesso → redireciona ou mostra mensagem
          console.log('Login bem-sucedido');
          window.location.href = '/home';  // exemplo de redirecionamento
      } else {
          msg.innerText = data.message || data.error || 'Usuário ou senha inválidos.';
          msg.style.display = 'block';
      }

  } catch (error) {
      console.error('Erro:', error);
      msg.innerText = 'Erro ao conectar com o servidor.';
      msg.style.display = 'block';
  }
});