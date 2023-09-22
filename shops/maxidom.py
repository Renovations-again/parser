import requests
from bs4 import BeautifulSoup

URL = 'https://www.maxidom.ru/catalog/vata-mineralnaya/1000947410/'

request = requests.get(URL)
soup = BeautifulSoup(request.text, 'lxml')

h1 = soup.find('h1')
code = soup.find('div', class_='flypage__lineinfo-code')

price = soup.find('div', class_='lvl1__product-body-buy-price')

print(h1.text)
print(code.text)
print(price)
