import os
import uvicorn
from typing import Optional, Union
from fastapi import FastAPI
from models import (
    DataResponse,
    FitResponse,
    ModelsResponse,
    PredictResponse,
    StatusResponse,
    SyncDataResponse,
)


if not os.path.exists("../data/"):
    os.mkdir("../data")



app = FastAPI(
    title='cbr_press_release_classifier',
    version='1.0.0',
)


@app.get('/', response_model=StatusResponse)
def root() -> StatusResponse:
    """
    Root
    """
    return StatusResponse(status='Works!')


@app.get(
    '/fit/{model_id}', response_model=None, responses={'201': {'model': FitResponse}}
)
def fit(model_id: str) -> Optional[FitResponse]:
    """
    Fit
    """
    pass


@app.get('/get_data', response_model=DataResponse)
def get_data() -> DataResponse:
    """
    Get Data
    """
    pass


@app.get('/get_models', response_model=ModelsResponse)
def get_status() -> ModelsResponse:
    """
    Get Status
    """
    pass


@app.get(
    '/predict/{model_id}',
    response_model=None,
    responses={'201': {'model': PredictResponse}},
)
def predict(model_id: str) -> Optional[PredictResponse]:
    """
    Predict
    """
    pass


@app.get('/sync_data', response_model=SyncDataResponse)
def sync_data() -> SyncDataResponse:
    """
    Sync Data
    """
    pass



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
