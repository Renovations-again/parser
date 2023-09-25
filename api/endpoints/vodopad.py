import re

import lxml  # noqa
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import APIRouter

from api.validators import validate_domain

router = APIRouter()

ua = UserAgent()


@router.post('/')
async def parse_vodopad(url):
    validate_domain(url)
    domain = 'https://vodopad.ru'
    headers = {
        'Accept': '*/*',
        'User-Agent': ua.random
    }

    def fetch_soup(url):
        try:
            request = requests.get(url, headers=headers)
            request.raise_for_status()  # Проверка на успешный статус ответа
            soup = BeautifulSoup(request.text, 'lxml')
            return soup
        except requests.exceptions.RequestException as err:
            print(f'Ошибка соединения: {err}')
            return None

    def get_title(soup):
        '''Get the name of the item (Название товара)'''
        try:
            title = soup.find('div', class_='prdct-blck-header').text.strip()
            return title
        except AttributeError:
            print('<--Ошибка! Название товара не найдено-->')

    def get_vendor_code(soup):
        '''Get vendor code of an item (Артикул товара)'''
        try:
            raw_vendor_code = soup.find('span', class_='prdct-artcl')
            vendor_code = re.findall('[0-9]+', raw_vendor_code.text)[0]
            return vendor_code
        except AttributeError:
            print('<--Ошибка! Артикул товара не найден-->')

    def get_price(soup):
        '''Get the price of an item (Цена товара)'''
        try:
            raw_price = soup.find('span', class_='prdct-prc mt-1')
            price = float(
                raw_price.text.replace('₽', '').replace(' ', '').strip())
            return price
        except AttributeError:
            print('<--Ошибка! У данного товара нет цены-->')

    def get_images(soup):
        '''Returns a list of all the images of an item (Ссылки на картинки)'''
        try:
            raw_images = soup.find('div', class_='col-12 col-prdct-gallery')
            images = raw_images.find_all('div', class_='swiper-slide')
            photos_count = int(len(images) / 2)
            links = []
            for image in images[:photos_count]:
                links.append(domain + image.img['data-src'])
                # <class 'bs4.element.Tag'> is a dictionary
            return links
        except AttributeError:
            print('<--Ошибка! Фото товара не найдено-->')

    soup = fetch_soup(url)

    return {
        'title': get_title(soup),
        'code': get_vendor_code(soup),
        'price_gold': get_price(soup),
        'price_retail': get_price(soup),
        'unit': 'шт',
        'images': get_images(soup),
    }
