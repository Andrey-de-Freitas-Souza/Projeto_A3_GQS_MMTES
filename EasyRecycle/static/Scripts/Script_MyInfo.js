function uploadImage(event) {
    const file = event.target.files[0];
    
    const maxSize = 2 * 1024 * 1024; // Limite de 2MB

    if (file.size > maxSize) {
        alert("A imagem deve ter no máximo 2MB.");
        return;
    }

    const validTypes = ["image/jpeg", "image/png", "image/gif"];
    if (!validTypes.includes(file.type)) {
        alert("Por favor, envie uma imagem JPEG, PNG ou GIF.");
        return;
    }

    const formData = new FormData();
    formData.append('profile_picture', file);

    fetch('/upload_photo', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualiza o caminho da imagem de perfil
            const userId = document.getElementById('Profile').getAttribute('data-user-id'); // Supondo que o id do usuário esteja armazenado no elemento
            document.getElementById('Profile').src = `/get_profile_image/${userId}`;
        } else {
            alert('Erro ao fazer o upload da foto!');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}
