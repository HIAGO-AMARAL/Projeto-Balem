/* Doce Pausa · versão estática (GitHub Pages).
   Aqui o navegador faz o que o servidor Flask fazia: guarda o carrinho, "entra"
   na conta e leva a pessoa à página do vídeo.

   PRIVACIDADE: tudo fica em sessionStorage, que é só da aba do visitante e some
   quando ela é fechada. Nada é enviado para servidor nenhum, e o e-mail e a senha
   digitados no login são ignorados. */

(function () {
    "use strict";

    var LIMITE_POR_DOCE = 20;
    var CHAVE_CARRINHO = "doce-pausa-carrinho";
    var CHAVE_LOGADO = "doce-pausa-logado";
    var CHAVE_AVISO = "doce-pausa-aviso";
    var CHAVE_FIM = "doce-pausa-fim";

    // ---- sessionStorage pode falhar (aba anônima, etc.), então protegemos ----
    var memoria = {};
    function ler(chave) {
        try { return sessionStorage.getItem(chave); } catch (e) {
            return Object.prototype.hasOwnProperty.call(memoria, chave) ? memoria[chave] : null;
        }
    }
    function gravar(chave, valor) {
        try { sessionStorage.setItem(chave, valor); } catch (e) { memoria[chave] = valor; }
    }
    function apagar(chave) {
        try { sessionStorage.removeItem(chave); } catch (e) { /* ignora */ }
        delete memoria[chave];
    }

    // ---- carrinho e login ----
    function lerCarrinho() {
        try {
            var c = JSON.parse(ler(CHAVE_CARRINHO) || "{}");
            return c && typeof c === "object" && !Array.isArray(c) ? c : {};
        } catch (e) { return {}; }
    }
    function gravarCarrinho(c) { gravar(CHAVE_CARRINHO, JSON.stringify(c)); }
    function totalDeItens(c) {
        return Object.keys(c).reduce(function (soma, id) {
            var q = parseInt(c[id], 10);
            return soma + (q > 0 ? Math.min(q, LIMITE_POR_DOCE) : 0);
        }, 0);
    }
    function estaLogado() { return ler(CHAVE_LOGADO) === "1"; }

    function brl(valor) {
        return "R$ " + valor.toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");
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
    // Aviso deixado pela página anterior (equivale ao "flash" do Flask).
    function guardarAviso(texto) { gravar(CHAVE_AVISO, texto); }
    var avisoPendente = ler(CHAVE_AVISO);
    if (avisoPendente) {
        apagar(CHAVE_AVISO);
        mostrarToast(avisoPendente);
    }

    // ---- cabeçalho: selo do carrinho e área da conta ----
    function atualizarCabecalho(animar) {
        var selo = document.getElementById("contagem-carrinho");
        if (selo) {
            var quantidade = totalDeItens(lerCarrinho());
            selo.textContent = quantidade;
            selo.hidden = quantidade <= 0;
            if (animar) {
                selo.classList.remove("pop");
                void selo.offsetWidth; // reinicia a animação
                selo.classList.add("pop");
            }
        }
        var linkEntrar = document.getElementById("link-entrar");
        var areaLogado = document.getElementById("area-logado");
        if (linkEntrar && areaLogado) {
            linkEntrar.hidden = estaLogado();
            areaLogado.hidden = !estaLogado();
        }
    }

    var botaoSair = document.getElementById("botao-sair");
    if (botaoSair) {
        botaoSair.addEventListener("click", function () {
            apagar(CHAVE_LOGADO);
            atualizarCabecalho(false);
            if (typeof desenharCarrinho === "function") { desenharCarrinho(); }
        });
    }

    // ---- cronômetro da "promoção relâmpago" (só enfeite) ----
    // Reinicia sozinho quando chega a zero: golpes de verdade fazem o mesmo.
    var contador = document.getElementById("contador");
    if (contador) {
        var DURACAO = 15 * 60 * 1000;
        var fim = Number(ler(CHAVE_FIM)) || 0;
        var reiniciar = function () {
            fim = Date.now() + DURACAO;
            gravar(CHAVE_FIM, String(fim));
        };
        var doisDigitos = function (n) { return (n < 10 ? "0" : "") + n; };
        var desenharContador = function () {
            if (fim - Date.now() <= 0) { reiniciar(); }
            var restante = fim - Date.now();
            contador.textContent =
                doisDigitos(Math.floor(restante / 60000)) + ":" +
                doisDigitos(Math.floor((restante % 60000) / 1000));
        };
        if (fim <= Date.now()) { reiniciar(); }
        desenharContador();
        setInterval(desenharContador, 1000);
    }

    // ---- loja: filtro por categoria, busca e "adicionar ao carrinho" ----
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

    Array.prototype.forEach.call(document.querySelectorAll(".form-adicionar"), function (form) {
        form.addEventListener("submit", function (evento) {
            evento.preventDefault();
            var botao = form.querySelector("button");
            if (botao.disabled) { return; }

            var id = form.dataset.doce;
            var carrinho = lerCarrinho();
            carrinho[id] = Math.min((parseInt(carrinho[id], 10) || 0) + 1, LIMITE_POR_DOCE);
            gravarCarrinho(carrinho);

            atualizarCabecalho(true);
            mostrarToast(form.dataset.nome + " foi para o carrinho!");

            var textoOriginal = botao.textContent;
            botao.disabled = true;
            botao.textContent = "✔ Adicionado!";
            botao.classList.add("is-ok");
            setTimeout(function () {
                botao.textContent = textoOriginal;
                botao.classList.remove("is-ok");
                botao.disabled = false;
            }, 1300);
        });
    });

    // ---- página do carrinho ----
    var listaCarrinho = document.getElementById("lista-carrinho");
    var desenharCarrinho; // fica indefinida fora da página do carrinho

    if (listaCarrinho) {
        var doces = JSON.parse(document.getElementById("dados-doces").textContent);
        var blocoVazio = document.getElementById("carrinho-vazio");
        var blocoCheio = document.getElementById("carrinho-cheio");

        desenharCarrinho = function () {
            var carrinho = lerCarrinho();
            var itens = [];
            var quantidade = 0, total = 0, totalOriginal = 0;

            Object.keys(carrinho).forEach(function (id) {
                var doce = Object.prototype.hasOwnProperty.call(doces, id) ? doces[id] : null;
                var q = Math.min(parseInt(carrinho[id], 10), LIMITE_POR_DOCE);
                if (!doce || !(q > 0)) { return; }
                itens.push({ id: id, doce: doce, quantidade: q });
                quantidade += q;
                total += doce.preco * q;
                totalOriginal += doce.preco_original * q;
            });

            blocoVazio.hidden = itens.length > 0;
            blocoCheio.hidden = itens.length === 0;
            atualizarCabecalho(false);
            if (!itens.length) { return; }

            listaCarrinho.innerHTML = itens.map(function (item) {
                var d = item.doce;
                var miniatura = d.foto
                    ? '<img src="assets/' + d.foto + '" alt="" width="72" height="72">'
                    : d.emoji;
                return '<li class="item-carrinho">' +
                    '<div class="item-carrinho__emoji cat-' + d.categoria + '" aria-hidden="true">' + miniatura + '</div>' +
                    '<div class="item-carrinho__info"><h3>' + d.nome + '</h3>' +
                    '<p><s>' + brl(d.preco_original) + '</s> <strong>' + brl(d.preco) + '</strong> cada</p></div>' +
                    '<div class="quantidade" role="group" aria-label="Quantidade de ' + d.nome + '">' +
                    '<button type="button" data-acao="menos" data-id="' + item.id + '" aria-label="Diminuir quantidade">−</button>' +
                    '<span>' + item.quantidade + '</span>' +
                    '<button type="button" data-acao="mais" data-id="' + item.id + '" aria-label="Aumentar quantidade">+</button></div>' +
                    '<div class="item-carrinho__subtotal">' + brl(d.preco * item.quantidade) + '</div>' +
                    '<button type="button" class="botao-remover" data-acao="remover" data-id="' + item.id + '"' +
                    ' aria-label="Remover ' + d.nome + '" title="Remover">✕</button>' +
                    '</li>';
            }).join("");

            var economia = totalOriginal - total;
            document.getElementById("resumo-itens").textContent = "Itens (" + quantidade + ")";
            document.getElementById("resumo-original").textContent = brl(totalOriginal);
            document.getElementById("resumo-desconto").textContent = "− " + brl(economia);
            document.getElementById("resumo-total").textContent = brl(total);
            document.getElementById("resumo-economia").textContent = "🎉 Você está economizando " + brl(economia) + "!";
            document.getElementById("resumo-nota").textContent = estaLogado()
                ? "Pagamento na retirada, durante o intervalo."
                : "Você vai precisar entrar na sua conta para finalizar.";
        };

        listaCarrinho.addEventListener("click", function (evento) {
            var botao = evento.target.closest("button[data-acao]");
            if (!botao) { return; }

            var id = botao.dataset.id;
            var carrinho = lerCarrinho();
            if (Object.prototype.hasOwnProperty.call(carrinho, id)) {
                var acao = botao.dataset.acao;
                var atual = parseInt(carrinho[id], 10) || 0;
                if (acao === "mais") { carrinho[id] = Math.min(atual + 1, LIMITE_POR_DOCE); }
                else if (acao === "menos") { carrinho[id] = atual - 1; }
                else if (acao === "remover") { carrinho[id] = 0; }
                if (carrinho[id] <= 0) { delete carrinho[id]; }
                gravarCarrinho(carrinho);
            }
            desenharCarrinho();
        });

        document.getElementById("botao-finalizar").addEventListener("click", function () {
            if (totalDeItens(lerCarrinho()) === 0) {
                guardarAviso("Seu carrinho está vazio. Escolha um docinho antes!");
                window.location.href = "index.html#doces";
                return;
            }
            if (!estaLogado()) {
                guardarAviso("Entre na sua conta para finalizar a compra.");
                window.location.href = "entrar.html?proximo=carrinho";
                return;
            }
            // Nada fica guardado depois da "compra".
            apagar(CHAVE_CARRINHO);
            apagar(CHAVE_LOGADO);
            window.location.href = "ops.html";
        });

        desenharCarrinho();
    }

    // ---- página de login (de mentira) ----
    var formLogin = document.getElementById("form-login");
    if (formLogin) {
        formLogin.addEventListener("submit", function (evento) {
            evento.preventDefault();
            // De propósito NÃO lemos os campos: nada digitado é usado ou salvo.
            gravar(CHAVE_LOGADO, "1");

            var proximo = new URLSearchParams(window.location.search).get("proximo");
            if (proximo === "carrinho") {
                guardarAviso("Pronto! Agora é só finalizar a sua compra.");
                window.location.href = "carrinho.html";
            } else {
                window.location.href = "index.html";
            }
        });
    }

    atualizarCabecalho(false);
})();
