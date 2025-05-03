document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os botões de "Marcar como lida"
    const buttons = document.querySelectorAll('.mark-as-read');

    // Para cada botão, adiciona o evento de clique
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const notificationId = this.closest('.notification').getAttribute('data-id');
            markAsRead(notificationId);
        });
    });
});

function markAsRead(notificationId) {
    const notification = document.querySelector(`.notification[data-id='${notificationId}']`);

    // Envia uma solicitação AJAX para o servidor marcar como lida
    fetch(`/mark_as_read/${notificationId}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualiza a interface, removendo a notificação "nova"
            notification.classList.add('read');
            notification.querySelector('.mark-as-read').disabled = true;
        }
    })
    .catch(error => {
        console.error('Erro ao marcar a notificação como lida:', error);
    });
}