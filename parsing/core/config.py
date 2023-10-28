from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Парсер строительных магазинов'
    app_description: str = ('Имеется 5 магазинов. У каждого свой эндпоинт. '
                            'Передаем ссылку на товар - получаем Название, '
                            'Артикул, Цену, Единицу измерения '
                            'и Список изображений товара.')

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def db_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'  # noqa

    class Config:
        env_file = '.env'


settings = Settings()
