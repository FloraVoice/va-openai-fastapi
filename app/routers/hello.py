from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])


@router.get("/")
def hello_world():
    return {"message": "Hello, World!"}
