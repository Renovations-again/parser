import json
import requests
from bs4 import BeautifulSoup

URL = 'https://moscow.petrovich.ru/catalog/9575968/987260/'  # стул
URL2 = 'https://moscow.petrovich.ru/catalog/12454/685400/'  # дверь
URL3 = 'https://moscow.petrovich.ru/catalog/245046398/620133/'  # плитка

CURRENT_URL = URL3


def fetch_soup(url):
    try:
        request = requests.get(url, headers={"Content-Type": "text"})
        request.raise_for_status()  # Проверка на успешный статус ответа
        soup = BeautifulSoup(request.text, 'lxml')
        return soup
    except requests.exceptions.RequestException as err:
        print(f'Ошибка соединения: {err}')
        return None


def get_title(soup):
    '''Get the name of an item (Название товара)'''
    if soup:
        return soup.find('h1').text
    return None


def get_vendor_code(soup):
    '''Get vendor code of an item (Артикул товара)'''
    if soup:
        return soup.find(
            'span', class_='pt-c-secondary-lowest'
            ).next_sibling.text
    return None


def get_images(soup):
    '''Returns a list of all the images of an item (Ссылки на картинки)'''
    if soup:
        images = soup.find_all('img', class_='swiper-lazy')
        link_images = [image.get('src') for image in images]
        return list(set(link_images))
    return []


def get_price(soup):
    '''Get the price of an item (Цена товара)'''
    try:
        units_tabs = soup.find('span', class_='units-tabs')
        units = []
        if len(units_tabs) <= 2:
            unit_1 = 'за ' + units_tabs.find_all('p')[1].text
            units.append(unit_1)
        else:
            for i in units_tabs.find_all('span'):
                units.append(i.text)
        units = list(set(units))
    except AttributeError:
        print('<--Ошибка! У данного товара нет цены-->')

    # достаем id товара
    item_id = CURRENT_URL.split('/')[-2] if CURRENT_URL.endswith('/') else\
        CURRENT_URL.split('/')[-1]

    cookies = {
        'SNK': '152',
        'u__typeDevice': 'desktop',
        'SIK': 'mAAAAKBmrmVykyoU50MAAA',
        'SIV': '1',
        'C_cFP1oZBwGxGkblLIrBex2M_puWc': 'AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAEAuVgTqQZg3cdasg-Y9TzU-9-Z63GQ', # noqa
        '_ym_uid': '1695318606607610233',
        '_ym_d': '1695318606',
        '_gid': 'GA1.2.453484247.1695318607',
        '_ym_isad': '2',
        '_ym_visorc': 'b',
        'FPID': 'FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607', # noqa
        'count_buy': '0',
        'js_SIK': 'mAAAAKBmrmVykyoU50MAAA',
        'ser_ym_uid': '1695318606607610233',
        'FPLC': 'IaYtKeyCQvEJAgPD7HqPJ0jRsxfXKtlH3jVpiCFs5cbyYOw8jIPZrB7oHJwDdE%2FyQFlPq4jvIv2EOGoMXugQMoqPRrQMjgPngozK9lUghpqN%2BFXoeF1f2tGuR7oHHw%3D%3D', # noqa
        'blueID': '45d198db-b4ff-41d0-830b-dce68f330055',
        'js_count_buy': '0',
        'js_FPID': 'FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607', # noqa
        'UIN': 'mAAAANSrojkSo5xLkm-3JcXTY1P6mSR7b5QqFGaqCAA',
        '_ga': 'GA1.2.508802657.1695318607',
        '_ga_XW7S332S1N': 'GS1.1.1695318606.1.1.1695318926.0.0.0',
    }

    headers = {
        'authority': 'api.petrovich.ru',
        'accept': 'application/json, text/plain, */*',
        # 'cookie': 'SNK=152; u__typeDevice=desktop; SIK=mAAAAKBmrmVykyoU50MAAA; SIV=1; C_cFP1oZBwGxGkblLIrBex2M_puWc=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAEAuVgTqQZg3cdasg-Y9TzU-9-Z63GQ; _ym_uid=1695318606607610233; _ym_d=1695318606; _gid=GA1.2.453484247.1695318607; _ym_isad=2; _ym_visorc=b; FPID=FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607; count_buy=0; js_SIK=mAAAAKBmrmVykyoU50MAAA; ser_ym_uid=1695318606607610233; FPLC=IaYtKeyCQvEJAgPD7HqPJ0jRsxfXKtlH3jVpiCFs5cbyYOw8jIPZrB7oHJwDdE%2FyQFlPq4jvIv2EOGoMXugQMoqPRrQMjgPngozK9lUghpqN%2BFXoeF1f2tGuR7oHHw%3D%3D; blueID=45d198db-b4ff-41d0-830b-dce68f330055; js_count_buy=0; js_FPID=FPID2.2.ZrhVvDiJvw6VjHuVBOGg8ZRI4lmnEf81rg93dyWOC%2Fo%3D.1695318607; UIN=mAAAANSrojkSo5xLkm-3JcXTY1P6mSR7b5QqFGaqCAA; _ga=GA1.2.508802657.1695318607; _ga_XW7S332S1N=GS1.1.1695318606.1.1.1695318926.0.0.0', # noqa
        'origin': 'https://petrovich.ru',
        'referer': 'https://petrovich.ru/catalog/1524/134991/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Opera";v="102"', # noqa
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0', # noqa
    }

    # среди параметров экспериментальным методом было обнаружено, что
    # необходим только city_code
    params = {
        'section_code': '1524',
        'city_code': 'msk',
        'client_id': 'pet_site',
    }
    petrovich_api = requests.get(
        f'https://api.petrovich.ru/catalog/v3/products/{item_id}',
        cookies=cookies,
        headers=headers,
        params=params
    ).text

    data = json.loads(petrovich_api)
    features = data['data']['product']
    if len(units) == 1:
        unit_1_price_card = \
            f'Цена за {units[0]} по карте: {features["price"]["gold"]}'
        unit_1_price_retail = \
            f'Цена за {units[0]}: {features["price"]["retail"]}'
        return unit_1_price_card + '\n' + unit_1_price_retail
    else:
        unit_1_price_card = \
            f'Цена за {units[0]} по карте: {features["price"]["gold"]}'
        unit_1_price_retail = \
            f'Цена за {units[0]}: {features["price"]["retail"]}'
        unit_2_price_card = \
            f'Цена за {units[1]} по карте: {features["price_alt"]["gold"]}'
        unit_2_price_retail = \
            f'Цена за {units[1]}: {features["price_alt"]["retail"]}'
        return (unit_1_price_card +
                '\n' + unit_1_price_retail +
                '\n' + unit_2_price_card +
                '\n' + unit_2_price_retail)


def main():
    print('URL:', CURRENT_URL)
    soup = fetch_soup(CURRENT_URL)
    print('------------')
    print('Название:', get_title(soup))
    print('------------')
    print('Артикул:', get_vendor_code(soup))
    print('------------')
    print(get_price(soup))
    print('------------')
    print('Список ссылок на картинки:', get_images(soup))
    print()


if __name__ == "__main__":
    main()
