import requests

def fetch_webpage_content(url):
    target_url = url
    
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        )
    }
    
    try:
        response = requests.get(target_url, headers=headers)

        if response.status_code == 200:
            return response.text  # Return the HTML content of the page
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
