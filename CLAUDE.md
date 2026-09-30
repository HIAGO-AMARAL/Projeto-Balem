# Doce Pausa · contexto do projeto

> Leia isto primeiro. Resume tudo o que já foi feito e combinado com o Hiago (dono do projeto),
> para não precisar perguntar de novo. Responda sempre em **português do Brasil**.

## O que é
Trabalho da **nota bimestral de Segurança da Informação**. É uma **simulação de phishing**: uma loja de
doces falsa, a **Doce Pausa**, com preços absurdos (torta de limão de R$ 6,00 por R$ 2,00). A pessoa
escolhe doces, vai ao carrinho, entra num login falso e, ao clicar em **Finalizar compra**, cai na página
`ops.html` (`/ops` no Flask) com o **vídeo da equipe** explicando que caiu num phishing e como se proteger.

- **Não pode ter banco de dados e não pode coletar dado de ninguém.** O login ignora e-mail e senha
  (os campos nem têm `name`). O objetivo é orientar, não roubar dados.
- **Meta da nota:** o site precisa ter **no mínimo 10 acessos**. Por isso há um contador (GoatCounter).
- A rede Wi-Fi da escola é privada (os alunos não acessam), então o QR code aponta para a internet.

## Endereços
- Repositório (público): https://github.com/HIAGO-AMARAL/Projeto-Balem
- **Site no ar:** https://hiago-amaral.github.io/Projeto-Balem/ (GitHub Pages, branch `main`, pasta `/docs`)
- Contador: GoatCounter, código `docepausa`, painel privado em https://docepausa.goatcounter.com
  - `index.html` = acessos · `entrar.html` = chegaram ao login · `ops.html` = caíram no phishing
  - O QR do cartaz usa `?utm_campaign=cartaz`, que aparece no bloco "Campaigns" do painel.

## Como o projeto está organizado
Existem **duas versões** do mesmo site:

| Versão | Onde | Para quê |
|---|---|---|
| Flask | `app.py`, `catalogo.py`, `templates/`, `static/` | rodar localmente (`python app.py`); tem `/painel` de contadores |
| **Estática** | `estatico/` → gera `docs/` | é a que está publicada no GitHub Pages |

- `catalogo.py`: os 25 doces, categorias e preços (fonte única, usada pelas duas versões).
- `static/img/doces/*.jpg`: fotos do Pexels (créditos em `CREDITOS.md` na mesma pasta).
- **`docs/` é gerada** por `python gerar_estatico.py`. **Nunca edite `docs/` à mão.**
  Mude os arquivos de origem (`catalogo.py`, `static/`, `estatico/`) e gere de novo.
- `GOATCOUNTER_CODIGO` fica no topo de `gerar_estatico.py`.
- **Vídeo da equipe:** já colocado em `static/video/phishing.mp4` (30 s, **vertical** 478×850, H.264+AAC, 6,5 MB).
  Em `app.py`, `VIDEO_ARQUIVO` aponta para ele (ou use `VIDEO_YOUTUBE`). Depois de trocar, rode `python gerar_estatico.py`.
  `videoinfo.py` lê o tamanho do MP4; vídeo vertical ganha a caixa `.video--vertical` (9:16). Sem vídeo, aparece um espaço reservado.
  **Cuidado ao testar:** nunca crie/apague arquivos com o nome `phishing.mp4` em testes; use outro nome.
- **Cartaz com QR code:** `python gerar_cartaz.py` gera `cartaz/` (PDF A4, PNG, HTML, QR em PNG e SVG).
  `python gerar_cartaz.py --banner` usa as fotos de `cartaz/fotos-alta/` (Pexels, 3000 px) para a versão de gráfica
  (`cartaz/banner-doce-pausa.pdf`, vetorial, proporção A4). Precisa de `pip install segno`.
  O PDF é gerado com o Edge em modo headless (`--print-to-pdf`, com `--user-data-dir` temporário).

## Ambiente
- Windows 11. Python 3.12 instalado via winget; ambiente virtual em `.venv` (não vai para o Git).
- Testar Flask: `python app.py` → http://127.0.0.1:5000. Testar a estática: `python -m http.server 8000 --directory docs`.
- Para conferir o site publicado sem contar visita no GoatCounter, use `curl` (o contador só conta quando o JavaScript roda).

## Regras de trabalho com o Hiago
- **Sempre em branch + Pull Request. Nunca direto na `main`.** O app bloqueia o `gh pr merge` feito por mim
  ("merge sem revisão"); não contorne: abra o PR e oriente o clique em *Merge pull request → Confirm merge*.
- Dê **passo a passo curto e numerado, com links diretos**. Ele não é especialista em GitHub e às vezes manda print.
- Baixar arquivos, instalar programas e mudar visibilidade/configurações do GitHub: **pedir o ok antes**,
  dizendo fonte, nome e tamanho.
- Commits em português, com a linha de coautoria pedida pelo ambiente.

## Estado (30/09/2026)
Feito e publicado: loja com 25 doces e fotos, carrinho, login falso, página `ops` com dicas, versão estática
no GitHub Pages, GoatCounter ligado. Cartaz A4 com QR code e banner de gráfica gerados, e **vídeo da equipe
incluído** (PR aberto na branch `feature/video-e-banner`; ele já contém o cartaz). O Hiago mandou o banner
para um amigo imprimir.

**Pendências:**
1. **Juntar o PR** (o Hiago clica em Merge) para o vídeo e o cartaz irem ao ar no GitHub Pages; depois conferir o vídeo no site publicado.
2. **Testar no celular com 4G** o link do site (ver se algum navegador mostra tela vermelha de "site enganoso") e conferir no painel do GoatCounter se as visitas aparecem.
3. **Imprimir e colar o cartaz**, com autorização do professor/coordenação, só dentro da escola.
4. **Depois do evento:** voltar o repositório para privado ou desligar o Pages, para o site sair do ar.
5. Guardar prints do painel do GoatCounter (a `index.html` mostra os acessos) para provar os 10 acessos ao professor.
