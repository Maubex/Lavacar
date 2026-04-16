/* ═══════════════════════════════════════════════════
   JS Sidebar - América Lavacar
   Proteção contra erros de elementos nulos
═══════════════════════════════════════════════════ */

let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

// 1. Só adiciona o evento se o botão de fechar existir na página
if (closeBtn && sidebar) {
    closeBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        menuBtnChange();
    });
}

// 2. Só adiciona o listener se o botão de busca existir
if (searchBtn && sidebar) {
    searchBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        menuBtnChange();
    });
}

// 3. Função para trocar o ícone do menu
function menuBtnChange() {
    if (sidebar && closeBtn) { // Verifica se os elementos existem antes de agir
        if (sidebar.classList.contains("open")) {
            closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
        } else {
            closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
        }
    }
}