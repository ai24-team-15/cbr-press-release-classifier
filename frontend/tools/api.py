import os
import json

import aiohttp


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    async def get_models(self, url):
        async with aiohttp.ClientSession() as session:
            url = self.base_url + url
            async with session.get(url) as response:
                models = await response.json()
                return models['models']
            
    async def predict(self, url, model_id):
        url = self.base_url + url
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}/{model_id}') as response:
                answer = await response.json()
                return answer
            
    async def load_data(self, url, data):        
        async with aiohttp.ClientSession() as session:
            url = self.base_url + url
            payload = data.to_json(orient='records')
            payload = json.loads(payload)
            payload = {'data': payload[:-1]}
            async with session.post(url, headers=self.headers, json=payload) as response:
                ans = await response.json()
                return ans
            
    async def fit(self, url, payload):
        async with aiohttp.ClientSession() as session:
            url = self.base_url + url
            async with session.post(url, headers=self.headers, json=payload) as response:
                ans = await response.json()
                return ans
            
client = ApiClient('http://0.0.0.0:8000')

    # def post(self, endpoint, **kwargs):
    #     """POST запрос с базовым URL."""
    #     url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    #     return self.session.post(url, **kwargs)



# async def get_models(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             models = await response.json()
#             return models