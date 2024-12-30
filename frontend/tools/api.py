import json
from typing import Any, Dict, List

import aiohttp
import pandas as pd
from tools.config import API_URL


class ApiClient:
    """
    Клиент для взаимодействия с REST API.

    :param base_url: Базовый URL для API.
    """
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}

    async def sync_data(self) -> str:
        """
        Забирает данные из s3 на API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + '/sync_data') as response:
                resp = await response.json()
                return resp['status']

    async def get_data(self) -> None:
        """
        Получает данные из API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + '/get_data') as response:
                data = await response.json()
                data = pd.DataFrame(data['data'])
                data.to_csv('./data/cbr-press-releases.csv')

    async def get_models(self, url: str) -> List[str]:
        """
        Получает список моделей из API.

        :param url: Путь к API для получения списка моделей.
        :return: Список идентификаторов моделей.
        """
        async with aiohttp.ClientSession() as session:
            full_url = self.base_url + url
            async with session.get(full_url) as response:
                models = await response.json()
                return models['models']

    async def predict(self, url: str, model_id: str, release: str) -> Dict[str, Any]:
        """
        Запрашивает предсказание от указанной модели.

        :param url: Путь к API для предсказания.
        :param model_id: Идентификатор модели.
        :param release: Текст пресс-релиза
        :return: Ответ от API с результатами предсказания.
        """
        full_url = self.base_url + url
        async with aiohttp.ClientSession() as session:
            payload = {'model_id': model_id, 'release': release}
            async with session.post(full_url, headers=self.headers, json=payload) as response:
                answer = await response.json()
                return answer

    async def load_data(self, url: str, data: Any) -> Dict[str, Any]:
        """
        Загружает данные в API.

        :param url: Путь к API для загрузки данных.
        :param data: Данные в формате pandas DataFrame.
        :return: Ответ от API после загрузки данных.
        """
        async with aiohttp.ClientSession() as session:
            full_url = self.base_url + url
            payload = data.to_json(orient='records')  # Преобразование данных в JSON
            payload = json.loads(payload)
            payload = {'data': payload[:-1]}  # Исключение последней записи (если необходимо)
            async with session.post(full_url, headers=self.headers, json=payload) as response:
                ans = await response.json()
                return ans

    async def fit(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет запрос на обучение модели с заданными данными.

        :param url: Путь к API для обучения модели.
        :param payload: Данные для обучения в формате словаря.
        :return: Ответ от API после обучения.
        """
        async with aiohttp.ClientSession() as session:
            full_url = self.base_url + url
            async with session.post(full_url, headers=self.headers, json=payload) as response:
                ans = await response.json()
                return ans

    async def calc_metrics(self, model_id: str) -> Dict[str, Any]:
        """
        Получает данные для вычисления метрик.

        :param url: Путь к API для вычисления метрик.
        :param model_id: Идентификатор модели.
        :return: Ответ от API с данными для вычисления метрик.
        """
        async with aiohttp.ClientSession() as session:
            full_url = self.base_url + f'/calc_metrics/{model_id}/30'
            async with session.get(full_url) as response:
                ans = await response.json()
                return ans

    async def remove_all(self):
        """
        Удаляет все данные и модели из API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(self.base_url + '/remove_all') as response:
                ans = await response.json()
                return ans


# Создание экземпляра клиента с базовым URL
client = ApiClient(API_URL)
