from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth import create_access_token, decode_token, hash_password, verify_password
from app.database import Prediction, SessionLocal, User
from app.models.schemas import (
    AIPredictionResponse,
    PredictionRequest,
    PredictionResponse,
    RegisterRequest,
)
from app.services.ai_service import (
    SUPPORTED_SPORTS,
    compute_prediction,
    generate_ai_prediction,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/supported-sports")
def supported_sports():
    return {"supported_sports": list(SUPPORTED_SPORTS.keys())}


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=payload.username, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    return {"message": f"User {payload.username} created successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction_text, confidence = compute_prediction(payload.team_a, payload.team_b, payload.sport)
    result = Prediction(
        team_a=payload.team_a,
        team_b=payload.team_b,
        sport=payload.sport,
        prediction=prediction_text,
        confidence=confidence,
        user_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.post("/predict/ai", response_model=AIPredictionResponse)
def ai_predict(
    payload: PredictionRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        ai_result = generate_ai_prediction(payload.team_a, payload.team_b, payload.sport)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    if not isinstance(ai_result, dict):
        raise HTTPException(status_code=500, detail="Invalid AI response format")
    return AIPredictionResponse(
        team_a=payload.team_a,
        team_b=payload.team_b,
        sport=payload.sport,
        prediction=ai_result.get("prediction", "Unknown"),
        confidence=int(ai_result.get("confidence", 0)),
        analysis=ai_result.get("analysis", ""),
        key_factors=ai_result.get("key_factors", []),
    )


@router.get("/predictions", response_model=List[PredictionResponse])
def get_predictions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Prediction).all()
