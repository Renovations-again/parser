import re
from http import HTTPStatus

import lxml  # noqa
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import APIRouter, HTTPException

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
        response = requests.get(url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=404,
                detail='Не удалось получить информацию о товаре',
            )
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup

    def get_title(soup):
        '''Get the name of the item (Название товара)'''
        try:
            title = soup.find('div', class_='prdct-blck-header').text.strip()
            return title
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Название товара не найдено'
            )

    def get_vendor_code(soup):
        '''Get vendor code of an item (Артикул товара)'''
        try:
            raw_vendor_code = soup.find('span', class_='prdct-artcl')
            vendor_code = re.findall('[0-9]+', raw_vendor_code.text)[0]
            return vendor_code
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Артикул товара не найден'
            )

    def get_price(soup):
        '''Get the price of an item (Цена товара)'''
        try:
            raw_price = soup.find('span', class_='prdct-prc mt-1')
            price = float(
                raw_price.text.replace('₽', '').replace(' ', '').strip())
            return price
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! У данного товара нет цены'
            )

    def get_images(soup):
        '''Returns a list of all the images of an item (Ссылки на картинки)'''
        try:
            raw_images = soup.find('div', class_='col-12 col-prdct-gallery')
            images = raw_images.find_all('div', class_='swiper-slide')
            photos_count = int(len(images) / 2)
            links = []
            for image in images[:photos_count]:
                links.append(domain + image.img['data-src'])
            return links
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Фото товара не найдено'
            )

    soup = fetch_soup(url)

    return {
        'title': get_title(soup),
        'code': get_vendor_code(soup),
        'price_gold': get_price(soup),
        'price_retail': get_price(soup),
        'unit': 'шт',
        'images': get_images(soup),
    }
