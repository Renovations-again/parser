from urllib.parse import urlparse

from fastapi import HTTPException

from resources.constants import DOMAINS_SHOPS


def validate_domain(url):
    parsed_url = urlparse(url)
    domain = '.'.join(parsed_url.netloc.split('.')[-2:])
    if domain not in DOMAINS_SHOPS:
        raise HTTPException(
            status_code=422,
            detail='Неверная ссылка',
        )
