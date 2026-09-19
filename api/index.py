from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MediPredict API", "status": "minimal"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

asgi_app = app