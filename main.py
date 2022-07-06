

from calendar import day_abbr
import json
import sqlite3 as db
import random
import PySimpleGUI as sg
from hashlib import md5


def cadastro(usuario,senha):
    dataBase = db.connect('Banco.db')
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM players WHERE usuario = '{usuario}'")
    row = cursor.fetchone()
    if row == None:
        janela2.hide()
        janela1.un_hide()
        senha = senha.encode('utf-8')
        senha = md5(senha).hexdigest()
        cursor.execute(f"INSERT INTO players VALUES ('{usuario}','{senha}',0,0)")
        dataBase.commit()
        janela1['texto2'].update("Cadastro realizado com sucesso, agora basta logar")
    else:
        janela2['texto1'].update('Este usuario ja existe')
        


def login(usuario,senha):
    senha = senha.encode("utf-8")
    senha = md5(senha).hexdigest()
    dataBase = db.connect("Banco.db")    
    cursor = dataBase.cursor()
    cursor.execute(f"SElECT senha FROM players WHERE '{senha}' == senha and '{usuario}' == usuario")
    row = cursor.fetchone()
    if row == None:
        print('Usuario ou senha incorretos')
    else:
        print('usuario escontrado')


def janela_login():
    layout = [
        [sg.Text("Usuario"),sg.Input('',key='usuario_login')],
        [sg.Text('Senha'),sg.Input('',key='senha_login',password_char="*")],
        [sg.Button('Logar')],
        [sg.Text("Não tem conta?",key='texto3'),sg.Button('Crie',)],
        [sg.Text('',key='texto2')]
    ]
    return sg.Window('Login',layout=layout,finalize=True)

def janela_cadastro():
    layout = [
        [sg.Text('Crie um usuario'),sg.Input('',key="usuario_cadastro")],
        [sg.Text('Crie uma senha'),sg.Input('',key="senha_cadastro",password_char="*")],
        [sg.Text('Confirmar senha'),sg.Input('',key="senha_confirm",password_char="*")],
        [sg.Button('Registrar')],
        [sg.Text('',key='texto1')],
        [sg.Text('Ja tem uma conta?'),sg.Button('Login')]
    ]
    return sg.Window('Registro',layout=layout,finalize=True)

janela1,janela2 = janela_login(),None

while True:
    window,events,values = sg.read_all_windows()
    if window == janela1 and events == sg.WINDOW_CLOSED:
        break
    if window == janela2 and events == sg.WINDOW_CLOSED:
        break
    if window == janela1 and events == "Crie":
        janela1.hide()
        janela2 = janela_cadastro()
    if window == janela2 and events == 'Login':
        janela2.hide()
        janela1.un_hide()
    if window == janela2 and events == 'Registrar':
        usuario_c = values['usuario_cadastro']
        senha_cadastro = values['senha_cadastro']
        senha_confirm = values['senha_confirm']
        if senha_cadastro == senha_confirm:
            quantidade = []
            for i in senha_cadastro:
                quantidade.append(i)
            if len(quantidade) >= 4:
                cadastro(usuario_c,senha_cadastro)
            else:
                janela2['texto1'].update('No minimo 8 caracteres')
        else:
            janela2['texto1'].update("As senhas não correspondem")
            janela2['senha_cadastro'].update('')
            janela2['senha_confirm'].update('')
    if window == janela1 and events == 'Logar':
        usuario = values["usuario_login"]
        senha = values["senha_login"]
        login(usuario,senha)
janela1.close()
janela2.close()
