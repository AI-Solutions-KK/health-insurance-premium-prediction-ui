# api/main.py
from fastapi import FastAPI
from api.inference import predict_premium

app = FastAPI(title="Health Insurance Premium API")


@app.get("/")
def root():
    return {"status": "API running"}


@app.post("/predict")
def predict(data: dict):
    result = predict_premium(data)
    return {"predicted_premium": result}
