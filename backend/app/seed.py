# backend/app/seed.py

from app.database import SessionLocal
from app import crud, schemas, models

print("Seeding database...")

# Get a database session
db = SessionLocal()

# --- Create a Test User ---
user_email = "test@example.com"
user_password = "password123"

# Check if the user already exists
db_user = crud.get_user_by_email(db, email=user_email)

if not db_user:
    user_in = schemas.UserCreate(email=user_email, password=user_password)
    db_user = crud.create_user(db, user=user_in)
    print(f"User '{db_user.email}' created successfully.")
else:
    print(f"User '{user_email}' already exists.")

# --- Create a Design Iteration for the user ---
iteration_in = schemas.DesignIterationCreate(
    prompt="A cozy brick cottage in a snowy forest, photorealistic",
    sketch_url="temp_uploads/initial_sketch.png"
)

# Use the user's ID to create the iteration
new_iteration = crud.create_iteration(db, iteration=iteration_in, user_id=db_user.id)
print(f"Design iteration '{new_iteration.prompt}' created for user '{db_user.email}'.")


# Close the database session
db.close()
print("Seeding finished.")