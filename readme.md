# FastAPI Project

A simple FastAPI application with PostgreSQL and SQLAlchemy ORM.

## 🚀 Features
- FastAPI framework for building APIs
- PostgreSQL database integration
- SQLAlchemy ORM for models and queries
- Environment variable support via `.env`
- Clean project structure with `app/` folder


## 🚀 How to Run the Server

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo


2. Create and activate a virtual environment
python -m venv venv


- On Linux/Mac:
source venv/bin/activate
- On Windows:
venv\Scripts\activate


3. Install dependencies
pip install -r requirements.txt


4. Set up the database
- Ensure PostgreSQL is running.
- Create a database (e.g., fastapi).
- If using Alembic migrations:
alembic upgrade head


5. Run the FastAPI server
uvicorn app.main:app --reload


- app.main:app → points to your FastAPI app instance inside main.py.
- --reload → restarts the server automatically when you change code.
6. Access the API
- Swagger docs: http://127.0.0.1:8000/docs (127.0.0.1 in Bing)
- ReDoc docs: http://127.0.0.1:8000/redoc (127.0.0.1 in Bing)

💡 Tip: Use the Swagger UI to test endpoints. Click Authorize, paste your JWT token, and you’ll be able to call protected routes like /posts/.
