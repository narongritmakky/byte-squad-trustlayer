from fastapi import FastAPI

app = FastAPI(title="TrustLayer API")


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
