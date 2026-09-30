"""Doce Pausa: loja de doces falsa usada numa simulação de phishing.

Projeto escolar de segurança da informação. A "loja" vende doces com preços
absurdos para atrair o clique. Quando a pessoa finaliza a compra, ela vê um
vídeo explicando que caiu num phishing e como se proteger.

PRIVACIDADE: o site NÃO tem banco de dados e NÃO guarda dados de ninguém.
  * Os campos de e-mail e senha do login não têm atributo `name`, então o
    navegador nem envia o que foi digitado (veja templates/login.html).
  * O servidor guarda só: os doces do carrinho (id + quantidade) no cookie de
    sessão do próprio visitante e dois contadores em memória, sem identificar
    ninguém.
"""

import os
import re

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from catalogo import CATEGORIAS, DOCES, DOCES_POR_ID

# ---------------------------------------------------------------------------
# VÍDEO DA EQUIPE: é aqui que se coloca o vídeo que vai passar no final.
# O site tenta as opções nesta ordem; se nenhuma estiver pronta, mostra um
# espaço reservado no lugar do vídeo.
#
#   Opção 1 (arquivo): coloque o .mp4 dentro de static/video/ e confira se o
#           nome abaixo é o mesmo do arquivo.
#   Opção 2 (YouTube): cole o link do vídeo (pode ser o link normal do
#           navegador, o encurtado youtu.be ou o de compartilhar).
# ---------------------------------------------------------------------------
VIDEO_ARQUIVO = "phishing.mp4"
VIDEO_YOUTUBE = ""

app = Flask(__name__)

# O cookie de sessão só guarda o carrinho, então uma chave fixa não é segredo
# crítico. Numa hospedagem de verdade, defina a variável SECRET_KEY.
app.secret_key = os.environ.get("SECRET_KEY", "doce-pausa-projeto-escolar")

# Contadores para a apresentação. Ficam só na memória (somem ao reiniciar).
estatisticas = {"logins": 0, "caiu": 0}

LIMITE_POR_DOCE = 20


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------
@app.template_filter("brl")
def formatar_real(valor):
    """1234.5 -> 'R$ 1.234,50'"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


# Fotos dos doces: coloque o arquivo em static/img/doces/ com o MESMO nome do
# id do doce (ex.: torta-limao.jpg). Sem foto, a loja mostra o emoji do doce.
EXTENSOES_FOTO = ("jpg", "jpeg", "webp", "png")


@app.template_global()
def foto_do_doce(doce_id):
    """Caminho (dentro de static/) da foto do doce, ou None se ainda não tem."""
    for extensao in EXTENSOES_FOTO:
        caminho = f"img/doces/{doce_id}.{extensao}"
        if os.path.isfile(os.path.join(app.static_folder, caminho)):
            return caminho
    return None


def carrinho_atual():
    return session.get("carrinho", {})


def detalhes_do_carrinho():
    """Devolve (itens, resumo) com os doces do carrinho já calculados."""
    itens = []
    quantidade_total = 0
    total = 0.0
    total_original = 0.0

    for doce_id, quantidade in carrinho_atual().items():
        doce = DOCES_POR_ID.get(doce_id)
        if doce is None:
            continue
        subtotal = doce["preco"] * quantidade
        itens.append({"doce": doce, "quantidade": quantidade, "subtotal": subtotal})
        quantidade_total += quantidade
        total += subtotal
        total_original += doce["preco_original"] * quantidade

    resumo = {
        "quantidade": quantidade_total,
        "total": total,
        "total_original": total_original,
        "economia": total_original - total,
    }
    return itens, resumo


def link_youtube_embed(link):
    """Converte qualquer link do YouTube no endereço de incorporação (ou None)."""
    achou = re.search(r"(?:youtu\.be/|v=|embed/|shorts/)([\w-]{11})", link or "")
    if achou:
        return f"https://www.youtube-nocookie.com/embed/{achou.group(1)}"
    return None


def arquivo_de_video_existe():
    """True se o arquivo de VIDEO_ARQUIVO está mesmo em static/video/."""
    if not VIDEO_ARQUIVO:
        return False
    return os.path.isfile(os.path.join(app.static_folder, "video", VIDEO_ARQUIVO))


def video_configurado():
    """Escolhe o vídeo a mostrar na página educativa (ou None)."""
    if arquivo_de_video_existe():
        return {
            "tipo": "arquivo",
            "src": url_for("static", filename=f"video/{VIDEO_ARQUIVO}"),
        }

    embed = link_youtube_embed(VIDEO_YOUTUBE)
    if embed:
        return {"tipo": "youtube", "src": embed}

    return None


@app.context_processor
def dados_globais():
    """Variáveis disponíveis em todos os templates (cabeçalho da loja)."""
    _, resumo = detalhes_do_carrinho()
    return {
        "qtd_carrinho": resumo["quantidade"],
        "logado": session.get("logado", False),
    }


# ---------------------------------------------------------------------------
# Loja
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", doces=DOCES, categorias=CATEGORIAS)


@app.route("/carrinho")
def carrinho():
    itens, resumo = detalhes_do_carrinho()
    return render_template("carrinho.html", itens=itens, resumo=resumo)


@app.route("/carrinho/adicionar/<doce_id>", methods=["POST"])
def adicionar(doce_id):
    doce = DOCES_POR_ID.get(doce_id)
    if doce is None:
        abort(404)

    itens = dict(carrinho_atual())
    itens[doce_id] = min(itens.get(doce_id, 0) + 1, LIMITE_POR_DOCE)
    session["carrinho"] = itens

    _, resumo = detalhes_do_carrinho()

    # O JavaScript da loja pede JSON para atualizar a página sem recarregar.
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify(ok=True, nome=doce["nome"], quantidade=resumo["quantidade"])

    flash(f"{doce['nome']} foi para o carrinho!")
    return redirect(url_for("index") + "#doces")


@app.route("/carrinho/atualizar/<doce_id>", methods=["POST"])
def atualizar(doce_id):
    itens = dict(carrinho_atual())
    if doce_id in itens:
        acao = request.form.get("acao")
        if acao == "mais":
            itens[doce_id] = min(itens[doce_id] + 1, LIMITE_POR_DOCE)
        elif acao == "menos":
            itens[doce_id] -= 1
        elif acao == "remover":
            itens[doce_id] = 0

        if itens[doce_id] <= 0:
            del itens[doce_id]
        session["carrinho"] = itens

    return redirect(url_for("carrinho"))


# ---------------------------------------------------------------------------
# Login de mentira: aceita qualquer coisa e não guarda nada
# ---------------------------------------------------------------------------
@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    if request.method == "POST":
        # De propósito NÃO lemos request.form: nada digitado é usado ou salvo.
        # Só marcamos que o visitante "entrou", para a loja parecer real.
        session["logado"] = True
        estatisticas["logins"] += 1

        if request.args.get("proximo") == "carrinho":
            flash("Pronto! Agora é só finalizar a sua compra.")
            return redirect(url_for("carrinho"))
        return redirect(url_for("index"))

    return render_template("login.html", proximo=request.args.get("proximo", ""))


@app.route("/sair", methods=["POST"])
def sair():
    session.pop("logado", None)
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# O momento da verdade
# ---------------------------------------------------------------------------
@app.route("/finalizar", methods=["POST"])
def finalizar():
    itens, _ = detalhes_do_carrinho()
    if not itens:
        flash("Seu carrinho está vazio. Escolha um docinho antes!")
        return redirect(url_for("index") + "#doces")

    if not session.get("logado"):
        flash("Entre na sua conta para finalizar a compra.")
        return redirect(url_for("entrar", proximo="carrinho"))

    estatisticas["caiu"] += 1
    session.clear()  # nada fica guardado depois da "compra"
    return redirect(url_for("educativo"))


@app.route("/ops")
def educativo():
    return render_template("educativo.html", video=video_configurado())


# ---------------------------------------------------------------------------
# Painel para a apresentação (não tem link no site)
# ---------------------------------------------------------------------------
@app.route("/painel")
def painel():
    return render_template("painel.html", stats=estatisticas)


if __name__ == "__main__":
    # Por padrão só o próprio computador acessa. Para a turma acessar pela rede
    # da escola, veja "Como rodar" no README.md.
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
