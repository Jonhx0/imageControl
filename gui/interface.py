import tkinter as tk
from tkinter import messagebox

class URLInputGUI:
    def __init__(self, master, submit_callback):
       self.master = master
       self.master.title("Extrator de Imagem")
       self.master.geometry("500x200")
       self.master.resizable(False, False)
       
       # Configurando layout do grid.
       self.master.columnconfigure(0, weight=1)
       self.master.rowconfigure([0, 1, 2], weight=1)
       
       # Label da URL.
       self.label = tk.Label(master, text="Coloque a URL da notícia:", font=("Arial", 12))
       self.label.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")
       
       # Entrada da URL.
       self.url_var = tk.StringVar()
       self.url_entry = tk.Entry(master, textvariable=self.url_var, width=60, font=("Arial", 12))
       self.url_entry.grid(row=1, column=0, padx=20, pady=10, sticky="we")
       
       # Botão de enviar.
       self.submit_button = tk.Button(master, text="Enviar", command=self.on_submit, font=("Arial", 12))
       self.submit_button.grid(row=2, column=0, padx=20, pady=(10,20), sticky="e")
       
       # Callback.
       self.submit_callback = submit_callback
       
    def on_submit(self):
        url = self.url_var.get().strip()
        if self.validate_url(url):
            self.submit_callback(url)
        else:
            messagebox.showerror("URL inválida", "Entre com uma URL válida.")
            
    @staticmethod
    def validate_url(url):
        # Verificação simples de https.
        return url.startswith("http://") or url.startswith("https://")