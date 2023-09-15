import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = 'https://moscow.petrovich.ru/catalog/9575968/987260/'  # стул
URL2 = 'https://moscow.petrovich.ru/catalog/12454/685400/'  # дверь
URL3 = 'https://moscow.petrovich.ru/catalog/245046398/620133/'  # плитка

CURRENT_URL = URL2


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
    prices = soup.find('div', class_='price-details')
    units = soup.find('span', class_='units-tabs')

    # Если детей (тегов <p>) > 1, то цены две: по карте и обычная
    children_price = list(prices.children)
    children_unit = list(units.children)

    def print_price():
        golden_price = float(
            page.query_selector('p[data-test="product-gold-price"]')
                .text_content()
                .replace('₽', '')
                .replace(' ', '')
                .replace(',', '.')
        )
        price = float(
            page.query_selector('p[data-test="product-retail-price"]')
                .text_content()
                .replace('₽', '')
                .replace(' ', '')
                .replace(',', '.')
        )
        if len(children_price) == 1:
            print(golden_price)
        else:
            print('  цена по карте:', golden_price)
            print('  цена не по карте:', price)

    # Прасим цены для разных единиц измерения (units)
    with sync_playwright() as p:  # noqa: E999
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(CURRENT_URL)
        # Если len(children_unit) > 2, то юнитов цены больше одного
        if len(children_unit) > 2:
            unit_text = page.query_selector(
                'span[class="active unit-tab"]'
            )
            print(f'Цена за {unit_text.text_content()}:')
            print_price()
            unit_text = page.query_selector('span[class="unit-tab"]')
            unit_text.click()

            print('/'*50)
            print(f'Цена за {unit_text.text_content()}:')
            print_price()
        else:
            print(f'Цена за {children_unit[1].text}:')
            print_price()


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
