import logging
from settings import settings
from fastapi import APIRouter, Response, Request, status
from pydantic import TypeAdapter
from models import (
    Model,
    DataModel,
    HTTPValidationError,
    ModelsResponse,
    PredictResponse,
    StatusResponse,
)
from typing import Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from utils import preprocessor, prepare_data


router = APIRouter()


@router.get("/", response_model=StatusResponse)
async def root(request: Request) -> StatusResponse:
    """
    Информация о статусе сервиса.
    """
    return StatusResponse(
        status=f"Сервис работает. Данных {len(request.app.data)}, моделей {len(request.app.ml_models)}"
    )


@router.post("/fit", response_model=None, responses={"201": {"model": StatusResponse}})
async def fit(body: Model, request: Request) -> Optional[StatusResponse]:
    """
    Обучает выбранную модель
    """
    if body.model_id in request.app.ml_models:
        answer = f"Модель '{body.model_id}' уже существует"
        logging.info(answer)
        return StatusResponse(status=answer)
    if len(request.app.data) == 0:
        answer = "Нет данных для обучения"
        logging.info(answer)
        return StatusResponse(status=answer)
    clf = None
    if body.type == "LogisticRegression":
        clf = LogisticRegression(**body.hyperparameters, random_state=settings.random_state)
    elif body.type == "SVC":
        clf = SVC(**body.hyperparameters, random_state=settings.random_state)
    transform = ColumnTransformer([("tf-idf", TfidfVectorizer(preprocessor=preprocessor), "release")])
    pipeline = Pipeline([("transform", transform), ("classifier", clf)])
    X, y, _ = prepare_data(request.app.data)
    pipeline.fit(X, y)
    request.app.ml_models[body.model_id] = {
        "description": body.description,
        "hyperparameters": body.hyperparameters,
        "pipeline": pipeline,
        "type": body.type,
    }
    answer = f"Модель '{body.model_id}' обучена"
    logging.info(answer)
    return StatusResponse(status=answer)


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


@router.get(
    "/predict/{model_id}",
    response_model=None,
    responses={"201": {"model": PredictResponse}},
)
async def predict(model_id: str, request: Request) -> Union[PredictResponse, StatusResponse]:
    """
    Делает прогноз с помощью указанной модели
    """
    if model_id not in request.app.ml_models:
        answer = f"Модель '{model_id}' не загружена"
        logging.info(answer)
        return StatusResponse(status=answer)
    _, _, last_release = prepare_data(request.app.data)
    predict = request.app.ml_models[model_id]["pipeline"].predict(last_release)[0]
    predict_proba = request.app.ml_models[model_id]["pipeline"].predict_proba(last_release)[0]
    return PredictResponse(predict=predict, predict_proba=predict_proba)


@router.get("/sync_data", response_model=StatusResponse)
async def sync_data() -> StatusResponse:
    """
    Запускает получение данных
    """
    pass
