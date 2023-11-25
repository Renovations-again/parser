from .database import async_session_maker
from .models import Shop


async def insert_data():
    async with async_session_maker() as session:
        shop_example = Shop(title='Vodopad')
        session.add(shop_example)
        await session.commit()
