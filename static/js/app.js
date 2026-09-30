/* Doce Pausa · comportamento da loja.
   Nada aqui envia dados pessoais: só adiciona doces ao carrinho, filtra o
   catálogo e mostra o cronômetro da promoção (que é só enfeite). */

(function () {
    "use strict";

    // ---- sessionStorage pode falhar (aba anônima, etc.), então protegemos ----
    function lerSessao(chave) {
        try { return sessionStorage.getItem(chave); } catch (e) { return null; }
    }
    function gravarSessao(chave, valor) {
        try { sessionStorage.setItem(chave, valor); } catch (e) { /* ignora */ }
    }

    // ---- cronômetro da "promoção relâmpago" ----
    // Reinicia sozinho quando chega a zero: golpes de verdade fazem o mesmo.
    var contador = document.getElementById("contador");
    if (contador) {
        var DURACAO = 15 * 60 * 1000;
        var fim = Number(lerSessao("doce-pausa-fim")) || 0;

        var reiniciar = function () {
            fim = Date.now() + DURACAO;
            gravarSessao("doce-pausa-fim", String(fim));
        };
        var doisDigitos = function (n) { return (n < 10 ? "0" : "") + n; };
        var desenhar = function () {
            if (fim - Date.now() <= 0) { reiniciar(); }
            var restante = fim - Date.now();
            var min = Math.floor(restante / 60000);
            var seg = Math.floor((restante % 60000) / 1000);
            contador.textContent = doisDigitos(min) + ":" + doisDigitos(seg);
        };

        if (fim <= Date.now()) { reiniciar(); }
        desenhar();
        setInterval(desenhar, 1000);
    }

    // ---- avisos (toast) ----
    var areaToast = document.getElementById("area-toast");

    function agendarSaida(toast) {
        setTimeout(function () {
            toast.classList.add("saindo");
            setTimeout(function () { toast.remove(); }, 400);
        }, 3600);
    }

    function mostrarToast(texto) {
        if (!areaToast) { return; }
        var toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = texto;
        areaToast.appendChild(toast);
        agendarSaida(toast);
    }

    if (areaToast) {
        Array.prototype.forEach.call(areaToast.querySelectorAll(".toast"), agendarSaida);
    }

    // ---- filtro por categoria e busca ----
    var cards = Array.prototype.slice.call(document.querySelectorAll(".card-doce"));
    var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
    var campoBusca = document.getElementById("busca");
    var semResultado = document.getElementById("sem-resultado");
    var filtroAtual = "todos";

    function normalizar(texto) {
        return texto.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    }

    function aplicarFiltros() {
        var termo = campoBusca ? normalizar(campoBusca.value.trim()) : "";
        var visiveis = 0;

        cards.forEach(function (card) {
            var categoriaOk = filtroAtual === "todos" || card.dataset.categoria === filtroAtual;
            var buscaOk = !termo || normalizar(card.dataset.busca).indexOf(termo) !== -1;
            card.hidden = !(categoriaOk && buscaOk);
            if (!card.hidden) { visiveis += 1; }
        });

        if (semResultado) { semResultado.hidden = visiveis > 0; }
    }

    chips.forEach(function (chip) {
        chip.addEventListener("click", function () {
            filtroAtual = chip.dataset.filtro;
            chips.forEach(function (c) { c.classList.toggle("is-ativo", c === chip); });
            aplicarFiltros();
        });
    });

    if (campoBusca) { campoBusca.addEventListener("input", aplicarFiltros); }

    // ---- adicionar ao carrinho sem recarregar a página ----
    function atualizarSeloCarrinho(quantidade) {
        var selo = document.getElementById("contagem-carrinho");
        if (!selo) { return; }
        selo.textContent = quantidade;
        selo.hidden = quantidade <= 0;
        selo.classList.remove("pop");
        void selo.offsetWidth; // reinicia a animação
        selo.classList.add("pop");
    }

    Array.prototype.forEach.call(document.querySelectorAll(".form-adicionar"), function (form) {
        form.addEventListener("submit", function (evento) {
            if (!window.fetch) { return; } // sem fetch, o formulário normal funciona

            evento.preventDefault();
            var botao = form.querySelector("button");
            if (botao.disabled) { return; }
            var textoOriginal = botao.textContent;
            botao.disabled = true;

            fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "fetch" },
                credentials: "same-origin"
            })
                .then(function (resposta) {
                    if (!resposta.ok) { throw new Error("falhou"); }
                    return resposta.json();
                })
                .then(function (dados) {
                    atualizarSeloCarrinho(dados.quantidade);
                    mostrarToast(dados.nome + " foi para o carrinho!");
                    botao.textContent = "✔ Adicionado!";
                    botao.classList.add("is-ok");
                    setTimeout(function () {
                        botao.textContent = textoOriginal;
                        botao.classList.remove("is-ok");
                        botao.disabled = false;
                    }, 1300);
                })
                .catch(function () {
                    form.submit(); // se algo der errado, cai no envio normal
                });
        });
    });
})();
