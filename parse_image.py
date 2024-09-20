import requests
from bs4 import BeautifulSoup
import re

def extract_all_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = set()
    
    for img_tag in soup.find_all('img'):
        for attr in ['src', 'data-src', 'data-lazy', 'srcset']:
            url = img_tag.get(attr)
            if url:
                if attr == 'srcset':
                    url = url.split(',')[-1].split()[0]
                image_urls.add(url)
                
    for picture_tag in soup.find_all('picture'):
        for source in picture_tag.find_all('source'):
            url = source.get('srcset')
            if url:
                url = url.split(',')[-1].split()[0]
                image_urls.add(url)
                
    for tag in soup.find_all(['meta', 'script']):
        content = tag.get('content') or tag.get('src') or ''
        matches = re.findall(r'(https?://[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif))', content)
        image_urls.update(matches)
        
    image_urls = {url.split()[0] for url in image_urls if url.startswith('http')}
    
    return list(image_urls)

def get_image_urls_from_webpage(url):
    response = requests.get(url)
    html_content = response.text
    return extract_all_image_urls(html_content)
