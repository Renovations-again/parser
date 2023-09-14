import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = 'https://moscow.petrovich.ru/catalog/9575968/987260/'  # стул
URL2 = 'https://moscow.petrovich.ru/catalog/12454/685400/'  # дверь
URL3 = 'https://moscow.petrovich.ru/catalog/245046398/620133/'  # плитка

CURRENT_URL = URL3

request = requests.get(CURRENT_URL)
soup = BeautifulSoup(request.text, 'lxml')


def get_title():
    '''Get the name of an item (Название товара)'''
    title = soup.find('h1').text
    return title


def get_vendor_code():
    '''Get vendor code of an item (Артикул товара)'''
    vendor_code = soup.find(
        'span', class_='pt-c-secondary-lowest'
    ).next_sibling.text
    return vendor_code


def get_images():
    '''Returns a list of all the images of an item (Ссылки на картинки)'''
    images = soup.find_all('img', class_="swiper-lazy")
    link_images = []
    for image in images:
        src = image.get('src')
        link_images.append(src)
    return list(set(link_images))


def get_price():
    '''Get the price of an item (Цена товара)'''
    prices = soup.find('div', class_='price-details')
    units = soup.find('span', class_='units-tabs')

    # Если детей (тегов <p>) > 1, то цены две: по карте и обычная
    children_price = list(prices.children)
    children_unit = list(units.children)

    # Прасим цены для разных единиц измерения (units)
    with sync_playwright() as p:  # noqa: E999
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(CURRENT_URL)
        # Если len(children_unit) > 2, то юнитов цены больше одного
        if len(children_unit) > 2:
            unit_text = page.query_selector('span[class="active unit-tab"]')
            print('Цена за ', unit_text.text_content())
            if len(children_price) == 1:
                print('Цена:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
            else:
                print('Цена по карте:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
                print('Цена не по карте:', float(
                    page.query_selector(
                        'p[data-test="product-retail-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
            unit_text = page.query_selector('span[class="unit-tab"]')
            unit_text.click()

            print('/'*50)
            print('Цена за ', unit_text.text_content())

            if len(children_price) == 1:
                print('Цена:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
            else:
                print('Цена по карте:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
                print('Цена не по карте:', float(
                    page.query_selector(
                        'p[data-test="product-retail-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
        else:
            print('Цена за ', children_unit[1].text)
            if len(children_price) == 1:
                print('Цена:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
            else:
                print('Цена по карте:', float(
                    page.query_selector(
                        'p[data-test="product-gold-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))
                print('Цена не по карте:', float(
                    page.query_selector(
                        'p[data-test="product-retail-price"]'
                    ).text_content().replace('₽', '').replace(' ', '').
                    replace(',', '.')
                ))


print('Название:', get_title())
print('------------')
print('Артикул:', get_vendor_code())
print('------------')
print(get_price())
print('------------')
print('Список ссылок на картинки:', get_images())
