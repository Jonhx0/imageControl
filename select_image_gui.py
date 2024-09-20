import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import requests
from io import BytesIO

def display_images(image_urls, aspect_ratio=(4,3), window_size=(800, 600)):
    window = tk.Tk()
    window.title("Select the Main Image")
    window.geometry(f"{window_size[0]}x{window_size[1]}")
    
    frame = tk.Frame(window)
    frame.pack()
    
    def on_image_click(url):
        print(f"Image selected: {url}")
        window.quit()
    
    for idx, url in enumerate(image_urls[:10]):
        try:
            response = requests.get(url)
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            
            target_width = 150
            target_height = int(target_width * aspect_ratio[1] / aspect_ratio[0])
            
            image = ImageOps.fit(image, (target_width, target_height), Image.LANCZOS)
            
            img = ImageTk.PhotoImage(image)
            
            btn = tk.Button(frame, image=img, command=lambda u=url: on_image_click(u))
            btn.image = img
            btn.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)
        
        except Exception as e:
            print(f"Error loading image from {url}: {e}")
            
    window.mainloop()
