# Doce Pausa 🧁

Simulação de **phishing** feita para a nota bimestral de **segurança cibernética**.

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

Cada doce mostra a foto da pasta `static/img/doces/` quando ela existe. Sem foto, aparece o emoji
do doce, então dá para ir colocando aos poucos.

1. Salve a foto com **exatamente** o nome da tabela abaixo (também vale `.jpeg`, `.png` ou `.webp`).
2. Coloque em `static/img/doces/` e recarregue a página (não precisa reiniciar o servidor).

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

## Estrutura

```
app.py            rotas da loja e configuração do vídeo
catalogo.py       lista de doces, categorias e preços
templates/        páginas HTML (base, loja, carrinho, login, educativo, painel)
static/css/       estilo do site
static/js/        filtro, busca, carrinho e cronômetro
static/img/       logo da Doce Pausa; fotos dos doces em static/img/doces/
static/video/     coloque aqui o vídeo da equipe
```

## Aviso

Este é um projeto escolar de conscientização. Use só com autorização do professor e dentro da escola.
Evite publicar o site na internet: páginas com formulário de login falso costumam ser marcadas como golpe
pelos navegadores e pelas hospedagens.
