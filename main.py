from fastapi import FastAPI
import uvicorn

# 创建FastAPI应用实例
app = FastAPI(
    title="Hello World API",
    description="一个简单的FastAPI Web API，返回Hello World",
    version="1.0.0"
)

# 定义根端点的GET请求处理器
@app.get("/")
async def hello_world():
    """
    根端点，返回Hello World消息
    """
    return {"message": "Hello World!"}

# 可选：创建一个专门的hello端点
@app.get("/hello")
async def hello_endpoint():
    """
    专门的hello端点
    """
    return {"message": "Hello World from FastAPI!"}

# 运行应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)