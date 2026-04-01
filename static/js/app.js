// 1. Pega os elementos que vamos usar
const abrirBtn = document.getElementById('abrirModalBtn');
const fecharBtn = document.getElementById('fecharModalBtn');
const modalOverlay = document.getElementById('meuModal');

// 2. Quando o usuário clicar no botão "Abrir"
abrirBtn.addEventListener('click', function() {
    // Adiciona a classe 'visivel' ao overlay
    modalOverlay.classList.add('visivel');
});

// 3. Quando o usuário clicar no botão de "Fechar" (o 'X')
fecharBtn.addEventListener('click', function() {
    // Remove a classe 'visivel' do overlay
    modalOverlay.classList.remove('visivel');
});

// 4. (Opcional) Fechar o modal se clicar FORA da janela (no fundo)
modalOverlay.addEventListener('click', function(event) {
    // Verifica se o clique foi no overlay (o pai) e não na janela (o filho)
    if (event.target === modalOverlay) {
        modalOverlay.classList.remove('visivel');
    }
});