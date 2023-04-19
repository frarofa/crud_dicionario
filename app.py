from flask import Flask, render_template
import repositorio

app = Flask(__name__)

#LEMBRE-SE -> 
# Ao obter dados do servidor, a máquina do cliente usa um GET
# Ao enviar dados para o servidor, a máquina do cliente usa um POST

#É preciso criar rotas que levem em conta as seguintes funcionalidades:
#Listar todos os produtos no template index.html
@app.route("/")
def listagem_produtos():
    return render_template('index.html', produtos=repositorio.retornar_produtos())

#Abrir um produto específico (carregando seus dados) no template cadastro.html
@app.route("/produto/<int:id>")
def exibir_produto(id):
    produto = repositorio.retornar_produto(id)
    produto['id'] = id
    return render_template('cadastro.html', **produto)

#Abrir o template cadastro.html apenas com o id preenchido para permitir novo cadastro
#Dar função aos botões excluir e salvar no template cadastro.html
    


app.run(debug=True)