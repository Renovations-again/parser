from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Парсер строительных магазинов'
    app_description: str = ('Имеется 5 магазинов. У каждого свой эндпоинт. '
                            'Передаем ссылку на товар - получаем Название, '
                            'Артикул, Цену, Единицу измерения '
                            'и Список изображений товара.')

    class Config:
        env_file = '.env'


settings = Settings()
