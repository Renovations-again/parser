# import asyncio
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    '''Base model derived from DeclarativeBase class.'''

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
    )

    def __repr__(self) -> str:
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return self.__class__.__name__

    __str__ = __repr__


class Product(Base):
    '''Product sqlalchemy model.'''

    __tablename__ = 'products'

    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    unit: Mapped[str] = mapped_column(String(50))
    vendor_code: Mapped[str] = mapped_column(String(50), index=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'))
    shop: Mapped['Shop'] = relationship(back_populates='product')
    city: Mapped[list['City']] = relationship(
        back_populates='product'
    )

    def __repr__(self):
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return '<City id: {id}, title: {title}>'.format(
            id=self.id,
            title=self.title,
        )


class Shop(Base):
    '''Shop sqlalchemy model.'''

    __tablename__ = 'shops'

    title: Mapped[str] = mapped_column(String(250))
    product: Mapped[list['Product']] = relationship(
        back_populates='shop'
    )

    def __repr__(self):
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return '<Shop id: {id}, title: {title}>'.format(
            id=self.id,
            title=self.title,
        )


class City(Base):
    '''Price sqlalchemy model.'''

    __tablename__ = 'cities'

    title: Mapped[str] = mapped_column(String(250), unique=False)
    price_id: Mapped[int] = mapped_column(ForeignKey('prices.id'))
    product: Mapped['Product'] = relationship(back_populates='city')
    price: Mapped[list['Price']] = relationship(
        back_populates='city'
    )

    def __repr__(self):
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return '<Price id: {id}, title: {title}>'.format(
            id=self.id,
            title=self.title,
        )


class Price(Base):
    '''Price sqlalchemy model.'''

    __tablename__ = 'prices'

    price: Mapped[float] = mapped_column(Numeric(10, 2))
    date = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )
    city: Mapped['City'] = relationship(back_populates='price')

    def __repr__(self):
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return '<Price id: {id}, title: {title}>'.format(
            id=self.id,
            title=self.title,
        )
