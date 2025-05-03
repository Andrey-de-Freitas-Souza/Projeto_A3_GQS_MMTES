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
  function togglepodio() {
    const lista = document.getElementById("lista-podio");
    const seta = document.getElementById("seta3");
  
    if (lista.style.display === "none") {
        lista.style.display = "block";
        seta.innerHTML = "&#9650;"; // seta para cima
    } else {
        lista.style.display = "none";
        seta.innerHTML = "&#9660;"; // seta para baixo
    }
  }
  window.onload = function() {
    // Pegar todos os elementos com a classe 'coluna'
    const amigos = document.querySelectorAll('.coluna');

    // Encontrar o valor máximo de pontos
    let maxPontos = 0;
    amigos.forEach(amigo => {
        const pontos = parseInt(amigo.querySelector('.pontos').textContent);
        if (pontos > maxPontos) {
            maxPontos = pontos;
        }
    });

    // Função para calcular a altura proporcional
    function calcularAltura(pontos, maxPontos, alturaMax = 300) {
        // Caso os pontos sejam 0, atribuímos 0,01 para evitar divisão por zero
        if (maxPontos === 0 || pontos === 0) {
            return 10;  // Atribui um valor mínimo de 0,01 se os pontos forem 0
        }
        return (pontos / maxPontos) * alturaMax;
    }

    // Aplicar a altura nas barras
    amigos.forEach(amigo => {
        const pontos = parseInt(amigo.querySelector('.pontos').textContent);
        const altura = calcularAltura(pontos, maxPontos);
        const barra = amigo.querySelector('.barra');
        barra.style.height = altura + 'px';  // Define a altura da barra
    });
};