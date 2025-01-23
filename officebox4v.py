from tkinter import *
import tkinter as tk
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox, simpledialog
import sqlite3 as lite
from datetime import datetime

# Configuração das cores
co1 ="#3E5641" # verde escuro
co2 ="#A24936" # laranja escuro
co3 ="#D36135" # laranja claro
co4 ="#282B28" # cinza chumbo
co5 ="#83BCA9" # azul celeste
co6 ="#F4EDEA" # branco
co7 ="#14110F" # preto

# Criando a janela
janela = Tk()
janela.title("REGISTRO DE INVENTÁRIO BONIFÁCIO RAUSCH")
janela.geometry('900x650')
janela.configure(background=co1)
janela.resizable(width=True, height=True)

style = ttk.Style(janela)
style.theme_use("vista")

# Criando a conexão com o banco de dados
con = lite.connect('dados.db')
with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Inventario(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, local TEXT, descricao TEXT, marca TEXT, data_da_compra DATE, valor_da_compra DECIMAL, serie TEXT, imagem TEXT)"
    )

# Frames
frameCima = Frame(janela, width=900, height=75, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=303, bg=co4, pady=20, relief="flat")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

framebaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
framebaixo.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

# Função para criar Labels e Entries
def criar_label_entry(frame, text, row, column, pady=(10, 0), padx=(10, 10 )):
    label = Label(frame, text=text, height=1, anchor=NW, font=('Ivy 10 bold'), bg=co4, fg=co6)
    label.grid(row=row, column=column, pady=pady, padx=padx, sticky=W)
    entry = Entry(frame, width=30, justify='left', relief="solid")
    entry.grid(row=row, column=column+1, pady=pady, padx=padx, sticky=W)
    return entry

# Criando Labels e Entries
e_nome = criar_label_entry(frameMeio, "Produto", 0, 0)
e_local = criar_label_entry(frameMeio, "Setor", 1, 0)
e_descricao = criar_label_entry(frameMeio, "Descrição", 2, 0)
e_model = criar_label_entry(frameMeio, "Marca/Modelo", 3, 0)
e_cal = criar_label_entry(frameMeio, "Data da compra", 4, 0)
e_valor = criar_label_entry(frameMeio, "Valor da compra", 5, 0)
e_serial = criar_label_entry(frameMeio, "N° Nota Fiscal", 6, 0)

# Botões
botao_inserir = Button(frameMeio, text="ADICIONAR", width=40, overrelief=RIDGE, font=('ivy 8'), bg=co1, fg=co6)
botao_inserir.grid(row=0, column=2, pady=1)

botao_editar = Button(frameMeio, text="EDITAR", width=40, overrelief=RIDGE, font=('ivy 8'), bg=co1, fg=co6)
botao_editar.grid(row=1, column=2, pady=1)

botao_ver = Button(frameMeio, text="VER ITEM", width=40, overrelief=RIDGE, font=('ivy 8'), bg=co1, fg=co6)
botao_ver.grid(row=2, column=2, pady=1)

# Campo de busca e botão de busca
l_busca_nome = Label(frameCima, text="Buscar por nome:", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co6)
l_busca_nome.place(x=10, y=10)

e_busca_nome = Entry(frameCima, width=30, justify='left', relief="solid")
e_busca_nome.place(x=150, y=11)

def buscar():
    nome = e_busca_nome.get()

    if nome.strip() != '':
        # Limpar Treeview antes de mostrar os resultados da busca
        for item in tree.get_children():
            tree.delete(item)

        # Realizar a busca no banco de dados
        query = "SELECT * FROM Inventario WHERE nome LIKE ?"
        params = ('%' + nome + '%',)
        cur.execute(query, params)

        # Atualizar Treeview com os resultados da busca
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)

        messagebox.showinfo('Busca Concluída', 'Busca realizada com sucesso!')
    else:
        messagebox.showwarning('Campo Vazio', 'Por favor, insira um nome para buscar.')

# Botão de busca
botao_buscar = Button(frameCima, text="BUSCAR", width=15, overrelief=RIDGE, font=('ivy 8'), bg=co4, fg='#feffff', command=buscar)
botao_buscar.place(x=370, y=10)

# Função para mostrar itens no Treeview
def mostrar():
    tabela_head = ['Id', 'Produto', 'Setor', 'Descrição', 'Marca/Modelo', 'Data da compra', 'Valor da compra', 'N° Nota Fiscal']

    global tree

    tree = ttk.Treeview(framebaixo, selectmode="extended", columns=tabela_head, show="headings")

    vsb = ttk.Scrollbar(framebaixo, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(framebaixo, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    framebaixo.grid_rowconfigure(0, weight=12)

    hd = ["center", "center", "center", "center", "center", "center", "center", 'center']
    h = [40, 150, 100, 160, 130, 100, 100, 100]
    n = 0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in cur.execute("SELECT * FROM Inventario"):
        tree.insert('', 'end', values=item)

mostrar()

# Função para inserir itens no banco de dados e Treeview
def inserir():
    nome = e_nome.get()
    local = e_local.get()
    descricao = e_descricao.get()
    model = e_model.get()
    data = e_cal.get()
    valor = e_valor.get()
    serie = e_serial.get()
    imagem = ''  # Placeholder para a imagem

    if nome == '' or local == '' or descricao == '' or model == '' or data == '' or valor == '' or serie == '':
        messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
    else:
        with con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Inventario (nome, local, descricao, marca, data_da_compra, valor_da_compra, serie, imagem) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (nome, local, descricao, model, data, valor, serie, imagem)
            )
            con.commit()
        mostrar()
        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

        e_nome.delete(0, 'end')
        e_local.delete(0, 'end')
        e_descricao.delete(0, 'end')
        e_model.delete(0, 'end')
        e_cal.delete(0, 'end')
        e_valor.delete(0, 'end')
        e_serial.delete(0, 'end')

botao_inserir.config(command=inserir)

# Função para redefinir a função do botão "EDITAR" para a função original de edição
def redefinir_botao_editar():
    botao_editar.config(command=editar)

def editar():
    try:
        tree_data = tree.focus()
        tree_values = tree.item(tree_data, 'values')
        
        if tree_values:
            # Preencher os campos de entrada com os valores selecionados
            e_nome.delete(0, 'end')
            e_nome.insert(0, tree_values[1])
            
            e_local.delete(0, 'end')
            e_local.insert(0, tree_values[2])
            
            e_descricao.delete(0, 'end')
            e_descricao.insert(0, tree_values[3])
            
            e_model.delete(0, 'end')
            e_model.insert(0, tree_values[4])
            
            e_cal.delete(0, 'end')
            e_cal.insert(0, tree_values[5])
            
            e_valor.delete(0, 'end')
            e_valor.insert(0, tree_values[6])
            
            e_serial.delete(0, 'end')
            e_serial.insert(0, tree_values[7])
            
            # Função para salvar as alterações
            def salvar_alteracoes():
                e_nome_value = e_nome.get()
                e_local_value = e_local.get()
                e_descricao_value = e_descricao.get()
                e_model_value = e_model.get()
                e_cal_value = e_cal.get()
                e_valor_value = e_valor.get()
                e_serial_value = e_serial.get()
                
                if (not e_nome_value or not e_local_value or not e_descricao_value or 
                    not e_model_value or not e_cal_value or not e_valor_value or not e_serial_value):
                    messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
                else:
                    with con:
                        cur = con.cursor()
                        cur.execute(
                            "UPDATE Inventario SET nome=?, local=?, descricao=?, marca=?, data_da_compra=?, valor_da_compra=?, serie=? WHERE id=?",
                            (e_nome_value, e_local_value, e_descricao_value, e_model_value, e_cal_value, e_valor_value, e_serial_value, tree_values[0])
                        )
                        con.commit()

                    mostrar()
                    messagebox.showinfo('Sucesso', 'Os dados foram atualizados com sucesso')

                    e_nome.delete(0, 'end')
                    e_local.delete(0, 'end')
                    e_descricao.delete(0, 'end')
                    e_model.delete(0, 'end')
                    e_cal.delete(0, 'end')
                    e_valor.delete(0, 'end')
                    e_serial.delete(0, 'end')

                    # Redefinir a função do botão "EDITAR" para a função original de edição
                    botao_editar.config(command=editar)
                    
            # Substituir a função do botão "EDITAR" para salvar as alterações
            botao_editar.config(command=salvar_alteracoes)
            
        else:
            messagebox.showerror('Erro', 'Selecione um item na tabela para editar')
        
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao tentar editar o item: {str(e)}')

botao_editar.config(command=editar)

# Função para redefinir o banco de dados
def redefinir_bd():
    senha = simpledialog.askstring("Redefinir Banco de Dados", "Digite a senha para redefinir o banco de dados:", show='*')
    
    if senha == '354060':  ####Substitua pela senha desejada ######
        try:
            with con:
                cur.execute("DROP TABLE IF EXISTS Inventario")
                cur.execute(
                    "CREATE TABLE Inventario(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, local TEXT, descricao TEXT, marca TEXT, data_da_compra DATE, valor_da_compra DECIMAL, serie TEXT, imagem TEXT)"
                )
            mostrar()
            messagebox.showinfo('Sucesso', 'O banco de dados foi redefinido com sucesso.')
        except Exception as e:
            messagebox.showerror('Erro', f'Ocorreu um erro ao redefinir o banco de dados: {str(e)}')
    else:
        if senha is not None:  # Check if user canceled the input dialog
            messagebox.showerror('Senha Incorreta', 'Senha incorreta. Tente novamente.')

# Botão para redefinir o banco de dados
botao_redefinir_bd = Button(frameCima, text="Redefinir BD", width=15, overrelief=RIDGE, font=('ivy 8'), bg=co2, fg='#feffff', command=redefinir_bd)
botao_redefinir_bd.place(x=500, y=10)

# Botão para limpar o filtro de busca
def limpar_filtro():
    e_busca_nome.delete(0, 'end')  # Limpa o campo de busca
    mostrar()  # Atualiza o Treeview para mostrar todos os itens novamente

botao_limpar_filtro = Button(frameCima, text="Limpar Filtro", width=15, overrelief=RIDGE, font=('ivy 8'), bg=co4, fg='#feffff', command=limpar_filtro)
botao_limpar_filtro.place(x=12, y=35)

# Função para ver detalhes de um item
def ver():
    try:
        tree_data = tree.focus()
        tree_values = tree.item(tree_data, 'values')

        messagebox.showinfo('Informação', f'Produto: {tree_values[1]}\nSetor: {tree_values[2]}\nDescrição: {tree_values[3]}\nMarca/Modelo: {tree_values[4]}\nData da compra: {tree_values[5]}\nValor da compra: {tree_values[6]}\nN° Nota Fiscal: {tree_values[7]}')

    except:
        messagebox.showerror('Erro', 'Selecione um item na tabela para ver')

botao_ver.config(command=ver)

janela.mainloop()
