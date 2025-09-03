from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"message": "Hello from TVS Mitra!"}

