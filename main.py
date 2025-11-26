print("""
1111111111111111111111111111111111
1111111111111111111111111111111111
1111111111111111111111111111111111
""")
# car_owner_api/main.py
from fastapi import FastAPI, Request

# from .routers import owners, cars      ❌

from database import init_db

print("""
    3333333333333333333333333333333333333
    3333333333333333333333333333333333333
    3333333333333333333333333333333333333
    """)

# --- Initialize Database ---
init_db()

print("""
    666666666666666666666666666666666666666666666666666
    666666666666666666666666666666666666666666666666666
    666666666666666666666666666666666666666666666666666
    """)

app = FastAPI(title="Car Owner Management API (SQLModel)", version="2.0.0")

# Custom middleware
@app.middleware("http")
async def print_middleware(request: Request, call_next):
    """Logs every incoming HTTP request’s method and path for debugging purposes."""
    print(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# # --- Register Routers ---
# app.include_router(owners.router)
# app.include_router(cars.router)


@app.get("/", tags=["Root"])
def read_root():
    """Simple health check endpoint."""
    return {"message": "Welcome to the SQLModel API. Check /docs for endpoints."}


"""
To run the application, use:
uvicorn main:app --reload

http://127.0.0.1:8000/

http://127.0.0.1:8000/docs
"""