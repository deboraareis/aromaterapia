(function () {
  "use strict";

  // ---- Tema claro/escuro/automático, persistido em localStorage ----
  var CHAVE = "debora-aromaterapia-tema";
  var raiz = document.documentElement;
  var botao = document.getElementById("btnTema");
  var rotulo = document.getElementById("btnTemaTexto");
  var ordem = ["auto", "claro", "escuro"];
  var nomes = { auto: "Automático", claro: "Claro", escuro: "Escuro" };

  function aplicar(modo) {
    if (modo === "auto") {
      raiz.removeAttribute("data-tema");
    } else {
      raiz.setAttribute("data-tema", modo);
    }
    if (rotulo) rotulo.textContent = nomes[modo];
  }

  var salvo = localStorage.getItem(CHAVE) || "auto";
  aplicar(salvo);

  if (botao) {
    botao.addEventListener("click", function () {
      var atual = localStorage.getItem(CHAVE) || "auto";
      var proximo = ordem[(ordem.indexOf(atual) + 1) % ordem.length];
      localStorage.setItem(CHAVE, proximo);
      aplicar(proximo);
    });
  }

  // ---- Ano do rodapé ----
  var anoEl = document.getElementById("anoAtual");
  if (anoEl) anoEl.textContent = String(new Date().getFullYear());

  // ---- Copiar e-mail ----
  var btnCopiar = document.getElementById("btnCopiarEmail");
  if (btnCopiar) {
    btnCopiar.addEventListener("click", function () {
      var email = btnCopiar.getAttribute("data-email") || "";
      var textoEl = document.getElementById("btnCopiarEmailTexto");
      navigator.clipboard.writeText(email).then(function () {
        if (textoEl) {
          var original = textoEl.textContent;
          textoEl.textContent = "E-mail copiado!";
          setTimeout(function () { textoEl.textContent = original; }, 2200);
        }
      });
    });
  }
})();
