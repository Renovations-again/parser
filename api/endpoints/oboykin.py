import requests

from http import HTTPStatus
import lxml  # noqa
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import APIRouter, HTTPException

from api.validators import validate_domain

router = APIRouter()

ua = UserAgent()


@router.post('/')
async def parse_oboykin(url):
    validate_domain(url)
    domain = 'https://oboykin.ru'
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
        '''Get the name of an item (Название товара)'''
        try:
            title = soup.find('h1')
            # У некоторых товаров есть дополнительное имя под основным
            if title.fetchNextSiblings('p'):
                verbose_name = title.fetchNextSiblings('p')[0].text
                return f'{title.text} ({verbose_name})'
            return title.text
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Название товара не найдено'
            )

    def get_vendor_code(soup):
        '''Get vendor code of an item (Артикул товара)'''
        try:
            description = soup.find(
                'div', class_='page-tovarpage__description__info'
            ).find('ul').find_all('li')
            for item in description:
                if item.find(string='Артикул'):
                    vendor_code = item.find(string='Артикул').find_next().text
            return vendor_code
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Артикул товара не найден'
            )

    def get_price(soup):
        '''Get the price of an item (Цена товара)'''
        try:
            identifier = soup.find('div', class_='page-tovarpage__price')
            price = identifier.find('div', class_='sum').text.replace(' ', '')
            units = identifier.find('div', class_='units').text
            return float(price), units
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! У данного товара нет цены'
            )

    def get_images(soup):
        '''Returns a list of all the images of an item (Ссылки на картинки)'''
        try:
            raw_images = soup.find(
                'div', {'class': 'owl-carousel'}
            ).find_all('a')
            images = []
            for item in raw_images:
                images.append(domain + item['href'])
            return images
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Фото товара не найдено'
            )

    soup = fetch_soup(url)

    return {
        'title': get_title(soup),
        'code': get_vendor_code(soup),
        'price_gold': get_price(soup)[0],
        'price_retail': get_price(soup)[0],
        'unit': get_price(soup)[1],
        'images': get_images(soup),
    }
