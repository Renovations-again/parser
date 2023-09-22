import urllib.parse as parse

url = 'https://moscow.petrovich.ru/catalog/9575968/987260/'

if url.endswith('/'):
    print(url.split('/')[-2])
else:
    print(url.split('/')[-1])
