from pydantic import BaseModel
from typing import Optional


class PredictionRange(BaseModel):
    min: float
    max: float


class PredictionResult(BaseModel):
    prediction: float
    confidence: float
    explanation: str
    range: PredictionRange
    risk: str  # low / medium / high


class ViewPrediction(BaseModel):
    views: PredictionResult
    ctr: PredictionResult
    retention: PredictionResult


class CTRPrediction(BaseModel):
    ctr: PredictionResult


class RevenuePrediction(BaseModel):
    revenue: PredictionResult
    rpm_range: PredictionRange


class RetentionPrediction(BaseModel):
    retention: PredictionResult
    avg_watch_time: PredictionResult


class SimulateRequest(BaseModel):
    topic: str
    title: str = ""
    description: str = ""


class SimulateResponse(BaseModel):
    topic: str
    views: PredictionResult
    ctr: PredictionResult
    retention: PredictionResult
    revenue: RevenuePrediction
