# routers/user.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def get_users():
    return [{"name": "Alice"}, {"name": "Bob"}]
