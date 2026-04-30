from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, validator

from app.services.ai_service import SUPPORTED_SPORTS


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6, max_length=72)


class PredictionRequest(BaseModel):
    team_a: str = Field(..., min_length=1)
    team_b: str = Field(..., min_length=1)
    sport: str = Field(default="football")

    @validator("sport", pre=True)
    def normalize_sport(cls, value):
        return value.lower()

    @validator("sport")
    def sport_supported(cls, value):
        if value not in SUPPORTED_SPORTS:
            raise ValueError(
                f"Unsupported sport '{value}'. Supported: {', '.join(SUPPORTED_SPORTS)}"
            )
        return value

    @model_validator(mode="after")
    def teams_must_be_different(cls, values):
        if values.team_a == values.team_b:
            raise ValueError("team_a and team_b must be different")
        return values


class PredictionResponse(BaseModel):
    id: int
    team_a: str
    team_b: str
    sport: str
    prediction: str
    confidence: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AIPredictionResponse(BaseModel):
    team_a: str
    team_b: str
    sport: str
    prediction: str
    confidence: int
    analysis: str
    key_factors: List[str]
