from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import engine, Base
from routers.auth_router import router as auth_router

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加认证路由
app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
