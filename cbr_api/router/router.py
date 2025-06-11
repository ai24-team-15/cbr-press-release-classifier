import logging
import asyncio
from typing import Optional, Union
from concurrent.futures.process import ProcessPoolExecutor
import urllib.request
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pydantic import TypeAdapter
from fastapi import APIRouter, Response, Request, status
from models.models import (
    Model,
    DataModel,
    HTTPValidationError,
    ModelsResponse,
    PredictRequest,
    PredictResponse,
    CalcResponse,
    StatusResponse,
)
from tools.utils import (
    preprocessor,
    preprocessor_knn,
    prepare_data,
    train_model,
    calc_metrics_utils,
    load_data_from_file,
)
from tools.settings import settings


executor = ProcessPoolExecutor(settings.threads_count)


async def run_in_process(fn, *args):
    "Запускает переданную функцию в фоновом режиме"
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, fn, *args)


router = APIRouter()


@router.get("/", response_model=StatusResponse)
async def root(request: Request) -> StatusResponse:
    """
    Информация о статусе сервиса.
    """
    return StatusResponse(
        status=f"Сервис работает. Данных {len(request.app.data)}, моделей {len(request.app.ml_models)}"
    )


@router.post("/fit", response_model=None, responses={"200": {"model": StatusResponse}})
async def fit(body: Model, request: Request) -> Optional[StatusResponse]:
    """
    Обучает выбранную модель
    """
    if body.model_id in request.app.ml_models:
        answer = f"Модель {body.model_id} уже существует"
        logging.info(answer)
        return StatusResponse(status=answer)
    if len(request.app.data) == 0:
        answer = "Нет данных для обучения"
        logging.info(answer)
        return StatusResponse(status=answer)
    clf = None
    if body.type == "LogisticRegression":
        clf = LogisticRegression(
            **body.hyperparameters, random_state=settings.random_state
        )
    elif body.type == "SVC":
        clf = SVC(**body.hyperparameters, random_state=settings.random_state)
    elif body.type == "KNN":
        clf = KNeighborsClassifier(**body.hyperparameters)
    transform = ColumnTransformer(
        [("tf-idf", TfidfVectorizer(preprocessor=preprocessor), "release")]
    )
    pipeline = Pipeline([("transform", transform), ("classifier", clf)])
    X, y, _ = prepare_data(request.app.data)
    pipeline = await run_in_process(train_model, pipeline, X, y)
    # pipeline.fit(X, y)
    request.app.ml_models[body.model_id] = {
        "description": body.description,
        "hyperparameters": body.hyperparameters,
        "pipeline": pipeline,
        "type": body.type,
    }
    answer = f"Модель {body.model_id} обучена"
    logging.info(answer)
    return StatusResponse(status=answer)


@router.get(
    "/calc_metrics/{model_id}/{window}",
    response_model=None,
    responses={"200": {"model": CalcResponse}},
)
async def calc_metrics(
    model_id: str, window: int, request: Request
) -> Union[StatusResponse, CalcResponse]:
    """
    Обучает на части данных и запоминает метрики
    """
    if model_id not in request.app.ml_models:
        answer = f"Модель {model_id} не добавлена"
        logging.info(answer)
        return StatusResponse(status=answer)
    if (len(request.app.data)) == 0 or (window >= len(request.app.data)):
        answer = "Нет данных для обучения"
        logging.info(answer)
        return StatusResponse(status=answer)
    clf = None
    X, y, _ = prepare_data(request.app.data)
    if request.app.ml_models[model_id]["type"] == "LogisticRegression":
        clf = LogisticRegression(**request.app.ml_models[model_id]["hyperparameters"])
        vec = TfidfVectorizer(preprocessor=preprocessor)
    elif request.app.ml_models[model_id]["type"] == "SVC":
        clf = SVC(**request.app.ml_models[model_id]["hyperparameters"])
        vec = TfidfVectorizer(preprocessor=preprocessor)
    elif request.app.ml_models[model_id]["type"] == "KNN":
        clf = KNeighborsClassifier(**request.app.ml_models[model_id]["hyperparameters"])
        vec = TfidfVectorizer(preprocessor=preprocessor_knn)
    
    X_tfidf = vec.fit_transform(X["release"])
    res = await run_in_process(calc_metrics_utils, clf, X_tfidf, y, window)
    return CalcResponse(y_preds=res[0], y_pred_probas=res[1], y_trues=res[2])


@router.get("/get_data", response_model=DataModel)
async def get_data(request: Request) -> DataModel:
    """
    Возвращает данные
    """
    ta = TypeAdapter(DataModel)
    return ta.validate_python({"data": request.app.data})


@router.get("/get_models", response_model=ModelsResponse)
async def get_status(request: Request) -> ModelsResponse:
    """
    Возвращает список реализованных моделей
    """
    res = []
    for key, value in request.app.ml_models.items():
        m = Model(
            model_id=key,
            hyperparameters=value["hyperparameters"],
            description=value["description"],
            type=value["type"],
        )
        res.append(m)
    return ModelsResponse(models=res)


@router.post(
    "/load_data",
    response_model=None,
    responses={
        "201": {"model": StatusResponse},
        "422": {"model": HTTPValidationError},
    },
)
async def load_data(
    body: DataModel, response: Response, request: Request
) -> Optional[Union[StatusResponse, HTTPValidationError]]:
    """
    Загрузка дополнительных данных
    """
    body_dict = body.model_dump()
    for b in body_dict["data"]:
        found = next(
            (item for item in request.app.data if item["date"] == b["date"]),
            None,
        )
        if found is None:
            request.app.data.append(b)
            logging.info("Для даты %s информация добавлена.", b["date"])
        else:
            new_fields = []
            changed_fields = []
            for key, value in b.items():
                if (key == "date") or (key in found and found[key] == value):
                    continue
                if key in found:
                    changed_fields.append(key)
                else:
                    new_fields.append(key)
                found[key] = value
            additional_log = ""
            if len(new_fields) > 0:
                additional_log += f" Добавлены поля {new_fields}."
            if len(changed_fields) > 0:
                additional_log += f" Изменены поля {changed_fields}."
            if additional_log != "":
                logging.info(
                    "Для даты %s информация изменена.%s",
                    b["date"],
                    additional_log,
                )
    response.status_code = status.HTTP_201_CREATED
    return StatusResponse(status="Данные успешно загружены")


@router.post(
    "/predict", response_model=None, responses={"200": {"model": PredictResponse}}
)
async def predict(
    body: PredictRequest, request: Request
) -> Union[PredictResponse, StatusResponse]:
    """
    Делает прогноз с помощью указанной модели
    """
    if body.model_id not in request.app.ml_models:
        answer = f"Модель {body.model_id} не загружена"
        logging.info(answer)
        return StatusResponse(status=answer)
    _, _, last_release = prepare_data(request.app.data)
    if body.release is not None:
        last_release.release = body.release
    pred = request.app.ml_models[body.model_id]["pipeline"].predict(last_release)[0]
    pred_proba = request.app.ml_models[body.model_id]["pipeline"].predict_proba(
        last_release
    )[0]
    return PredictResponse(predict=pred, predict_proba=pred_proba)


@router.get("/sync_data", response_model=StatusResponse)
async def sync_data(request: Request) -> StatusResponse:
    """
    Запускает получение данных
    """
    try:
        urllib.request.urlretrieve(
            "https://storage.yandexcloud.net/cbr-press-release-classifier/cbr-press-releases.csv",
            f"{settings.data_path}/data_s3.csv",
        )
        request.app.data = load_data_from_file(
            filename=f"{settings.data_path}/data_s3.csv"
        )
        answer = f"Данные с S3 успешно загружены ({len(request.app.data)})"
    except urllib.error.HTTPError as e:
        answer = f"Ошибка загрузки данных с S3 ({e})"
    logging.info(answer)
    return StatusResponse(status=answer)


@router.delete("/remove_all", response_model=StatusResponse)
async def remove_all(request: Request):
    """
    Удаляет из сервиса модели и данные
    """
    request.app.ml_models = {}
    request.app.data = []
    return StatusResponse(status="Все данные и модели удалены")
