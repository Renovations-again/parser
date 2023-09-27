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
            title = soup.find('h1').text
            return title
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Название товара не найдено'
            )

    def get_vendor_code(soup):
        '''Get vendor code of an item (Артикул товара)'''
        try:
            vendor_code = soup.find('span', class_='_2XlQF').text
            return vendor_code
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Артикул товара не найден'
            )

    def get_price(soup):
        '''Get the price of an item (Цена товара)'''
        try:
            raw_price = soup.find('span', class_='_3IeOW').text
            price = float(
                ''.join([
                    i for i in raw_price if i.isdigit() or i == ','
                ]).replace(',', '.')
            )
            unit = soup.find('span', class_='_3SDdj').text
            return price, unit
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! У данного товара нет цены'
            )

    def get_images(soup):
        '''Returns a list of all the images of an item (Ссылки на картинки)'''
        try:
            raw_images = soup.find(
                'div', class_='_3CCD5 _2EcjD'
            ).findChildren()
            link_images = [
                            image.
                            get('srcset') for image in raw_images if image.
                            get('srcset')
                        ]
            images = []
            for image in link_images:
                big_image = image.split(',')[1].split()[0].strip()
                images.append(big_image)
            return images[::2]
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
