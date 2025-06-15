import requests
from bs4 import BeautifulSoup
import os
from config.constants import CHARACTER_ICON_URL
from utils.icons.crop_icon import crop_image_to_square
from time import sleep

def get_icons(game, crop=False):
    
    os.makedirs(f"assets/character_icons/{game}/raw", exist_ok=True)
    os.makedirs(f"assets/character_icons/{game}/icons", exist_ok=True)
    
    assets_icons_path = f"assets/character_icons/{game}/icons"
    assets_raw_path = f"assets/character_icons/{game}/icons"
    
    existing_raw = [ assets_raw_path + "/" + img for img in os.listdir(assets_raw_path)]
    existing_icons = [ assets_icons_path + "/" + img for img in os.listdir(assets_icons_path)]
    
    #input()
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
                raw_filename = assets_raw_path + f"/{character_name.replace(':', '').replace(' ', '_')}{file_extension}"
                icon_filename = assets_icons_path + f"/{character_name.replace(':', '').replace(' ', '_')}{file_extension}"

                if raw_filename in existing_raw:
                    if crop:
                        if icon_filename in existing_icons:
                            print(f"Raw/Icon images for {character_name} already exist. Skipping...")
                            continue
                    else:
                        pass
                    
                    print(f"Raw image for {character_name} already exists, cropping is disabled. Skipping...")
                    continue
                
                with open(raw_filename, 'wb') as img_file:
                    img_file.write(img_data)
                if crop:
                    crop_image_to_square(raw_filename, icon_filename)
               
                print(f"Downloaded: {character_name} -> {raw_filename}" + " || cropped" if crop else "")
            else:
                print(f"No image found for {character_name}")
        else:
            print("No avatar div found in this card.")

    print("Exited with no errors.")
            