from http import HTTPStatus

import requests
from fake_useragent import UserAgent
from fastapi import APIRouter, HTTPException

from api.validators import validate_domain
from resources.constants import COOKIES
from services.parser_urls import parser_url_petrovich

router = APIRouter()


@router.post('/')
async def parse_petrovich(url):
    validate_domain(url)
    parsed_url, category, city_code = parser_url_petrovich(url)

    headers = {
        'User-Agent': UserAgent().random,
        'Referer': url,
        'Origin': parsed_url.scheme + '://' + parsed_url.netloc,
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    params = {
        'section_code': category[2],
        'city_code': city_code,
        'client_id': 'pet_site',
    }

    code = category[3]
    api_url = 'https://api.petrovich.ru/catalog/v3/products/' + str(code)
    response = requests.get(api_url, cookies=COOKIES, headers=headers,
                            params=params)
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=404,
            detail='Не удалось получить информацию о товаре',
        )
    else:
        data = response.json()
        product = data.get('data').get('product')
        # Обработать данные через Pydantic (на будущее)
        if product['checkout_type'] == 'disabled':
            return 'Товар недоступен в этом городе'
        else:
            product_info = {
                'title': product['title'],
                'code': product['code'],
                'price_gold': product['price']['gold'],
                'price_retail': product['price']['retail'],
                'unit': product['unit_title'],
                'images': product['images'],
            }
            return product_info
