from .database import async_session_maker
from .models import Product, Shop, Price, City

from test_csv import get_data_from_csv


async def insert_data_vodopad():
    async with async_session_maker() as session:
        for item in get_data_from_csv():
            example_insertion_city = City(
                title=item['city']
            )  # , price_id=City.id)
            example_insertion_product = Product(
                title=item['title'],
                url=item['url'],
                unit=item['unit'],
                vendor_code=item['vendor_code'],
            )
            example_insertion_price = Price(
                price=item['price'],
                date=item['date'],
            )
            example_insertion_shop = Shop(title=item['shop'])

            session.add_all([
                example_insertion_city,
                example_insertion_price,
                example_insertion_shop,
                example_insertion_product,
            ])
            # session.add(example_insertion_city)
            # session.add(example_insertion_product)
            # session.add(example_insertion_price)
            # session.add(example_insertion_shop)
        await session.commit()
