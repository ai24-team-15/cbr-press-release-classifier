FROM python:3.11.11-slim

RUN pip install poetry  
RUN mkdir -p /app  
COPY . /app

WORKDIR /app

RUN poetry install --without dev
CMD ["poetry", "run", "streamlit", "run", "main.py"]
