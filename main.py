import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.fastapi import FASTAPI_KWARGS, CORS_KWARGS
import routers


app = FastAPI(
    **FASTAPI_KWARGS
)

app.add_middleware(
    CORSMiddleware,
    **CORS_KWARGS
)

app.include_router(routers.common)
app.include_router(routers.reports)
app.include_router(routers.retail)
app.include_router(routers.config)
app.include_router(routers.upload)


if __name__ == "__main__":
    # Аналогично `uvicorn main:app --reload`
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
