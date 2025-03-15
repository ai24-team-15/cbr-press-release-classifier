from csv import DictReader
import json
import httpx


def load_data_from_file(filename) -> list[dict]:
    """
    Считывает csv файл в список словарей
    """
    result = []
    with open(filename, "r", encoding="UTF-8") as f:
        reader = DictReader(f)
        for row in reader:
            result.append(row)
    return result


SERVER_NAME = "http://localhost:8000/"


def test_status():
    """
    Тестирует статус сервиса
    """
    print("\nTest before load data")
    r = httpx.delete(SERVER_NAME + "remove_all")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200

    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_sync_data():
    """
    Тестирует загрузку данных с S3
    """
    print("\nTest sync data")
    r = httpx.get(SERVER_NAME + "sync_data")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200

    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_send_from_file():
    """
    Тестирует загрузку данных из файла
    """
    print("\nTest load data from file")
    r = httpx.get(SERVER_NAME + "get_data")
    assert r.status_code == 200

    data = load_data_from_file("data/cbr-press-releases.csv")
    step = 10
    for i in range(0, len(data), step):
        r = httpx.post(
            SERVER_NAME + "load_data",
            content=json.dumps({"data": data[i: i + step]}),
        )
        assert r.status_code == 201

    r = httpx.get(SERVER_NAME + "get_data")
    assert r.status_code == 200


def test_status_after_add():
    """
    Тестирует статус сервиса
    """
    print("\nTest after load data")
    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_fit_1():
    """
    Тестирует обучение первой модели
    """
    print("\nTest fit 01")
    r = httpx.post(
        SERVER_NAME + "fit",
        content="""{
                   "model_id": "Model_SVC",
                   "description": "SVC model with best hyperparameters",
                   "hyperparameters": {
                        "C": 5,
                        "kernel": "linear",
                        "probability": true
                    },
                   "type": "SVC"}""",
        timeout=1000.0,
    )
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_fit_2():
    """
    Тестирует обучение второй модели
    """
    print("\nTest fit 02")
    r = httpx.post(
        SERVER_NAME + "fit",
        content="""{
                   "model_id": "Model_LR",
                   "description":
                        "LogisticRegression model with best hyperparameters",
                   "hyperparameters": {
                        "C": 10,
                        "l1_ratio": 0.1,
                        "max_iter": 10000,
                        "penalty": "elasticnet",
                        "solver": "saga"
                    },
                   "type": "LogisticRegression"}""",
        timeout=1000.0,
    )
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_get_models():
    """
    Тестирует получение информации о моделях
    """
    print("\nTest get_models")
    r = httpx.get(SERVER_NAME + "get_models")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_predict():
    """
    Тестирует прогноз двух моделей
    """
    print("\nTest predict")
    r = httpx.post(SERVER_NAME + "predict", content="""{"model_id": "Model_SVC"}""")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200

    r = httpx.post(SERVER_NAME + "predict", content="""{"model_id": "Model_LR"}""")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_predict_with_release():
    """
    Тестирует прогноз двух моделей с заданным релизом
    """
    print("\nTest predict with release")
    r = httpx.post(
        SERVER_NAME + "predict",
        content="""{"model_id": "Model_SVC", "release": "Ставка будет повышена"}""",
        timeout=1000.0
    )
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200

    r = httpx.post(
        SERVER_NAME + "predict",
        content="""{"model_id": "Model_LR", "release": "Ставка будет повышена"}""",
        timeout=1000.0
    )
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_status_after():
    """
    Тестирует статус сервиса с обученными моделями
    """
    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_calc_metrics():
    """
    Тестирует получение данных обучения
    """
    print("\nTest calc metrics")
    r = httpx.get(SERVER_NAME + "calc_metrics/Model_SVC/30", timeout=1000.0)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200
