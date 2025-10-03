# backend/app/main.py (Final Complete Version)

import shutil
import os
import json
from datetime import timedelta
from typing import List

from fastapi import FastAPI, File, UploadFile, Form, Depends, BackgroundTasks, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas, security
from .database import get_db
from .ai_service import run_ai_pipeline

os.makedirs("temp_uploads", exist_ok=True)

app = FastAPI(title="Architectural Design Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THIS IS THE REAL AI BACKGROUND TASK ---
def process_design_task(iteration_id: int, prompt: str, sketch_path: str, db: Session):
    print(f"Starting REAL AI task for iteration {iteration_id}")
    results = run_ai_pipeline(prompt, sketch_path)
    
    if results:
        try:
            parsed_text = json.loads(results["narrative_and_compliance"])
            narrative = parsed_text.get("narrative", "No narrative generated.")
            compliance = parsed_text.get("compliance_check", "No compliance check performed.")
        except (json.JSONDecodeError, TypeError):
            narrative = "Could not parse AI-generated narrative."
            compliance = "Could not parse AI-generated compliance check."

        update_data = schemas.DesignIterationUpdate(
            status="completed",
            generated_image_url=results["generated_image_url"],
            narrative=narrative,
            compliance_check=compliance
        )
        crud.update_iteration(db, iteration_id, update_data)
        print(f"Finished REAL AI task for iteration {iteration_id}")
    else:
        update_data = schemas.DesignIterationUpdate(status="failed")
        crud.update_iteration(db, iteration_id, update_data)
        print(f"FAILED REAL AI task for iteration {iteration_id}")

# --- AUTHENTICATION ENDPOINTS ---
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED ENDPOINTS ---
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(security.get_current_active_user)):
    return current_user

@app.post("/iterations", response_model=schemas.DesignIteration)
def create_iteration(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    sketch: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    sketch_path = f"temp_uploads/{sketch.filename}"
    with open(sketch_path, "wb") as buffer:
        shutil.copyfileobj(sketch.file, buffer)

    iteration_data = schemas.DesignIterationCreate(prompt=prompt, sketch_url=sketch_path)
    db_iteration = crud.create_iteration(db=db, iteration=iteration_data, user_id=current_user.id)
    
    background_tasks.add_task(process_design_task, db_iteration.id, prompt, sketch_path, db)
    return db_iteration

@app.get("/iterations", response_model=List[schemas.DesignIteration])
def read_iterations_for_user(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    iterations = crud.get_iterations_for_user(db, user_id=current_user.id)
    return iterations

@app.get("/iterations/{iteration_id}", response_model=schemas.DesignIteration)
def read_iteration(
    iteration_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    db_iteration = crud.get_iteration(db, iteration_id)
    if db_iteration is None or db_iteration.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Iteration not found")
    return db_iteration