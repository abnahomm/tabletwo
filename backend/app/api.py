from fastapi import FastAPI

app = FastAPI(
    title="TableTwo API",
    description="backend api for tabletwo restaurant recommendations"
)


@app.get("/")
def home():
    return {
        "message": "tabletwo api is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }