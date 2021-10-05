from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from requests.exceptions import ConnectionError, InvalidSchema
from django.conf import settings

import requests
import re


class CrockPotRecipe():
    def __init__(self, receipe_id):
        self.receipe_id = receipe_id
        self.receipe_url = ''.join(['https://www.crockpot.pl/przepis?p=', str(self.receipe_id)])

        r = requests.get(self.receipe_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.receipe_div = soup.find("div", class_="przepis")

    def __get_receipe_details(self, class_name):
        return self.receipe_div.\
                find("div", class_=f"przepis-ikonki {class_name}").\
                find("span", class_="przepis-wartosc").\
                string

    def __get_receipe_text(self, class_name):
        receipe_text = self.receipe_div.\
                        find("div", class_=f"{class_name}").span.contents
        return ' '.join(str(t) for t in receipe_text)

    def get_receipe_data(self):
        if self.receipe_div:
            return {
                "url": self.receipe_url,
                "receipe_id": self.receipe_id,
                "name": self.receipe_div.h1.string,
                "serving_size": self.__get_receipe_details("przepis-ilosc-porcji"),
                "preparing_time": self.__get_receipe_details("przepis-czas"),
                "time_on_high": self.__get_receipe_details("przepis-czas-na-high"),
                "time_on_low": self.__get_receipe_details("przepis-czas-na-low"),
                "receipe_ingredients": self.__get_receipe_text("przepis-skladniki"),
                "receipe_how_to": self.__get_receipe_text("przepis-wykonanie")
            }
        else:
            return False

    def get_receipe_images(self):
        if self.receipe_div:
            images_div = self.receipe_div.find_all("div", { "class": "przepis-miniaturka"})
            images_list = []
            for i in range(1,len(images_div)+1):
                img = requests.get(f'https://www.crockpot.pl/themes/crockpot/img/przepisy/{self.receipe_id}/photo_{i}.jpg')
                img_content = Image.open(BytesIO(img.content))
                img_resized = img_content.resize(
                                (int(img_content.width * 1.5),
                                int(img_content.height * 1.5)),
                                resample=5)
                img_name = f'crockpot_{self.receipe_id}_photo_{i}.jpg'
                img_resized.save(f"{settings.MEDIA_ROOT}\img\{img_name}", img_content.format)
                images_list.append(img_name)
            return {
                "receipe_id": self.receipe_id,
                "images": images_list
            }
        else:
            return "No receipe images found"


def get_last_crockpot_receipe_id():
    try:
        r = requests.get('https://www.crockpot.pl/przepisy')
        soup = BeautifulSoup(r.text, 'html.parser')
        receipes_div = soup.find_all("div", class_="aopisek")
        latest_receipe_link = receipes_div[0].a['href']
        latest_receipe_id = re.search("(\d)+", latest_receipe_link).group(0)
        return int(latest_receipe_id)
    except (ConnectionError, IndexError, InvalidSchema):
        return False