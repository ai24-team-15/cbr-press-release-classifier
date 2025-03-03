from __future__ import annotations
from typing import List, Dict, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class StatusResponse(BaseModel):
    status: str = Field(..., title="Status")


class Datum(BaseModel):
    date: str
    link: Optional[str] = None
    title: Optional[str] = None
    release: Optional[str] = None
    inflation: Optional[float] = None
    rate: Optional[float] = None
    usd: Optional[float] = None
    usd_cur_change_relative: Optional[float] = None
    target_categorial: Optional[int] = None
    target_absolute: Optional[float] = None
    target_relative: Optional[float] = None

    @field_validator(
        "inflation",
        "rate",
        "usd",
        "usd_cur_change_relative",
        "target_categorial",
        "target_absolute",
        "target_relative",
        mode="before",
    )
    # pylint: disable=E0213
    def blank_string(cls, value):
        "Превращает пустую строку в None"
        if value == "":
            return None
        return value


class DataModel(BaseModel):
    data: Optional[List[Datum]] = Field(None, title="Data")


class Model(BaseModel):
    model_id: str
    description: Optional[str] = None
    hyperparameters: Dict
    type: ModelType


class ModelsResponse(BaseModel):
    models: List[Model] = Field(..., title="Models")


class ModelType(str, Enum):
    log = "LogisticRegression"
    svc = "SVC"


class PredictRequest(BaseModel):
    model_id: str
    release: Optional[str] = None


class PredictResponse(BaseModel):
    predict: int = Field(..., title="Prediction")
    predict_proba: List[float] = Field(..., title="Probability estimates")


class CalcResponse(BaseModel):
    y_preds: List[int] = Field(..., title="Prediction values")
    y_pred_probas: List[List[float]] = Field(..., title="Probability estimates")
    y_trues: List[int] = Field(..., title="Prediction values")


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title="Detail")
