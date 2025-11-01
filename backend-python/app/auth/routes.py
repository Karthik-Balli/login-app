from fastapi import APIRouter, Depends, HTTPException, Request, Response
from app.database import users_collection
from app.auth.utils import create_access_token, create_refresh_token, verify_password, hash_password
from app.models import User
from app.auth.schemas import LoginSchema
from bson import ObjectId
import jwt
from app.config import REFRESH_SECRET

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user.password = hash_password(user.password)
    await users_collection.insert_one(user.dict())
    return {"message": "User created successfully"}

@router.post("/login")
async def login(response: Response, payload: LoginSchema):
    try:
        user = await users_collection.find_one({"email": payload.email})
        print(">> Payload email:", payload.email)
        print(">> Fetched user:", user)
        if not user or not verify_password(payload.password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during login")

    access_token = create_access_token({"id": str(user["_id"])})
    refresh_token = create_refresh_token({"id": str(user["_id"])})

    response.set_cookie(key="refreshToken", value=refresh_token, httponly=True, samesite="none", secure=True)

    return {
        "user": {"_id": str(user["_id"]), "name": user["name"], "email": user["email"], "role": user["role"]},
        "accessToken": access_token
    }

@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refreshToken")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        decoded = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
        user_id = decoded["id"]
        new_access = create_access_token({"id": user_id})
        return {"accessToken": new_access}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refreshToken")
    return {"message": "Logged out successfully"}
