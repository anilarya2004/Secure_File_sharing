from fastapi import APIRouter, HTTPException, Depends
from db.mongo import users_collection
from auth.models import UserCreate, UserLogin
from auth.utils import hash_password, verify_password, create_access_token
from bson import ObjectId
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    exists = await users_collection.find_one({"email": user.email})
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    new_user = {"email": user.email, "password": hashed, "role": user.role}
    await users_collection.insert_one(new_user)

    token = create_access_token({"email": user.email, "role": user.role})
    return {"message": "User created", "verify_url": f"http://localhost:8000/verify/{token}"}

@router.get("/verify/{token}")
async def verify_email(token: str):
    data = decode_token(token)
    await users_collection.update_one({"email": data["email"]}, {"$set": {"verified": True}})
    return {"message": "Email Verified"}

@router.post("/login")
async def login(user: UserLogin):
    found = await users_collection.find_one({"email": user.email})
    if not found or not verify_password(user.password, found['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"email": user.email, "role": found['role']})
    return {"access_token": token}
