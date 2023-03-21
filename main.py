import uvicorn
from fastapi import FastAPI

from config.fastapi import FASTAPI_KWARGS
import routers


app = FastAPI(
    **FASTAPI_KWARGS
)

app.include_router(routers.common)
app.include_router(routers.files)


if __name__ == "__main__":
    # Аналогично `uvicorn main:app --reload`
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
