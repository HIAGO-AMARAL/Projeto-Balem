from flask import Flask, render_template, request, session
from datetime import datetime

app = Flask(__name__)

# Necessário para utilizar a sessão
app.secret_key = "chave-simulacao-brownie"

# Dados temporários da pesquisa
registros = []


@app.route("/")
def index():
    # A versão pode ser A ou B:
    # A = vantagem financeira
    # B = mensagem neutra

    versao = request.args.get("versao", "A").upper()

    if versao not in ["A", "B"]:
        versao = "A"

    session["versao"] = versao

    return render_template("index.html", versao=versao)


@app.route("/produto")
def produto():
    versao = session.get("versao", "A")

    return render_template(
        "produto.html",
        versao=versao
    )


@app.route("/adicionar", methods=["POST"])
def adicionar():
    quantidade = int(request.form.get("quantidade", 1))

    session["quantidade"] = quantidade

    return render_template(
        "carrinho.html",
        quantidade=quantidade,
        preco=5.00,
        total=quantidade * 5.00
    )


@app.route("/finalizar", methods=["POST"])
def finalizar():

    versao = session.get("versao", "A")

    # Registro mínimo e anônimo
    registro = {
        "versao": versao,
        "converteu": True,
        "timestamp": datetime.now().isoformat()
    }

    registros.append(registro)

    return render_template(
        "educativo.html",
        versao=versao
    )


@app.route("/resultado")
def resultado():

    total_a = 0
    conversoes_a = 0

    total_b = 0
    conversoes_b = 0

    for registro in registros:

        if registro["versao"] == "A":
            total_a += 1

            if registro["converteu"]:
                conversoes_a += 1

        elif registro["versao"] == "B":
            total_b += 1

            if registro["converteu"]:
                conversoes_b += 1

    taxa_a = 0
    taxa_b = 0

    if total_a > 0:
        taxa_a = (conversoes_a / total_a) * 100

    if total_b > 0:
        taxa_b = (conversoes_b / total_b) * 100

    return render_template(
        "resultado.html",
        total_a=total_a,
        conversoes_a=conversoes_a,
        taxa_a=round(taxa_a, 2),
        total_b=total_b,
        conversoes_b=conversoes_b,
        taxa_b=round(taxa_b, 2)
    )


if __name__ == "__main__":
    app.run(debug=True)