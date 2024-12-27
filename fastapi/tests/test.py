import httpx
from csv import DictReader
import json


def load_data_from_file(filename):
    result = []
    with open(filename, "r", encoding="UTF-8") as f:
        reader = DictReader(f)
        for row in reader:
            result.append(row)
    return result


SERVER_NAME = "http://localhost:8000/"


def test_status():
    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_send_from_file():
    r = httpx.get(SERVER_NAME + "get_data")
    assert r.status_code == 200

    data = load_data_from_file("../data/cbr-press-releases.csv")
    step = 10
    for i in range(0, len(data), step):
        r = httpx.post(
            SERVER_NAME + "load_data",
            content=json.dumps({"data": data[i: i + step]}),
        )
        assert r.status_code == 201

    r = httpx.get(SERVER_NAME + "get_data")
    assert r.status_code == 200


def test_fit_1():
    print("\nTest fit 01")
    r = httpx.post(
        SERVER_NAME + "fit",
        content="""{
                   "model_id": "Model_01",
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
    print("\nTest fit 02")
    r = httpx.post(
        SERVER_NAME + "fit",
        content="""{
                   "model_id": "Model_02",
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
    print("\nTest get_models")
    r = httpx.get(SERVER_NAME + "get_models")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_predict():
    print("\nTest predict")
    r = httpx.get(SERVER_NAME + "predict/Model_01")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200

    r = httpx.get(SERVER_NAME + "predict/Model_02")
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200


def test_status_arter():
    r = httpx.get(SERVER_NAME)
    print(f"HTTP Code = {r.status_code}, answer {r.text}")
    assert r.status_code == 200
