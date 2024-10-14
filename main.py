import tkinter as tk
from gui.interface import URLInputGUI
from utils.fetcher import fetch_webpage
from utils.parser import parse_image_urls
from utils.image_processor import download_and_resize_image
from tkinter import messagebox, Label, Button, Radiobutton, IntVar
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ImageSelectionGUI:
    def __init__(self, root, image_urls):
        self.root = root
        self.image_urls = image_urls
        self.selected_image_index = IntVar()
        self.images = []

        self.label = Label(root, text="Selecione uma das imagens abaixo.")
        self.label.pack(pady=10)

        self.display_thumbnails()

        self.submit_button = Button(root, text="Download da Imagem Selecionada", command=self.handle_image_selection)
        self.submit_button.pack(pady=10)

    def display_thumbnails(self):

        for idx, image_url in enumerate(self.image_urls):
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                img_data = BytesIO(response.content)

                img = Image.open(img_data)
                img.thumbnail((200, 200))
                img_tk = ImageTk.PhotoImage(img)

                self.images.append(img_tk)

                label = Label(self.root, image=img_tk)
                label.pack(pady=5)

                Radiobutton(
                    self.root,
                    text=f"Imagem {idx + 1}",
                    variable=self.selected_image_index,
                    value=idx
                ).pack()
            except Exception as e:
                print(f"Falha ao carregar a imagem {image_url}: {e}")

    def handle_image_selection(self):

        selected_idx = self.selected_image_index.get()
        if selected_idx < 0 or selected_idx >= len(self.image_urls):
            messagebox.showwarning("Nenhuma imagem selecionada", "Por favor, selecione alguma imagem.")
            return

        selected_image_url = self.image_urls[selected_idx]
        print(f"Imagem selecionada: {selected_image_url}")

        try:
            output_filename = f"downloaded_image_{selected_idx + 1}.jpeg"

            download_and_resize_image(
                selected_image_url,
                output_size=(1200, 630),
                output_format="jpeg",
                output_filename=output_filename
            )
            messagebox.showinfo("Sucesso", f"Imagem baixada e redimensionada com sucesso!\nSalva como {output_filename} na pasta Downloads.")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao baixar e redimensionar a imagem: {e}")

def main():
    global root
    root = tk.Tk()
    root.title("Newspaper Image Extractor")
    root.geometry("500x200")
    root.resizable(False, False)

    def handle_submit(url):

        print(f"URL enviada: {url}")

        try:
            html_content = fetch_webpage(url)
            image_urls = parse_image_urls(html_content, url)

            if not image_urls:
                messagebox.showinfo("Não foram encontradas imagens", "Nenhuma imagem relevante foi encontrada.")
                return

            top_image_urls = image_urls[:5]

            selection_window = tk.Toplevel(root)
            selection_window.title("Seleção de Imagem")
            selection_window.geometry("600x600")
            ImageSelectionGUI(selection_window, top_image_urls)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    app = URLInputGUI(root, handle_submit)

    root.mainloop()

if __name__ == "__main__":
    main()
