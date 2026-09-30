"""Gera a versão estática da Doce Pausa na pasta docs/, pronta para o GitHub Pages.

Uso (dentro da pasta do projeto, com o ambiente virtual ativado):

    python gerar_estatico.py

O que o script faz:
  * lê o catálogo (catalogo.py), o vídeo (VIDEO_ARQUIVO / VIDEO_YOUTUBE em app.py),
    o CSS e as fotos (pasta static/);
  * monta as páginas a partir dos modelos da pasta estatico/;
  * escreve tudo em docs/ (esta pasta é APAGADA e refeita a cada execução, então
    não edite nada dentro dela: mude os arquivos de origem e rode o script de novo).

A versão estática não tem servidor: o carrinho e o login funcionam dentro do
navegador de quem visita (veja estatico/loja.js) e nada é enviado para lugar nenhum.
"""

import json
import os
import re
import shutil
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app import (
    VIDEO_ARQUIVO,
    VIDEO_YOUTUBE,
    arquivo_de_video_existe,
    foto_do_doce,
    formatar_real,
    link_youtube_embed,
)
from catalogo import CATEGORIAS, DOCES

# ---------------------------------------------------------------------------
# CONTADOR DE ACESSOS (GoatCounter): gratuito, sem cookies e sem dados pessoais.
#
#   1. Crie uma conta grátis em https://www.goatcounter.com/signup e escolha um
#      "site code" (ex.: docepausa). Ele vira o endereço https://docepausa.goatcounter.com
#   2. Escreva esse código aqui embaixo e rode o script de novo.
#   3. Veja os acessos no painel do GoatCounter, em https://SEUCODIGO.goatcounter.com
#
# Deixe vazio ("") para gerar o site sem contador.
# ---------------------------------------------------------------------------
GOATCOUNTER_CODIGO = "docepausa"

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIGEM_STATIC = os.path.join(RAIZ, "static")
ORIGEM_MODELOS = os.path.join(RAIZ, "estatico")
SAIDA = os.path.join(RAIZ, "docs")

PAGINAS = ["index", "carrinho", "entrar", "ops"]


def copiar_arquivos():
    """Copia CSS, imagens, vídeo e JavaScript para docs/assets/."""
    assets = os.path.join(SAIDA, "assets")

    shutil.copytree(os.path.join(ORIGEM_STATIC, "css"), os.path.join(assets, "css"))
    shutil.copytree(
        os.path.join(ORIGEM_STATIC, "img"),
        os.path.join(assets, "img"),
        ignore=shutil.ignore_patterns(".gitkeep", "*.md"),
    )

    os.makedirs(os.path.join(assets, "js"))
    shutil.copy(os.path.join(ORIGEM_MODELOS, "loja.js"), os.path.join(assets, "js", "loja.js"))

    if arquivo_de_video_existe():
        os.makedirs(os.path.join(assets, "video"))
        shutil.copy(
            os.path.join(ORIGEM_STATIC, "video", VIDEO_ARQUIVO),
            os.path.join(assets, "video", VIDEO_ARQUIVO),
        )


def video_para_a_pagina():
    """Mesma escolha do site Flask, mas com caminho relativo (funciona no GitHub Pages)."""
    if arquivo_de_video_existe():
        return {"tipo": "arquivo", "src": f"assets/video/{VIDEO_ARQUIVO}"}
    embed = link_youtube_embed(VIDEO_YOUTUBE)
    if embed:
        return {"tipo": "youtube", "src": embed}
    return None


def montar_dados():
    """Catálogo com o caminho da foto de cada doce (ou None se ainda não tem)."""
    return [dict(doce, foto=foto_do_doce(doce["id"])) for doce in DOCES]


def main():
    if GOATCOUNTER_CODIGO and not re.fullmatch(r"[a-z0-9-]+", GOATCOUNTER_CODIGO):
        sys.exit("GOATCOUNTER_CODIGO inválido: use só letras minúsculas, números e hífen.")

    if os.path.isdir(SAIDA):
        shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    copiar_arquivos()

    ambiente = Environment(
        loader=FileSystemLoader(ORIGEM_MODELOS),
        autoescape=select_autoescape(["html"]),
    )
    ambiente.filters["brl"] = formatar_real

    doces = montar_dados()
    contexto = {
        "doces": doces,
        "categorias": CATEGORIAS,
        "doces_dados": {d["id"]: d for d in doces},
        "video": video_para_a_pagina(),
        "goatcounter": GOATCOUNTER_CODIGO,
    }

    for pagina in PAGINAS:
        html = ambiente.get_template(f"{pagina}.html").render(**contexto)
        with open(os.path.join(SAIDA, f"{pagina}.html"), "w", encoding="utf-8") as arquivo:
            arquivo.write(html)

    # Impede o GitHub Pages de processar a pasta com Jekyll.
    open(os.path.join(SAIDA, ".nojekyll"), "w").close()

    fotos = sum(1 for d in doces if d["foto"])
    print(f"Site gerado em docs/  ({len(PAGINAS)} páginas, {len(doces)} doces, {fotos} com foto)")
    video = contexto["video"]
    print("Vídeo:", video["tipo"] if video else "espaço reservado (nenhum vídeo configurado)")
    print("Contador de acessos:", f"GoatCounter ({GOATCOUNTER_CODIGO})" if GOATCOUNTER_CODIGO else "desligado")


if __name__ == "__main__":
    main()
