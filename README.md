# Doce Pausa 🧁

Simulação de **phishing** feita para a nota bimestral de **segurança da informação**.

A ideia é uma loja de doces com preços absurdos (torta de limão de R$ 6,00 por R$ 2,00).
Quando a pessoa clica em **Finalizar compra**, ela cai numa página com o vídeo da equipe
explicando que caiu num phishing e como se proteger.

> **Nenhum dado é coletado.** O site não tem banco de dados. O e-mail e a senha do login são
> só encenação: os campos não têm o atributo `name`, então o navegador nem envia o que foi digitado.

## Fluxo da simulação

1. A pessoa entra na loja e escolhe os doces.
2. Vai para o carrinho e clica em **Finalizar compra**.
3. A loja pede login (qualquer e-mail e senha funcionam, e nada é guardado).
4. Ao clicar em **Finalizar compra** de novo, aparece a página `/ops` com o vídeo e as dicas.

## Como rodar

Precisa do [Python 3.10+](https://www.python.org/downloads/). No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\activate        # no Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra <http://127.0.0.1:5000>.

### Deixar a turma acessar pela rede da escola

Rode com o servidor aberto para a rede local (PowerShell):

```powershell
$env:HOST = "0.0.0.0"
python app.py
```

Descubra o IP do seu computador com `ipconfig` e passe `http://SEU-IP:5000` para o pessoal.
Se o Windows perguntar sobre o firewall, permita o acesso em rede privada.

Não use `FLASK_DEBUG=1` quando o servidor estiver aberto para a rede.

## Onde colocar o vídeo da equipe 🎬

A página educativa já tem o espaço do vídeo pronto. Escolha **uma** das opções em [`app.py`](app.py):

- **Arquivo:** coloque o `.mp4` em `static/video/` e deixe `VIDEO_ARQUIVO` com o mesmo nome do arquivo
  (o padrão é `phishing.mp4`).
- **YouTube:** cole o link em `VIDEO_YOUTUBE` (pode ser o link normal, o `youtu.be` ou o de compartilhar).

Sem nenhum dos dois, a página mostra um espaço reservado no lugar do vídeo. O GitHub não aceita
arquivos com mais de 100 MB, então prefira o YouTube (pode ser "não listado") se o vídeo for pesado.

## Fotos dos doces 📸

As 25 fotos já estão em `static/img/doces/`. Vieram do [Pexels](https://www.pexels.com) (licença livre)
e os créditos estão em [`static/img/doces/CREDITOS.md`](static/img/doces/CREDITOS.md).

Para **trocar** uma foto, salve a nova com o mesmo nome do arquivo da tabela abaixo (também vale
`.jpeg`, `.png` ou `.webp`) e recarregue a página, sem reiniciar o servidor. Se apagar a foto de um
doce, a loja volta a mostrar o emoji dele.

Dicas para a foto vender bem e o projeto não ficar pesado:

- Prefira foto na horizontal, com o doce no centro. O card corta as bordas para caber.
- Deixe com uns 800 px de largura e menos de 200 KB. Foto de celular vem com vários MB, então
  reduza antes (o app Fotos do Windows ou o <https://squoosh.app> fazem isso).
- Use só fotos que vocês tirem ou que tenham licença livre (Pexels, Unsplash, Pixabay).

**Brigadeiros e trufas**

| Doce | Nome do arquivo |
|---|---|
| Brigadeiro tradicional | `brigadeiro.jpg` |
| Beijinho de coco | `beijinho.jpg` |
| Brigadeiro de leite ninho | `brigadeiro-ninho.jpg` |
| Cajuzinho | `cajuzinho.jpg` |
| Trufa de chocolate | `trufa.jpg` |
| Palha italiana | `palha-italiana.jpg` |

**Bolos e tortas**

| Doce | Nome do arquivo |
|---|---|
| Fatia de torta de limão | `torta-limao.jpg` |
| Bolo de cenoura com chocolate | `bolo-cenoura.jpg` |
| Fatia de bolo de chocolate | `bolo-chocolate.jpg` |
| Fatia de torta de morango | `torta-morango.jpg` |
| Pão de mel | `pao-de-mel.jpg` |
| Cupcake de baunilha | `cupcake.jpg` |

**Cookies e biscoitos**

| Doce | Nome do arquivo |
|---|---|
| Cookie de gotas de chocolate | `cookie.jpg` |
| Brownie de chocolate | `brownie.jpg` |
| Casadinho | `casadinho.jpg` |
| Paçoca rolha | `pacoca.jpg` |

**Copinhos e gelados**

| Doce | Nome do arquivo |
|---|---|
| Pudim de leite no copinho | `pudim.jpg` |
| Mousse de maracujá | `mousse-maracuja.jpg` |
| Bolo de pote ninho com morango | `bolo-pote.jpg` |
| Brigadeiro de colher | `brigadeiro-colher.jpg` |
| Sacolé de chocolate | `sacole.jpg` |

**Doces de festa**

| Doce | Nome do arquivo |
|---|---|
| Maçã do amor | `maca-do-amor.jpg` |
| Pipoca doce | `pipoca-doce.jpg` |
| Cocada de forno | `cocada.jpg` |
| Pé de moleque | `pe-de-moleque.jpg` |

## Painel da apresentação

Em `/painel` (sem link no site) aparecem dois contadores: quantas pessoas passaram pelo login e
quantas finalizaram a compra. São só números em memória e voltam a zero quando o servidor reinicia.

## Publicar na internet com o GitHub Pages 🌐

A pasta `docs/` é uma **versão estática** do site (sem servidor): o carrinho e o login funcionam
dentro do navegador de quem visita e nada é enviado para lugar nenhum. Com ela o site fica no ar
de graça, com um endereço fixo, sem precisar do seu computador ligado. Serve para o QR code do cartaz.

### 1. Gerar o site

```bash
python gerar_estatico.py
```

O script refaz a pasta `docs/` inteira a partir do catálogo, das fotos, do CSS e do vídeo. **Não edite
nada dentro de `docs/`**: mude os arquivos de origem (`catalogo.py`, `static/`, `estatico/`) e rode o
script de novo. Depois é só fazer o commit da pasta `docs/`.

### 2. Contar os acessos (GoatCounter)

O GitHub Pages não conta visitas sozinho. Use o [GoatCounter](https://www.goatcounter.com): é grátis,
não usa cookies e não guarda IP nem dado pessoal.

1. Crie uma conta em <https://www.goatcounter.com/signup> e escolha um código (ex.: `docepausa`).
2. Escreva o código em `GOATCOUNTER_CODIGO`, no topo de [`gerar_estatico.py`](gerar_estatico.py).
3. Rode `python gerar_estatico.py` de novo e faça o commit.
4. Veja os números em `https://SEUCODIGO.goatcounter.com`.

No painel, cada página conta uma etapa da simulação:

| Página | O que significa |
|---|---|
| `index.html` | pessoas que abriram a loja (os **acessos**) |
| `entrar.html` | pessoas que chegaram ao login |
| `ops.html` | pessoas que **caíram** no phishing e viram o vídeo |

Acessos feitos no seu próprio computador (`localhost`) não entram na contagem. Teste pelo celular.

### 3. Publicar

1. No GitHub: **Settings → General → Danger Zone → Change visibility → Make public**.
   O GitHub Pages grátis só publica repositórios públicos. Não há nada secreto no código.
2. **Settings → Pages → Build and deployment**: em *Source* escolha **Deploy from a branch**,
   depois a branch `main` e a pasta **`/docs`**, e salve.
3. Depois de 1 a 2 minutos o site aparece em algo como
   `https://hiago-amaral.github.io/Projeto-Balem/`. Esse é o endereço do QR code.

Antes de imprimir o cartaz, abra o link em alguns celulares e no Chrome. Páginas com login falso podem
ser marcadas como golpe pelos navegadores, e o GitHub pode remover o conteúdo. Avise o professor.

**Diferenças da versão estática:** não existe `/painel` (quem conta os acessos é o GoatCounter) e o vídeo
entra na hora de gerar o site (`python gerar_estatico.py` copia o arquivo ou usa o link do YouTube).

## Estrutura

```
app.py            rotas da loja e configuração do vídeo
catalogo.py       lista de doces, categorias e preços
templates/        páginas HTML (base, loja, carrinho, login, educativo, painel)
static/css/       estilo do site
static/js/        filtro, busca, carrinho e cronômetro
static/img/       logo da Doce Pausa; fotos dos doces em static/img/doces/
static/video/     coloque aqui o vídeo da equipe
estatico/         modelos e JavaScript da versão estática
gerar_estatico.py gera a versão estática na pasta docs/
docs/             site pronto para o GitHub Pages (gerado, não edite)
```

## Aviso

Este é um projeto escolar de conscientização. Use só com autorização do professor e dentro da escola.
Ao publicar na internet, teste antes: páginas com formulário de login falso costumam ser marcadas como golpe
pelos navegadores e pelas hospedagens. Depois do evento, tire o site do ar (volte o repositório para privado
ou desligue o Pages).
