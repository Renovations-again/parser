# import json
# import requests
# from bs4 import BeautifulSoup

# URL = 'https://moscow.petrovich.ru/catalog/9575968/987260/'  # стул
# URL2 = 'https://moscow.petrovich.ru/catalog/12454/685400/'  # дверь
# URL3 = 'https://moscow.petrovich.ru/catalog/245046398/620133/'  # плитка

# CURRENT_URL = URL3


# def fetch_soup(url):
#     try:
#         request = requests.get(url, headers={"Content-Type": "text"})
#         request.raise_for_status()  # Проверка на успешный статус ответа
#         soup = BeautifulSoup(request.text, 'lxml')
#         return soup
#     except requests.exceptions.RequestException as err:
#         print(f'Ошибка соединения: {err}')
#         return None


# def get_title(soup):
#     '''Get the name of an item (Название товара)'''
#     if soup:
#         return soup.find('h1').text
#     return None


# def get_vendor_code(soup):
#     '''Get vendor code of an item (Артикул товара)'''
#     if soup:
#         return soup.find(
#             'span', class_='pt-c-secondary-lowest'
#             ).next_sibling.text
#     return None


# def get_images(soup):
#     '''Returns a list of all the images of an item (Ссылки на картинки)'''
#     if soup:
#         images = soup.find_all('img', class_='swiper-lazy')
#         link_images = [image.get('src') for image in images]
#         return list(set(link_images))
#     return []


# def get_price(soup):
#     '''Get the price of an item (Цена товара)'''
#     try:
#         units_tabs = soup.find('span', class_='units-tabs')
#         units = []
#         if len(units_tabs) <= 2:
#             unit_1 = 'за ' + units_tabs.find_all('p')[1].text
#             units.append(unit_1)
#         else:
#             for i in units_tabs.find_all('span'):
#                 units.append(i.text)
#         units = list(set(units))
#     except AttributeError:
#         print('<--Ошибка! У данного товара нет цены-->')

#     # достаем id товара
#     item_id = CURRENT_URL.split('/')[-2] if CURRENT_URL.endswith('/') else\
#         CURRENT_URL.split('/')[-1]

#     cookies = {
#         'SNK': '152',
#         'u__typeDevice': 'desktop',
#         'SIK': 'mAAAAKBmrmVykyoU50MAAA',
#         'SIV': '1',
#         'C_cFP1oZBwGxGkblLIrBex2M_puWc': 'AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAEAuVgTqQZg3cdasg-Y9TzU-9-Z63GQ', # noqa
#         '_ym_uid': '1695318606607610233',
#         '_ym_d': '1695318606',
#         '_gid': 'GA1.2.453484247.1695318607',
#         '_ym_isad': '2',
#         '_ym_visorc': 'b',
#         'FPID': 'FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607', # noqa
#         'count_buy': '0',
#         'js_SIK': 'mAAAAKBmrmVykyoU50MAAA',
#         'ser_ym_uid': '1695318606607610233',
#         'FPLC': 'IaYtKeyCQvEJAgPD7HqPJ0jRsxfXKtlH3jVpiCFs5cbyYOw8jIPZrB7oHJwDdE%2FyQFlPq4jvIv2EOGoMXugQMoqPRrQMjgPngozK9lUghpqN%2BFXoeF1f2tGuR7oHHw%3D%3D', # noqa
#         'blueID': '45d198db-b4ff-41d0-830b-dce68f330055',
#         'js_count_buy': '0',
#         'js_FPID': 'FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607', # noqa
#         'UIN': 'mAAAANSrojkSo5xLkm-3JcXTY1P6mSR7b5QqFGaqCAA',
#         '_ga': 'GA1.2.508802657.1695318607',
#         '_ga_XW7S332S1N': 'GS1.1.1695318606.1.1.1695318926.0.0.0',
#     }

#     headers = {
#         'authority': 'api.petrovich.ru',
#         'accept': 'application/json, text/plain, */*',
#         # 'cookie': 'SNK=152; u__typeDevice=desktop; SIK=mAAAAKBmrmVykyoU50MAAA; SIV=1; C_cFP1oZBwGxGkblLIrBex2M_puWc=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAEAuVgTqQZg3cdasg-Y9TzU-9-Z63GQ; _ym_uid=1695318606607610233; _ym_d=1695318606; _gid=GA1.2.453484247.1695318607; _ym_isad=2; _ym_visorc=b; FPID=FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607; count_buy=0; js_SIK=mAAAAKBmrmVykyoU50MAAA; ser_ym_uid=1695318606607610233; FPLC=IaYtKeyCQvEJAgPD7HqPJ0jRsxfXKtlH3jVpiCFs5cbyYOw8jIPZrB7oHJwDdE%2FyQFlPq4jvIv2EOGoMXugQMoqPRrQMjgPngozK9lUghpqN%2BFXoeF1f2tGuR7oHHw%3D%3D; blueID=45d198db-b4ff-41d0-830b-dce68f330055; js_count_buy=0; js_FPID=FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607; UIN=mAAAANSrojkSo5xLkm-3JcXTY1P6mSR7b5QqFGaqCAA; _ga=GA1.2.508802657.1695318607; _ga_XW7S332S1N=GS1.1.1695318606.1.1.1695318926.0.0.0', # noqa
#         'origin': 'https://petrovich.ru',
#         'referer': 'https://petrovich.ru/catalog/1524/134991/',
#         'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Opera";v="102"', # noqa
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-site',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0', # noqa
#     }

#     # среди параметров экспериментальным методом было обнаружено, что
#     # необходим только city_code
#     params = {
#         'section_code': '1524',
#         'city_code': 'msk',
#         'client_id': 'pet_site',
#     }
#     petrovich_api = requests.get(
#         f'https://api.petrovich.ru/catalog/v3/products/{item_id}',
#         cookies=cookies,
#         headers=headers,
#         params=params
#     ).text

#     data = json.loads(petrovich_api)
#     features = data['data']['product']
#     if len(units) == 1:
#         unit_1_price_card = \
#             f'Цена за {units[0]} по карте: {features["price"]["gold"]}'
#         unit_1_price_retail = \
#             f'Цена за {units[0]}: {features["price"]["retail"]}'
#         return unit_1_price_card + '\n' + unit_1_price_retail
#     else:
#         unit_1_price_card = \
#             f'Цена за {units[0]} по карте: {features["price"]["gold"]}'
#         unit_1_price_retail = \
#             f'Цена за {units[0]}: {features["price"]["retail"]}'
#         unit_2_price_card = \
#             f'Цена за {units[1]} по карте: {features["price_alt"]["gold"]}'
#         unit_2_price_retail = \
#             f'Цена за {units[1]}: {features["price_alt"]["retail"]}'
#         return (unit_1_price_card +
#                 '\n' + unit_1_price_retail +
#                 '\n' + unit_2_price_card +
#                 '\n' + unit_2_price_retail)


# def main():
#     print('URL:', CURRENT_URL)
#     soup = fetch_soup(CURRENT_URL)
#     print('------------')
#     print('Название:', get_title(soup))
#     print('------------')
#     print('Артикул:', get_vendor_code(soup))
#     print('------------')
#     print(get_price(soup))
#     print('------------')
#     print('Список ссылок на картинки:', get_images(soup))
#     print()


# if __name__ == "__main__":
#     main()
from urllib.parse import urlparse

import requests
CITY_PETROVICH = {
    'moscow': 'msk',
    'arkhangelsk': 'arkh',
    'astrakhan': 'astrh',
    'novgorod': 'nvr',
    'vladimir': 'vld',
    'volzhskiy': 'volzh',
    'vyborg': 'vbg',
    'gatchina': 'gtn',
    'gubkin': 'gbkn',
    'zheleznogorsk': 'zhelez',
    'i-ola': 'iola',
    'kazan': 'kzn',
    'kaluga': 'klg',
    'kingisepp': 'kgs',
    'kirov': 'krv',
    'kursk': 'krsk',
    'lipetsk': 'lipck',
    'luga': 'lug',
    'magnitogorsk': 'mgnt',
    'naberezhnye-chelny': 'nabchel',
    'nizhnevartovsk': 'nizhvar',
    'nizhniy-novgorod': 'nizhnov',
    'nizhniy-tagil': 'tagil',
    'orel': 'orl',
    'pervouralsk': 'pervour',
    'petrozavodsk': 'pzv',
    'pskov': 'pskv',
    'ryazan': 'rzn',
    'stary-oskol': 'oskol',
    'syktyvkar': 'sktv',
    'tver': 'tvr',
    'tobolsk': 'tbl',
    'tula': 'tul',
    'cheboksary': 'cheb',
    'engels': 'engl',
    'petrovich': 'spb',
}



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


print(parse_petrovich('https://petrovich.ru/catalog/1524/134991/'))