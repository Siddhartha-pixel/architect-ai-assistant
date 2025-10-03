# backend/app/crud.py (Corrected Version)

from sqlalchemy.orm import Session
from . import models, schemas, security # <-- Added 'security' to this line

# --- User CRUD Functions ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- DesignIteration CRUD Functions ---
def get_iteration(db: Session, iteration_id: int):
    return db.query(models.DesignIteration).filter(models.DesignIteration.id == iteration_id).first()

def get_iterations_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.DesignIteration).filter(models.DesignIteration.owner_id == user_id).offset(skip).limit(limit).all()

def create_iteration(db: Session, iteration: schemas.DesignIterationCreate, user_id: int):
    db_iteration = models.DesignIteration(
        prompt=iteration.prompt,
        sketch_url=iteration.sketch_url,
        owner_id=user_id
    )
    db.add(db_iteration)
    db.commit()
    db.refresh(db_iteration)
    return db_iteration

def update_iteration(db: Session, iteration_id: int, iteration_data: schemas.DesignIterationUpdate):
    db_iteration = get_iteration(db, iteration_id)
    if db_iteration:
        db_iteration.status = iteration_data.status
        db_iteration.generated_image_url = iteration_data.generated_image_url
        db_iteration.narrative = iteration_data.narrative
        db_iteration.compliance_check = iteration_data.compliance_check
        db.commit()
        db.refresh(db_iteration)
    return db_iteration