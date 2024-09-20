# teste de git push e pull
from fetch import fetch_webpage_content
from parse_image import extract_all_image_urls
from select_image_gui import display_images

def main():
    url = "https://g1.globo.com/politica/noticia/2024/09/12/stf-decide-que-e-valida-a-execucao-imediata-da-pena-de-condenados-pelo-tribunal-do-juri.ghtml"
    html_content = fetch_webpage_content(url)
    
    if html_content:
        image_url = extract_all_image_urls(html_content)
        if image_url:
            display_images(image_url)
        else:
            print("No images found.")
    else:
        print("Failed to retrieve the webpage content.")
        
if __name__ == "__main__":
    main()
