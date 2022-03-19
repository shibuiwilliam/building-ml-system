from typing import List

from pydantic import BaseModel, Extra


class AnimalFeatureInitializeRequest(BaseModel):
    mlflow_experiment_id: int
    mlflow_run_id: str

    class Config:
        extra = Extra.forbid


class AnimalFeatureRegistrationRequest(BaseModel):
    mlflow_experiment_id: int
    mlflow_run_id: str

    class Config:
        extra = Extra.forbid
