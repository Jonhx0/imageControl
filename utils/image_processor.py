import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import os

def get_downloads_folder():

    home = Path.home()
    downloads = home / "Downloads"

    if downloads.exists() and downloads.is_dir():
        return downloads
    else:
        return home

def download_and_resize_image(image_url, output_size=(1200, 630), output_format="jpeg", output_filename="downloaded_image.jpg"):

    downloads_folder = get_downloads_folder()
    output_path = downloads_folder / output_filename

    if not downloads_folder.exists():
        os.makedirs(downloads_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to download the image: {e}")

    img_data = BytesIO(response.content)

    try:
        img = Image.open(img_data)

        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        desired_ratio = output_size[0] / output_size[1]
        img_ratio = img.width / img.height

        if img_ratio > desired_ratio:
            new_height = output_size[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = output_size[0]
            new_height = int(new_width / img_ratio)

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        left = (new_width - output_size[0]) / 2
        top = (new_height - output_size[1]) / 2
        right = (new_width + output_size[0]) / 2
        bottom = (new_height + output_size[1]) / 2

        img_cropped = img_resized.crop((left, top, right, bottom))

        img_cropped.save(output_path, output_format.upper())
        print(f"Image saved as {output_path} in {output_format.upper()} format.")
    except Exception as e:
        raise ValueError(f"Failed to process the image: {e}")
