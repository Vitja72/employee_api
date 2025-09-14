from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://api_user:secure_password_123@localhost:5432/employees_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS employees;"))
    conn.commit()  # commit the transaction
    print("Table dropped successfully!")