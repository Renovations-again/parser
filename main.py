from urllib.parse import urlparse

import requests
import uvicorn
from constants import CITY_PETROVICH
from fastapi import FastAPI

app = FastAPI()


def parse_petrovich(url):
    parsed_url = urlparse(url)
    path = urlparse(url).path
    category = path.split('/')
    city_domen = parsed_url.netloc.split('.')
    city_code = 'rf'
    if city_domen[0] in CITY_PETROVICH:
        city_code = CITY_PETROVICH[city_domen[0]]

    cookies = {
        'geoQtyTryRedirect': '1',
        'u__geoUserChoose': '1',
        'u__geoCityGuid': 'b835705e-037e-11e4-9b63-00259038e9f2',
        'SIK': 'mAAAAMT1YhwEVBoUZvAMAA',
        'SIV': '1',
        'C_V0Bd3ZwDwQ-zLfop0AueTblltG0': 'AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAIDZ0QPqQeG7jthN9kOI6KLoIBS8aWI',
        'UIN': 'mAAAAEAbthKXpsJhZ546YimsWEfcVM59BVQaFIZ4DAA',
        'ssaid': '16a98b50-4ef8-11ee-b28c-6d7ae9394ec7',
        'dd__lastEventTimestamp': '1695229981519',
        'dd__persistedKeys': '^[^%^22custom.lastViewedProductImages^%^22^%^2C^%^22custom.lt13^%^22^%^2C^%^22custom.ts14^%^22^%^2C^%^22custom.ts12^%^22^%^2C^%^22custom.lt11^%^22^%^2C^%^22user.isReturning^%^22^%^2C^%^22custom.lt15^%^22^%^2C^%^22custom.ts16^%^22^%^2C^%^22custom.productsViewed^%^22^]',
        'dd_custom.lastViewedProductImages': '^[^%^22^%^22^%^2C^%^226964819^%^22^%^2C^%^22^%^22^]',
        '_ga_XW7S332S1N': 'GS1.1.1695227472.17.1.1695231722.0.0.0',
        '_ga': 'GA1.2.1849574150.1694253795',
        'FPID': 'FPID2.2.Zd^%^2BC3kSCNn69o^%^2BQem43EX1^%^2FgGPuy8HIyvWxyV30utH4^%^3D.1694253795',
        'count_buy': '0',
        'js_count_buy': '0',
        'js_SIK': 'mAAAAMT1YhwEVBoUZvAMAA',
        'js_FPID': 'FPID2.2.Zd^%^2BC3kSCNn69o^%^2BQem43EX1^%^2FgGPuy8HIyvWxyV30utH4^%^3D.1694253795',
        '_gpVisits': '{isFirstVisitDomain:true,idContainer:100025B4}',
        'adrcid': 'AKe4CmUyr3Ka08LRJRwFS0A',
        'ser_adrcid': 'AKe4CmUyr3Ka08LRJRwFS0A',
        'tmr_lvid': '9e5c50c934ac24d976b9557857c21c94',
        'tmr_lvidTS': '1694253799011',
        'dd_custom.lt13': '2023-09-20T17:00:28.723Z',
        'dd_custom.ts14': '{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:{^%^221694217600^%^22:15^%^2C^%^221694390400^%^22:6^%^2C^%^221694563200^%^22:6^%^2C^%^221695168000^%^22:1}}',
        'digi_uc': 'W1sidiIsIjE1OTY1NiIsMTY5NTIyOTk4MTI5M10sWyJ2IiwiNjIwMTMzIiwxNjk1MjI3NDk2Nzg4XSxbInYiLCI2ODU0MDAiLDE2OTUxMTA2NTU2NjddLFsidiIsIjk4NzI2MCIsMTY5NDQ1MzEwMTQ0Ml0sWyJ2IiwiOTc3MDg0IiwxNjk0NDM5OTExNjIzXSxbInYiLCI2NzE4ODUiLDE2OTQ0Mzk5MDgwMjZdLFsidiIsIjEwNTcwMyIsMTY5NDQzOTg3NjQ4Ml0sWyJ2IiwiMTU5MDgyIiwxNjk0NDM5ODY4NDA2XSxbInYiLCIxNDkxNDMiLDE2OTQ0Mzk4NjA3NzNdLFsidiIsIjY4NTM5OSIsMTY5NDI1NjkzNDUzN10sWyJjdiIsIjEwNTY3OSIsMTY5NTIyOTIyNjk3MV0sWyJjdiIsIjY2NzYzMCIsMTY5NDYyMTE4MDYwMF0sWyJjdiIsIjYzNDc0MSIsMTY5NDYyMTEzNTQ0NV0sWyJjdiIsIjE1ODAzMyIsMTY5NDYyMTAwMDY0OF0sWyJjdiIsIjY3NTYxMSIsMTY5NDYyMDcxODcyNl0sWyJjdiIsIjY3ODkyMiIsMTY5NDQzOTg5MDU5M10sWyJjdiIsIjE0NTcwOCIsMTY5NDQzOTg4NzQ3OF0sWyJjdiIsIjEwNTcwMyIsMTY5NDQzOTg3Mjg4MF0sWyJjdiIsIjE0NDQ0NCIsMTY5NDQzOTg3MDkzMF0sWyJjdiIsIjk4NzI2MCIsMTY5NDQzODg2ODU1NF0sWyJzdiIsIjYyMDEzMyIsMTY5NDQzOTk3OTkyM10sWyJzdiIsIjE0OTE0MyIsMTY5NDQzOTg2NTEyNl0sWyJzdiIsIjY4NTQwMCIsMTY5NDQzOTM0MzI2OV0sWyJzdiIsIjY4MTEyNCIsMTY5NDQzOTMwNTEzNV1d',
        'dd_custom.ts12': '{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:{^%^221694217600^%^22:9^%^2C^%^221694390400^%^22:22^%^2C^%^221694736000^%^22:2^%^2C^%^221694995200^%^22:5^%^2C^%^221695081600^%^22:2^%^2C^%^221695168000^%^22:7}}',
        'dd_custom.lt11': '2023-09-20T17:13:01.513Z',
        'dd_user.isReturning': 'true',
        'blueID': 'bcfc7339-1efa-4fed-9445-5eb62ee4914f',
        'dd_custom.lt15': '2023-09-11T13:46:20.954Z',
        'dd_custom.ts16': '{^%^22ttl^%^22:2592000^%^2C^%^22granularity^%^22:86400^%^2C^%^22data^%^22:{^%^221694390400^%^22:5}}',
        'aplaut_distinct_id': 'mMSPKPSF9OGZ',
        'popmechanic_sbjs_migrations': 'popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1',
        '_ga_W2P47Q5K50': 'GS1.1.1694444360.1.1.1694444469.0.0.0',
        '_ga_80YQWC36XE': 'GS1.2.1694444362.1.1.1694444457.60.0.0',
        'SNK': '152',
        'u__typeDevice': 'desktop',
        'dd_custom.productsViewed': '7',
        'FPLC': 'WnE7mSAbWcKzyyJJLBZUNMthhTrZg8gM8Ohyp2XCunFmEwZHCpsbRA2VMs0KV0prNxpRcD4OKs1ULctOc9HZMwKZGEHw1z4D^%^2Fx7vuG^%^2B2^%^2BoZzx1DCuO85MKPxYqxfww^%^3D^%^3D',
        '_gid': 'GA1.2.225145910.1695227475',
        '_gp100025B4': '{hits:4,vc:1,ac:1,a6:1}',
        '__tld__': 'null',
        'mindboxDeviceUUID': '242c99d6-f1ff-4c36-b485-0ef0de294d5d',
        'directCrm-session': '^%^7B^%^22deviceGuid^%^22^%^3A^%^22242c99d6-f1ff-4c36-b485-0ef0de294d5d^%^22^%^7D',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
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
    response = requests.get(api_url, cookies=cookies, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        product = data['data']['product']
        product_info = {
            'title': product['title'],
            'code': product['code'],
            'price_gold': product['price']['gold'],
            'price_retail': product['price']['retail'],
            'unit': product['unit_title'],
            'images': product['images'],
        }
        return product_info
    else:
        return {'error': 'Не удалось получить информацию о товаре'}


def parse_vodopad():
    pass


@app.get('/')
async def get_product_by_store(url: str):
    # Определяем магазин на основе структуры URL
    parsed_url = urlparse(url)
    if 'petrovich' in parsed_url.netloc:
        return parse_petrovich(url)
    elif 'vodopad' in parsed_url.netloc:
        return parse_vodopad(url)
    else:
        return {'error': 'Магазин с таким идентификатором не найден'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
