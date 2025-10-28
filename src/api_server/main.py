from fastapi import FastAPI
from src.api_server.routers import laws

app = FastAPI(
    title="BHSN API",
    description="API for the Law Information Management System.",
    version="0.1.0"
)

# Include the laws router
app.include_router(laws.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BHSN API"}
