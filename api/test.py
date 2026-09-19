from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test API working", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

asgi_app = app