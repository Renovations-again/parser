# from .database import async_session_maker
# from .models import Shop


# def insert_data():
#     with async_session_maker() as session:
#         shop_example = Shop(title='Vodopad')
#         session.add_all([shop_example])
#         session.commit()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Shop

# Create the engine and sessionmaker
engine = create_engine(
    'postgresql+asyncpg://david:-\P>S(1s{*c=~<@80.90.185.151:5432/opyat_remont_dev'  # noqa
)
Session = sessionmaker(bind=engine)


def insert_data():
    # Create a new Shop instance with the provided title
    shop = Shop()

    # Create a new session
    session = Session()

    try:
        # Add the shop object to the session
        session.add(shop)

        # Commit the session to persist the changes
        session.commit()
        print("Data inserted successfully!")
    except Exception as e:
        # Rollback the session in case of any error
        session.rollback()
        print("Failed to insert data:", str(e))
    finally:
        # Close the session
        session.close()
