from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import SessionLocal, Prediction, User, Base
from app.auth import hash_password, verify_password, create_access_token, decode_token


app = FastAPI()

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

@app.get("/")
def home():
    return {"message": "Sports AI Prediction API is running"}

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password must be 72 characters or less")
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": f"User {username} created successfully"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/predict")
def predict(team_a: str, team_b: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = Prediction(
        team_a=team_a,
        team_b=team_b,
        prediction=f"{team_a} Win",
        confidence="72%"
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Prediction).all()


