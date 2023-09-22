import requests

import lxml  # noqa
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

domain = 'https://vodopad.ru'
url = 'https://www.oboykin.ru/catalog/russia/biber/plenka-zashhitnaya/31811/'  # noqa
headers = {
    'Accept': '*/*',
    'User-Agent': ua.random
}
html = requests.get(url, headers=headers).text
bs = BeautifulSoup(html, 'lxml')


def get_title():
    '''Get the name of an item (Название товара)'''
    try:
        # Здесь находим имя товара по тегу h1 (тег h1 представлен на странице
        # товара в единственном экземпляре).
        title = bs.find('h1')
        # У некоторых товаров есть дополнительное имя под основным. Чтобы его
        # достать, применяется метод fetchNextSiblings с заданным критерием
        # поиска (поиск тега <p>)
        if title.fetchNextSiblings('p'):
            verbose_name = title.fetchNextSiblings('p')[0].text
            return f'{title.text} ({verbose_name})'
        return title.text
    except AttributeError:
        print('<--Ошибка! Название товара не найдено-->')


def get_vendor_code():
    '''Get vendor code of an item (Артикул товара)'''
    try:
        description = bs.find(
            'div', class_='page-tovarpage__description__info'
        ).find('ul').find_all('li')
        for item in description:
            if item.find(string='Артикул'):
                # метод .find_next() помог найти следующий тег
                vendor_code = item.find(string='Артикул').find_next().text
        return vendor_code
    except AttributeError:
        print('<--Ошибка! Артикул товара не найден-->')


def get_price():
    '''Get the price of an item (Цена товара)'''
    try:
        identifier = bs.find('div', class_='page-tovarpage__price')
        price = identifier.find('div', class_='sum').text.replace(' ', '')
        units = identifier.find('div', class_='units').text
        if identifier.find('div', class_='page-tovarpage__price__special'):
            special = identifier.find(
                'div', class_='page-tovarpage__price__special'
            )
            spec_title = special.find(
                'span', string='Цена за упаковку:'
            ).text
            spec_price = special.find(class_='rub').text
            return f'Цена {units}: {float(price)}\n{spec_title} {spec_price}'
        return f'Цена {units}: {float(price)}'
    except AttributeError:
        print('<--Ошибка! У данного товара нет цены-->')


def get_images():
    '''Returns a list of all the images of an item (Ссылки на картинки)'''
    try:
        raw_images = bs.find('div', {'class': 'owl-carousel'}).find_all('a')
        images = []
        for item in raw_images:
            images.append(domain + item['href'])
        return images
    except AttributeError:
        print('<--Ошибка! Фото товара не найдено-->')


print('Название:', get_title())
print('------------')
print('Артикул:', get_vendor_code())
print('------------')
print('Цена:', get_price())
print('------------')
print('Список ссылок на картинки:', get_images())
