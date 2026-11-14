(function () {
  "use strict";

  var itens = document.querySelectorAll(".faq__item");

  itens.forEach(function (item) {
    var pergunta = item.querySelector(".faq__pergunta");
    if (!pergunta) return;

    pergunta.addEventListener("click", function () {
      var estavaAberto = item.getAttribute("data-aberto") === "true";
      itens.forEach(function (outro) {
        outro.setAttribute("data-aberto", "false");
        var p = outro.querySelector(".faq__pergunta");
        if (p) p.setAttribute("aria-expanded", "false");
      });
      if (!estavaAberto) {
        item.setAttribute("data-aberto", "true");
        pergunta.setAttribute("aria-expanded", "true");
      }
    });
  });
})();
