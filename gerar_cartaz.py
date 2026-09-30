"""Gera o cartaz A4 da Doce Pausa, com o QR code que leva ao site.

Uso (dentro da pasta do projeto, com o ambiente virtual ativado):

    pip install segno
    python gerar_cartaz.py

Escreve em cartaz/:
  * cartaz.html   o cartaz (A4). Para imprimir: abra no Chrome/Edge > Ctrl+P > "Salvar como PDF"
                  (ou imprima direto), com "Gráficos de segundo plano" ligado e margens "Nenhuma";
  * qrcode.png    só o QR code, para usar no Canva ou em outro programa;
  * qrcode.svg    o mesmo QR code em vetor (não perde qualidade ao ampliar).

O QR aponta para o site com "?utm_campaign=cartaz": o GoatCounter mostra no painel
(bloco "Campaigns") quantas pessoas chegaram pelo cartaz.
"""

import os

import segno
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from catalogo import DOCES_POR_ID

# ---------------------------------------------------------------------------
SITE = "https://hiago-amaral.github.io/Projeto-Balem/"
CAMPANHA = "cartaz"  # aparece no painel do GoatCounter; deixe "" para não marcar

DESTAQUE = "torta-limao"
EXTRAS = ["brigadeiro", "cookie", "cupcake", "pudim"]
# ---------------------------------------------------------------------------

RAIZ = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(RAIZ, "cartaz")

COR_ESCURA = "#2B170E"  # marrom bem escuro: contraste alto para a câmera ler fácil


def dados_do_doce(doce_id):
    doce = DOCES_POR_ID[doce_id]
    foto = f"../static/img/doces/{doce_id}.jpg"
    if not os.path.isfile(os.path.join(RAIZ, "static", "img", "doces", f"{doce_id}.jpg")):
        raise SystemExit(f"Falta a foto de {doce_id} em static/img/doces/")
    return {
        "nome": doce["nome"].replace("Fatia de ", "").capitalize(),
        "original": f"{doce['preco_original']:.2f}".replace(".", ","),
        "preco": f"{doce['preco']:.2f}".replace(".", ","),
        "desconto": doce["desconto"],
        "foto": foto,
    }


def main():
    url = SITE + (f"?utm_campaign={CAMPANHA}" if CAMPANHA else "")

    # error="q": o QR aguenta ~25% de sujeira/dobra do papel e continua legível
    qr = segno.make(url, error="q", micro=False)
    qr.save(os.path.join(PASTA, "qrcode.png"), scale=20, border=4, dark=COR_ESCURA, light="white")
    qr.save(os.path.join(PASTA, "qrcode.svg"), scale=10, border=4, dark=COR_ESCURA, light="white")
    qr_svg = qr.svg_inline(scale=10, border=4, dark=COR_ESCURA, light="white", omitsize=True)

    with open(os.path.join(RAIZ, "static", "img", "logo.svg"), encoding="utf-8") as arquivo:
        logo_svg = arquivo.read()

    ambiente = Environment(
        loader=FileSystemLoader(PASTA),
        autoescape=select_autoescape(["html"]),
    )
    html = ambiente.get_template("modelo.html").render(
        destaque=dados_do_doce(DESTAQUE),
        extras=[dados_do_doce(i) for i in EXTRAS],
        qr_svg=Markup(qr_svg),  # já é HTML pronto: Markup impede o Jinja de escapar
        logo_svg=Markup(logo_svg),
        url_curta=SITE.replace("https://", "").rstrip("/"),
    )
    with open(os.path.join(PASTA, "cartaz.html"), "w", encoding="utf-8") as arquivo:
        arquivo.write(html)

    print("Cartaz gerado em cartaz/cartaz.html")
    print("QR aponta para:", url)
    print("Módulos do QR:", qr.symbol_size(border=0)[0], "x", qr.symbol_size(border=0)[1])


if __name__ == "__main__":
    main()
