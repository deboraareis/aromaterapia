(function () {
  "use strict";

  var botao = document.getElementById("btnMenu");
  var nav = document.getElementById("navMovel");
  if (!botao || !nav) return;

  function fechar() {
    nav.classList.remove("aberto");
    botao.setAttribute("aria-expanded", "false");
  }

  botao.addEventListener("click", function () {
    var aberto = nav.classList.toggle("aberto");
    botao.setAttribute("aria-expanded", aberto ? "true" : "false");
  });

  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", fechar);
  });

  document.addEventListener("keydown", function (evento) {
    if (evento.key === "Escape") fechar();
  });
})();
