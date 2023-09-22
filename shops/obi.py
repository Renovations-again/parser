import requests
from bs4 import BeautifulSoup

URL = 'https://obi.ru/products/keramogranit-lavit-amazonite-aqua-zelenyj-120h60-sm-5055062'  # noqa

try:
    request = requests.get(URL, headers={"Content-Type": "text"})
    request.raise_for_status()
    soup = BeautifulSoup(request.text, 'lxml')

    h1 = soup.find('h1')

    code = soup.find('span', class_='_2XlQF')

    price_block = soup.find_all('div', class_='_18Fo_')

    # price = soup.find_all('span', class_='_3IeOW')
    # unit = soup.find_all('span', class_='_3SDdj')

    prices = []
    units = []
    price_elements = soup.find_all('div', class_='_18Fo_')
    for price_element in price_elements:
        price = price_element.find('span', class_='_3IeOW').text.strip()
        unit = price_element.find('span', class_='_3SDdj').text.strip()
        prices.append(price)
        units.append(unit)

    print(h1.text)
    print(code.text)
    print(price_block)
    print(prices)
    print(units)

except requests.exceptions as err:
    print(f'Ошибка: {err}')
