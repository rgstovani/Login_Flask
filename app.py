from flask import Flask, render_template, request, redirect, session, flash, url_for
import sys
sys.path.append('./app')
from funcoes import *
from validador_cpf import *
from calculadorafrete import *
from cotador import *
import os


app = Flask(__name__)
app.secret_key = 'testeflaskhtml'
cria_bd()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/index')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('login'))


@app.route('/autenticar', methods=['POST'])
def autenticar():
    login = teste_login(request.form.get('usuario'), request.form.get('senha'))

    if login is False:
        flash('Usuario/Senha inválidos.')
        return redirect(url_for('login'))
    if login is True:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ', login bem sucedido.')
        return render_template('index.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.form.get('senha') == request.form.get('repetesenha'):
        if (adiciona_usuario_bd(request.form.get('nome'),
                            request.form.get('email'),
                            request.form.get('usuario'),
                            request.form.get('senha'))) is not False:
            flash('Cadastrado com sucesso.')
            return redirect(url_for('login'))
        else:
            flash('Usuario ja está cadastrado na base de dados.')
            return render_template('cadastro.html')

    else:
        flash('As senhas digitadas não coincidem')
        return render_template('cadastro.html')


@app.route('/esqueciasenha')
def esqueciasenha():
    return render_template('esqueciasenha.html')


@app.route('/autenticar_troca', methods=['POST'])
def autenticar_troca_senha():
    teste = esquecisenha_bd(request.form.get('email'), request.form.get('usuario'))

    if teste is True:
        session['usuario_logado'] = request.form['usuario']
        return render_template('alterarsenha.html')

    else:
        return render_template('esqueciasenha.html')


@app.route('/alterarsenha', methods=['POST', 'GET'])
def alterarsenha():
    if request.form.get('senha') == request.form.get('repetesenha'):
        usuario = str(session['usuario_logado'])
        senha = str(request.form.get('senha'))

        altera_senha_bd(usuario, senha)
        flash('Senha alterada com sucesso.')
        return redirect(url_for('login'))
    else:
        flash('Senha não alterada.')
        return render_template('alterarsenha.html')


@app.route('/cpf', methods=['POST', 'GET'])
def cpf():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('cpf.html')


@app.route('/validacpf', methods=['POST', 'GET'])
def validacpf():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    cpf = request.form.get('cpf')
    resultado = validador_cpf(cpf)
    return render_template('cpf.html', resultado=resultado)


@app.route('/calculadorafrete', methods=['POST', 'GET'])
def calculadorafrete():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('calculadorafrete.html')


@app.route('/pesquisaendereco', methods=['POST', 'GET'])
def pesquisaendereco():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))


    ponto1 = request.form.get('origem')
    ponto2 = request.form.get('destino')

    resultado = consulta_endereco(ponto1, ponto2)
    flash('Pesquisa Efetuada')

    origem = f'De: {resultado[0]}'
    destino = f'Para: {resultado[1]}'
    km = f'KM: {resultado[2]}'
    duracao = f'Duração: {resultado[3]}'

    session['km'] = km

    return render_template('calculadorafrete.html', origem=origem,
                           destino=destino, km=km, duracao=duracao)

@app.route('/calculafrete', methods=['POST', 'GET'])
def calculafrete():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    flash('Calculo Efetuado')

    km2 = float(session['km'].split(": ")[1])
    valorkm = float(request.form.get('valorkm'))

    valorfrete = "{:.2f}".format(km2 * valorkm)
    return render_template('calculadorafrete.html', valorfrete=valorfrete, km2=km2)


@app.route('/cotadordemoedas', methods=['POST', 'GET'])
def cotadordemoedas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('cotadordemoedas.html')

@app.route('/cotarmoeda', methods=['POST', 'GET'])
def cotarmoeda():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    moedaescolhida = str(request.form.get('moedaescolhida'))
    valor_cotado = cotar(moedaescolhida)
    flash('Cotação efetuada com sucesso.')
    cotacao = f'O valor da {moedaescolhida} é de {valor_cotado}.'

    return render_template('cotadordemoedas.html', cotacao=cotacao)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)