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
static/img/       logo da Doce Pausa
static/video/     coloque aqui o vídeo da equipe
```

## Aviso

Este é um projeto escolar de conscientização. Use só com autorização do professor e dentro da escola.
Evite publicar o site na internet: páginas com formulário de login falso costumam ser marcadas como golpe
pelos navegadores e pelas hospedagens.
