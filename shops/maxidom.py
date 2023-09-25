import requests
from bs4 import BeautifulSoup

# паркетная доска https://www.maxidom.ru/catalog/parket/1001248398/
URL = 'https://www.maxidom.ru/catalog/ugolki/1000786934/'  # Уголок крепёжный


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
            'div', class_='flypage__lineinfo-code'
            ).text
    return None


def get_price(soup):
    '''Get the price of an item (Цена товара)'''

    # get price_1
    price_block = soup.select('div.lvl1__product-body-buy-price-base')
    for p in price_block:
        price_unit_1 = int(p.get('data-repid_price'))
        break

    # get unit_1
    price_block = soup.find('div', class_='lvl1__product-body-buy-price-base')
    unit_1 = price_block.find(
        'span', class_='lvl1__product-body-buy-price-measure'
    ).contents[0]

    return (f'{price_unit_1} {unit_1}')


def get_images(soup):
    '''Returns a list of all the images of an item (Ссылки на картинки)'''
    img_block = soup.find('div', {'id': 'flypage_slider_large_vertical_base'})
    images = img_block.find('div', class_='swiper-wrapper').findChildren()
    link_images = [image.get('src') for image in images if image.get('src')]
    return link_images


def main():
    print('URL:', URL)
    soup = fetch_soup(URL)
    # print('------------')
    # print('Название:', get_title(soup))
    # print('------------')
    # print('Артикул:', get_vendor_code(soup))
    print('------------')
    print('Цены:', get_price(soup))
    # print('------------')
    # print('Список ссылок на картинки:', get_images(soup))
    # print()


if __name__ == "__main__":
    main()
