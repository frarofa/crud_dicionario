from flask import Flask, render_template, request, redirect, url_for 
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
@app.route("/produto/<int:id>", methods=["GET"])
def exibir_produto(id):
    if id==0: #estamos verificando se o id recebido foi ZERO
        id = repositorio.gerar_id() #caso tenha sido ZERO, vamos gerar um novo id, pois é sinal de que estão querendo criar um novo produto (essa combinação de que 0 = novo produto foi feita por nós)

    produto = repositorio.retornar_produto(id)
    produto['id'] = id
    return render_template('cadastro.html', **produto)

#Abrir o template cadastro.html apenas com o id preenchido para permitir novo cadastro
#Dar função aos botões excluir e salvar no template cadastro.html
@app.route("/produto/<int:id>", methods=["POST"])
#A linha acima indica que a mesma rota que já haviamos criado antes foi recriada com o metodo POST, ou seja, quando o usuário enviar dados
def editar_produto(id):
    if "excluir" in request.form:        
        #Aqui estamos verificando que "excluir" está contido na requisão, ou seja, o usuário clicou no botão excluir do formulário
        repositorio.remover_produto(id)
        
    elif "salvar" in request.form:        
        #Aqui estamos verificando que "salvar" está contido na requisão, ou seja, o usuário clicou no botão salvar do formulário
        produto = {} #Criando um dicionário vazio para conter os dados do produto que será salvo
        produto["nome"] = request.form["nome"] #Colocamos no dicionario o conteudo que veio do formulario
        produto["descricao"] = request.form["descricao"]
        produto["preco"] = request.form["preco"]
        produto["imagem"] = request.form["imagem"]

        #Precisamos definir se vou SALVAR um novo produto ou ATUALIZAR um produto já existente
        produtos = repositorio.retornar_produtos()
        #Vamos testar se o id do produto está no dicionário que contem todos eles
        if id in produtos.keys():
            repositorio.atualizar_produto(id, produto) #Caso o id já exista, vamos chamar a função atualizar_produto indicando o id e os novos dados
        else:
            repositorio.criar_produto(**produto) #Caso a id não existam vamos chamar a função criar_produto passando os dados do dicionário
            #Podemos fazer da seguinte forma -> repositorio.criar_produto(nome=produto['nome'], descricao=produto['descricao'], preco=produto['preco'], imagem=produto['imagem'])
    return redirect(url_for('listagem_produtos'))
    


app.run(debug=True)