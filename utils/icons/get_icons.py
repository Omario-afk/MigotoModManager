import requests
from bs4 import BeautifulSoup
import os
from config.constants import CHARACTER_ICON_URL
from utils.crop_icon import crop_image_to_square

def get_icons(game, crop=False):
    url = CHARACTER_ICON_URL[game]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='avatar-card card')

    for card in cards:
        name_tag = card.find('span', class_='emp-name')
        if name_tag:
            character_name = name_tag.text.strip()
            #print(character_name)
        else:
            character_name = "Unknown"
        if card:
            img_tag = [ img for img in card.find_all('img', {'data-main-image': True}) if 'src' in img.attrs][0]

            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
                base_url = 'https://www.prydwen.gg' 
                full_img_url = base_url + img_url if img_url.startswith('/') else img_url

                img_data = requests.get(full_img_url).content
                file_extension = os.path.splitext(full_img_url)[1].split('?')[0]  # handle query strings
                filename = f"assets/character_icons/{game}/raw/{character_name.replace(':', '').replace(' ', '_')}{file_extension}"
                
                if crop:
                    crop_image_to_square(filename, filename.replace("raw", f"assets/character_icons/{game}/icons/{character_name.replace(':', '').replace(' ', '_')}{file_extension}"))
                with open(filename, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {character_name} -> {filename}")
            else:
                print(f"No image found for {character_name}")
        else:
            print("No avatar div found in this card.")
            
get_icons("ZenlessZoneZero", crop=True)