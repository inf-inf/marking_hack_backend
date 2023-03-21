from fastapi import APIRouter

router_files = APIRouter(
    prefix='/files',
    tags=['files']
)
