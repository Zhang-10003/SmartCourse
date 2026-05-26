from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from models import engine, Base
from routers.auth_router import router as auth_router
from routers.assignment_router import router as assignment_router
from routers.ai_router import router as ai_router
from routers.rag_router import router as rag_router
from routers.message_router import router as message_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(auth_router)
app.include_router(assignment_router)
app.include_router(ai_router)
app.include_router(rag_router)
app.include_router(message_router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 分享页面路由
@app.get("/share/{share_code}")
async def share_page(share_code: str):
    """作业分享页面，用于在浏览器中打开并尝试唤起 APP"""
    share_html_path = Path(__file__).parent / "static" / "share.html"
    if share_html_path.exists():
        return FileResponse(share_html_path, media_type="text/html")
    return {"message": "Share page not found"}