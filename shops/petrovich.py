import requests
from bs4 import BeautifulSoup

URL = 'https://moscow.petrovich.ru/catalog/9575968/987260/'  # стул
URL2 = 'https://moscow.petrovich.ru/catalog/12454/685400/'  # дверь
URL3 = 'https://moscow.petrovich.ru/catalog/245046398/620133/'  # плитка

request = requests.get(URL3)
soup = BeautifulSoup(request.text, 'lxml')

h1 = soup.find('h1')
code = soup.find('span', class_='pt-c-secondary-lowest').next_sibling
images = soup.find_all('img', class_="swiper-lazy")
link_images = []

prices = soup.find_all('div', class_='price-details')

units = soup.find('span', class_='units-tabs').find_all('span', class_='unit-tab')

for image in images:
    src = image.get('src')
    link_images.append(src)

print(h1.text, code.text, set(link_images), sep='\n')

for unit in units:
    print('Цена за', unit.get_text())


gold_price = soup.find('p', class_='gold-price')
retail_price = soup.find('p', class_='retail-price')

print('Цена по карте:', gold_price.text)
print('Цена:', retail_price.text)
