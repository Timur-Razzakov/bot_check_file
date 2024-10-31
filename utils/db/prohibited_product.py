from sqlalchemy import Column, Integer, String, select
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from .base import Base


class ProhibitedProduct(Base):
    __tablename__ = 'prohibited_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)

    def __init__(self, product_name, **kw: Any):
        super().__init__(**kw)
        self.product_name = product_name

    @property
    def stats(self) -> str:
        return ""

    def __str__(self) -> str:
        return f"<prohibited_product:{self.id}>"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    async def get_all_prohibited_product(session_maker: sessionmaker):
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(select(ProhibitedProduct.product_name).distinct())
                countries = [row[0] for row in result]
                return countries

    @staticmethod
    async def create_prohibited_products(product_names: list[str], session_maker: sessionmaker) -> None:
        async with session_maker() as session:
            async with session.begin():
                products = [ProhibitedProduct(product_name=product_name) for product_name in product_names]
                try:
                    session.add_all(products)
                    await session.commit()  # Сохранить изменения
                except ProgrammingError as e:
                    await session.rollback()
                    pass

    # Функция удаления записи из таблицы "countries"
    @staticmethod
    async def delete_prohibited_products_by_name(product_names: str, session_maker: sessionmaker):
        async with session_maker() as session:
            async with session.begin():
                prohibited_product = await session.get(ProhibitedProduct, product_names)
                if prohibited_product:
                    try:
                        await session.delete(prohibited_product)
                        await session.commit()  # Сохранить изменения
                    except Exception as e:
                        session.rollback()  # Откатить изменения в случае ошибки
                else:
                    return "Страна не найдена"
