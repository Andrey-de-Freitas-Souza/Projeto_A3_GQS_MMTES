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

  // Helpers
  function tratarTexto(texto) {
    return texto.trim()
      .replace(/\s+/g, ' ')
      .replace(/[^a-zA-ZÀ-ÿ\s-]/g, '')
      .toLowerCase()
      .split(' ')
      .map(p => p.charAt(0).toUpperCase() + p.slice(1))
      .join(' ');
  }

  function exibirErro(campoErro, mensagem) {
    if (campoErro) {
      campoErro.style.display = 'inline';
      campoErro.textContent = mensagem;
    }
  }

  function esconderErros(erros) {
    erros.forEach(erro => {
      if (erro) erro.style.display = 'none';
    });
  }

  // Máscaras e validações imediatas
  if (nomeInput) nomeInput.addEventListener('input', e => e.target.value = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s-]/g, ''));
  if (sobrenomeInput) sobrenomeInput.addEventListener('input', e => e.target.value = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s-]/g, ''));

  if (emailInput) {
    emailInput.addEventListener('input', function (e) {
      const erroEmail = document.getElementById('erro-email');
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      exibirErro(erroEmail, emailRegex.test(e.target.value) ? '' : 'Por favor, insira um e-mail válido.');
      if (emailRegex.test(e.target.value)) erroEmail.style.display = 'none';
    });
  }

  if (telefoneInput) {
    telefoneInput.addEventListener('input', function (e) {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length <= 2) v = '(' + v;
      else if (v.length <= 6) v = '(' + v.slice(0, 2) + ') ' + v.slice(2);
      else if (v.length <= 10) v = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
      else v = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7, 11);
      e.target.value = v;
    });
  }

  if (cepInput) {
    cepInput.addEventListener('input', function (e) {
      e.target.value = e.target.value.replace(/\D/g, '').replace(/^(\d{5})(\d)/, '$1-$2').slice(0, 9);
    });
  }

  if (senhaInput) {
    senhaInput.addEventListener('input', function (e) {
      const erroSenha = document.getElementById('erro-senha');
      if (e.target.value.length < 4) {
        exibirErro(erroSenha, 'A senha deve ter no mínimo 4 caracteres.');
      } else {
        erroSenha.style.display = 'none';
      }
    });
  }

  if (confirmacaoSenhaInput) {
    confirmacaoSenhaInput.addEventListener('input', function () {
      const erro = document.getElementById('erro-confirmacao-senha');
      if (senhaInput.value !== confirmacaoSenhaInput.value) {
        exibirErro(erro, 'As senhas não correspondem.');
      } else {
        erro.style.display = 'none';
      }
    });
  }

  // Alternância entre formulários
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

  // Máscara de data
  $(function () {
    const hoje = new Date();
    $('#data').datepicker({
      dateFormat: 'dd/mm/yy',
      changeMonth: true,
      changeYear: true,
      yearRange: '1910:' + hoje.getFullYear(),
      showButtonPanel: true,
      maxDate: hoje
    }).on('focus click', function () {
      $(this).datepicker('show');
    });
  });

  // Validação e envio do cadastro
  if (btnCadastrar) {
    btnCadastrar.addEventListener('click', async function (e) {
      e.preventDefault();
  
      const form = document.getElementById('cadastro-form');
      const formData = new FormData(form);
  
      const nome = tratarTexto(formData.get('name') || '');
      const sobrenome = tratarTexto(formData.get('sobrenome') || '');
      const nomeCompleto = `${nome} ${sobrenome}`.trim();
      const cep = (formData.get('address') || '').replace(/\D/g, '');
      const email = formData.get('email') || '';
      const senha = formData.get('senha') || '';
      const confirmar = formData.get('confirm_password') || '';
      const data = formData.get('birth_date') || '';
      const telefone = formData.get('phone') || '';
  
      const erroNome = document.getElementById('erro-nome');
      const erroCep = document.getElementById('erro-cep');
      const erroEmail = document.getElementById('erro-email');
      const erroSenha = document.getElementById('erro-senha');
      const erroData = document.getElementById('erro-data');
      const erroTelefone = document.getElementById('erro-telefone');
      const erroConfirmacaoSenha = document.getElementById('erro-confirmacao-senha');
      console.log(senha)
      console.log(senha.length)
      esconderErros([erroNome, erroCep, erroEmail, erroSenha, erroData, erroTelefone, erroConfirmacaoSenha]);
  
      let valid = true;
  
      if ((nome + sobrenome).length < 7 || nomeCompleto.length > 100) {
        exibirErro(erroNome, 'Nome e sobrenome devem ter entre 7 e 100 caracteres no total.');
        valid = false;
      }
  
      if (cep.length !== 8) {
        exibirErro(erroCep, 'Preencha o CEP completo.');
        valid = false;
      }
  
      if (!data.trim()) {
        exibirErro(erroData, 'Adicione uma data.');
        valid = false;
      }
  
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        exibirErro(erroEmail, 'Por favor, insira um e-mail válido.');
        valid = false;
      }
  
      if (senha.length <= 3) {
        exibirErro(erroSenha, 'A senha deve ter no mínimo 4 caracteres.');
        valid = false;
      }
  
      if (senha !== confirmar) {
        exibirErro(erroConfirmacaoSenha, 'As senhas não correspondem.');
        valid = false;
      }
  
      if (telefone.length !== 15) {
        exibirErro(erroTelefone, 'Preencha o telefone completo.');
        valid = false;
      }
  
      if (!valid) return;
  
      try {
        const res = await fetch(`/check-email?email=${email}`);
        const check = await res.json();
  
        if (check.emailExists) {
          exibirErro(erroEmail, 'Este e-mail já está cadastrado.');
          return;
        }
  
        formData.set('name', nomeCompleto);
  
        const response = await fetch('/register', {
          method: 'POST',
          body: formData
        });
  
        const result = await response.json();
  
        if (response.ok) {
          alert('Cadastro: ' + result.message);
          window.location.href = '/home';
        } else {
          exibirErro(document.getElementById('erro-cadastro'), 'Erro: ' + (result.message || 'Erro no cadastro.'));
        }
  
      } catch (error) {
        console.error('Erro:', error);
        exibirErro(document.getElementById('erro-cadastro'), 'Erro inesperado. Tente novamente.');
      }
    });
  }
  

  // Validação e envio do login
  if (btnLogin) {
    btnLogin.addEventListener('click', async function (e) {
      e.preventDefault();
  
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const msg = document.getElementById('login-msg');
      msg.style.display = 'none';
  
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        msg.innerText = 'Por favor, insira um e-mail válido.';
        msg.style.display = 'block';
        return;
      }
  
      if (password.length <= 3) {
        msg.innerText = 'A senha deve ter pelo menos 4 caracteres.';
        msg.style.display = 'block';
        return;
      }
  
      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({ email, password })
        });
  
        const data = await response.json();
  
        // Verifica se o status da resposta é 200 (login bem-sucedido)
        if (response.status === 200) {
          window.location.href = '/home';  // Redireciona para a página /home
        } else {
          msg.innerText = data.error || 'Usuário ou senha inválidos.';
          msg.style.display = 'block';
        }
  
      } catch (error) {
        console.error('Erro:', error);
        msg.innerText = 'Erro ao conectar com o servidor.';
        msg.style.display = 'block';
      }
    });
  }
  
});
