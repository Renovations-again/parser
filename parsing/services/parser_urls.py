from urllib.parse import urlparse

from resources.constants import CITY_PETROVICH


def parser_url_petrovich(url):
    parsed_url = urlparse(url)
    path = urlparse(url).path
    category = path.split('/')
    city_domen = parsed_url.netloc.split('.')
    city_code = 'rf'
    if city_domen[0] in CITY_PETROVICH:
        city_code = CITY_PETROVICH[city_domen[0]]
    return parsed_url, category, city_code
