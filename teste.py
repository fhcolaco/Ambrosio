import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

# Criar a janela principal com estilo moderno
janela = tk.Tk()
janela.title("App Moderna com Dropdown e Mapa")
janela.geometry("800x600")
janela.configure(bg="#f5f5f5")

# Estilos
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 14), background="#f5f5f5")
style.configure('TCombobox', font=('Helvetica', 12), padding=5)

# Cabeçalho
cabecalho = ttk.Label(janela, text="App Moderna com Dropdown e Mapa", font=('Helvetica', 20, 'bold'))
cabecalho.pack(pady=15)

# Dropdown (Combobox)
opcoes = ["Lisboa, Portugal", "Porto, Portugal", "Coimbra, Portugal", "Faro, Portugal"]
local_selecionado = tk.StringVar()
dropdown = ttk.Combobox(janela, textvariable=local_selecionado, values=opcoes, state="readonly")
dropdown.current(0)
dropdown.pack(pady=10)

# Mapa
def atualizar_mapa(event):
    local = dropdown.get()
    mapa.set_address(local, marker=True)

mapa = TkinterMapView(janela, width=750, height=400, corner_radius=0)
mapa.pack(pady=20)

# Inicializar mapa com a localização inicial
mapa.set_address(opcoes[0], marker=True)

# Associar evento de mudança ao dropdown
dropdown.bind('<<ComboboxSelected>>', atualizar_mapa)

# Rodapé
rodape = ttk.Label(janela, text="© 2025 App Moderna")
rodape.pack(side="bottom", pady=10)

# Iniciar a aplicação
janela.mainloop()
