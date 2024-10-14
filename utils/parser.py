from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import re

def parse_image_urls(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = set()
    
    # Extração de Imagens.
    article = soup.find('article')
    if article:
        main_image = article.find('img', class_='main-image-class')
        if main_image:
            add_image_url(main_image['src'], base_url, image_urls)
            
    og_image = soup.find("meta", property="og:image")
    if og_image:
        image_urls.add(og_image["content"])
                
            
    # Verificação de imagens nas tags.
    for picture_tag in soup.find_all('picture'):
        for source in picture_tag.find_all('source'):
            url = source.get('srcset')
            if url:
                url = url.split(',')[-1].split()[0]
                image_urls.add(url)
    
    # Extração de todas as tags de imagem da página.
    for img_tag in soup.find_all('img'):
        for attr in ['src', 'data-src', 'data-lazy', 'srcset']:
            url = img_tag.get(attr)
            if url:
                if attr == 'srcset':
                    url = url.split(',')[-1].split()[0]
                add_image_url(urljoin(base_url, url), base_url, image_urls)
                
    # Regex para as imagens na meta e nas tags de script.
    for tag in soup.find_all(['meta', 'script']):
        content = tag.get('content') or tag.get('src') or ''
        matches = re.findall(r'(https?://[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif))', content)
        image_urls.update(matches)
        
    # Filtragem e retorno das URLs de imagens válidas.
    return list(url for url in image_urls if is_valid_image_url(url))

def add_image_url(img_url, base_url, image_urls):
    if img_url and img_url.startswith('http'):
        image_urls.add(img_url)
        
def is_valid_image_url(img_url):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff']
    parsed_url = urlparse(img_url)
    return any(parsed_url.path.lower().endswith(ext) for ext in valid_extensions)
