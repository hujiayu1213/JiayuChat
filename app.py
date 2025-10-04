from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users_db = {}

class User(BaseModel):
    name: str
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# 添加根路径路由
@app.get("/")
def read_root():
    return {"message": "Welcome to the User API", "endpoints": {
        "create_user": "POST /users/{user_id}",
        "get_user": "GET /users/{user_id}",
        "login": "POST /login"
    }}

@app.get("/users/{user_id}")
def get_user(user_id: int, q: str | None = None):
    user = users_db.get(user_id)
    if user:
        user_info = user.copy()
        user_info.pop("password", None)
        return {"user_id": user_id, "user": user_info, "query": q}
    return {"error": "User not found", "user_id": user_id, "query": q}

@app.post("/users/{user_id}")
def create_user(user_id: int, user: User):
    users_db[user_id] = user.dict()
    user_info = user.dict().copy()
    user_info.pop("password", None)
    return {
        "user_id": user_id,
        **user_info
    }

@app.post("/login")
def login(login_req: LoginRequest):
    for user in users_db.values():
        if user["username"] == login_req.username and user["password"] == login_req.password:
            user_info = user.copy()
            user_info.pop("password", None)
            return {"message": "Login successful", "user": user_info}
    raise HTTPException(status_code=401, detail="Invalid username or password")