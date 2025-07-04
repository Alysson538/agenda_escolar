import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os

if not os.path.exists("data"):
    os.makedirs("data")

conn = sqlite3.connect("data/agenda.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data TEXT NOT NULL,
        prioridade TEXT
    )
''')
conn.commit()

def adicionar_tarefa():
    titulo = entrada_titulo.get()
    descricao = entrada_descricao.get()
    data = entrada_data.get()
    prioridade = var_prioridade.get()

    if not titulo or not data:
        messagebox.showwarning("Aviso", "Título e Data são obrigatórios!")
        return

    try:
        datetime.strptime(data, "%Y/%m/%d")
    except ValueError:
        messagebox.showerror("Erro", "Data inválida! Use o formato YYYY/MM/DD")
        return

    c.execute("INSERT INTO tarefas (titulo, descricao, data, prioridade) VALUES (?, ?, ?, ?)",
              (titulo, descricao, data, prioridade))
    conn.commit()
    listar_tarefas()
    limpar_campos()

def listar_tarefas():
    lista_tarefas.delete(0, tk.END)
    c.execute("SELECT id, titulo, data, prioridade FROM tarefas ORDER BY data")
    for row in c.fetchall():
        lista_tarefas.insert(tk.END, f"{row[0]} - {row[1]} | {row[2]} | Prioridade: {row[3]}")

def limpar_campos():
    entrada_titulo.delete(0, tk.END)
    entrada_descricao.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    var_prioridade.set("Média")

janela = tk.Tk()
janela.title("Organizador de Estudos")
janela.geometry("500x500")

tk.Label(janela, text="Título da Tarefa:").pack()
entrada_titulo = tk.Entry(janela, width=50)
entrada_titulo.pack()

tk.Label(janela, text="Descrição:").pack()
entrada_descricao = tk.Entry(janela, width=50)
entrada_descricao.pack()

tk.Label(janela, text="Data (YYYY/MM/DD):").pack()
entrada_data = tk.Entry(janela, width=20)
entrada_data.pack()

tk.Label(janela, text="Prioridade:").pack()
var_prioridade = tk.StringVar(value="Média")
tk.OptionMenu(janela, var_prioridade, "Alta", "Média", "Baixa").pack()

tk.Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa).pack(pady=10)

tk.Label(janela, text="Tarefas Cadastradas:").pack()
lista_tarefas = tk.Listbox(janela, width=70)
lista_tarefas.pack()

listar_tarefas()
janela.mainloop()

conn.close()
