import uvicorn
from fastapi import FastAPI

from config.fastapi import FASTAPI_KWARGS


app = FastAPI(
    **FASTAPI_KWARGS
)


if __name__ == "__main__":
    # Аналогично `uvicorn main:app --reload`
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
