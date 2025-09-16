from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="简易用户认证API")

# 模拟用户数据库（实际项目中用真实数据库）
fake_users_db = {
    "zhangsan": {"username": "zhangsan", "password": "123456", "name": "张三"},
    "lisi": {"username": "lisi", "password": "abcdef", "name": "李四"}
}


# 定义数据格式
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user_info: Optional[dict] = None


# 用户登录端点
@app.post("/login", response_model=LoginResponse)
async def user_login(login_data: LoginRequest):
    """
    用户登录
    - username: 用户名
    - password: 密码
    """

    # 1. 检查用户是否存在
    if login_data.username not in fake_users_db:
        raise HTTPException(status_code=401, detail="用户不存在")

    user = fake_users_db[login_data.username]

    # 2. 检查密码是否正确
    if login_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="密码错误")

    # 3. 生成简单的token（实际项目要用JWT）
    simple_token = f"user_{login_data.username}_token"

    # 4. 返回成功响应
    return LoginResponse(
        success=True,
        message="登录成功",
        token=simple_token,
        user_info={
            "username": user["username"],
            "name": user["name"]
        }
    )


# 需要认证的端点
@app.get("/user-info")
async def get_user_info(token: str):
    """
    获取用户信息（需要token认证）
    """
    # 简单的token验证
    if not token.startswith("user_") or not token.endswith("_token"):
        raise HTTPException(status_code=401, detail="无效的token")

    # 从token中提取用户名
    username = token.replace("user_", "").replace("_token", "")

    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="用户不存在")

    user = fake_users_db[username]

    return {
        "username": user["username"],
        "name": user["name"],
        "message": "这是你的个人信息"
    }


# 首页
@app.get("/")
async def home():
    return {"message": "欢迎使用简易认证API", "登录端点": "/login"}


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)