import requests
from requests.exceptions import RequestException

def fetch_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try: 
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        raise ValueError(f"Falha ao escanear a página: {e}")
    