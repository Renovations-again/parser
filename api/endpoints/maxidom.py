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
async def parse_maxidom(url):
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
        '''Get the name of the item (Название товара)'''
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
            vendor_code = soup.find(
                'div', class_='flypage__lineinfo-code'
                ).text
            return vendor_code
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! Артикул товара не найден'
            )

    def get_price(soup):
        '''Get the price of an item (Цена товара)'''
        try:
            # get price_1
            price_block = soup.select('div.lvl1__product-body-buy-price-base')
            for p in price_block:
                price_unit = int(p.get('data-repid_price'))
                break

            # get unit_1
            price_block = soup.find(
                'div', class_='lvl1__product-body-buy-price-base'
            )
            unit = price_block.find(
                'span', class_='lvl1__product-body-buy-price-measure'
            ).contents[0]

            return price_unit, unit
        except AttributeError:
            raise HTTPException(
                status_code=404, detail='Ошибка! У данного товара нет цены'
            )

    def get_images(soup):
        '''Returns a list of all the images of an item (Ссылки на картинки)'''
        try:
            img_block = soup.find(
                'div', {'id': 'flypage_slider_large_vertical_base'}
            )
            images = img_block.find(
                'div', class_='swiper-wrapper'
            ).findChildren()
            link_images = [
                image.get('src') for image in images if image.get('src')
            ]
            return link_images
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
