from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from requests.exceptions import ConnectionError, InvalidSchema
from django.conf import settings

import requests
import re


class CrockPotRecipe():
    def __init__(self, recipe_id):
        self.recipe_id = recipe_id
        self.recipe_url = ''.join(['https://www.crockpot.pl/przepis?p=', str(self.recipe_id)])

        r = requests.get(self.recipe_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.recipe_div = soup.find("div", class_="przepis")

    def __get_recipe_details(self, class_name):
        return self.recipe_div.\
                find("div", class_=f"przepis-ikonki {class_name}").\
                find("span", class_="przepis-wartosc").\
                string

    def __get_recipe_text(self, class_name):
        recipe_text = self.recipe_div.\
                        find("div", class_=f"{class_name}").span.contents
        return ' '.join(str(t) for t in recipe_text)

    def get_recipe_data(self):
        if self.recipe_div:
            return {
                "url": self.recipe_url,
                "recipe_id": self.recipe_id,
                "name": self.recipe_div.h1.string,
                "serving_size": self.__get_recipe_details("przepis-ilosc-porcji"),
                "preparing_time": self.__get_recipe_details("przepis-czas"),
                "time_on_high": self.__get_recipe_details("przepis-czas-na-high"),
                "time_on_low": self.__get_recipe_details("przepis-czas-na-low"),
                "recipe_ingredients": self.__get_recipe_text("przepis-skladniki"),
                "recipe_how_to": self.__get_recipe_text("przepis-wykonanie")
            }
        else:
            return False

    def get_recipe_images(self):
        if self.recipe_div:
            images_div = self.recipe_div.find_all("div", { "class": "przepis-miniaturka"})
            images_list = []
            for i in range(1,len(images_div)+1):
                img = requests.get(f'https://www.crockpot.pl/themes/crockpot/img/przepisy/{self.recipe_id}/photo_{i}.jpg')
                img_content = Image.open(BytesIO(img.content))
                img_resized = img_content.resize(
                                (int(img_content.width * 1.5),
                                int(img_content.height * 1.5)),
                                resample=5)
                img_name = f'crockpot_{self.recipe_id}_photo_{i}.jpg'
                img_resized.save(f"{settings.MEDIA_ROOT}\img\{img_name}", img_content.format)
                images_list.append(img_name)
            return {
                "recipe_id": self.recipe_id,
                "images": images_list
            }
        else:
            return "No recipe images found"


def get_last_crockpot_recipe_id():
    try:
        r = requests.get('https://www.crockpot.pl/przepisy')
        soup = BeautifulSoup(r.text, 'html.parser')
        recipes_div = soup.find_all("div", class_="aopisek")
        latest_recipe_link = recipes_div[0].a['href']
        latest_recipe_id = re.search("(\d)+", latest_recipe_link).group(0)
        return int(latest_recipe_id)
    except (ConnectionError, IndexError, InvalidSchema):
        return False