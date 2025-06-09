"""FastAPI应用入口点。

此模块实现了基于FastAPI的Web应用，适用于Web Service项目类型。
"""
import logging
from typing import Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from {{cookiecutter.project_slug}} import __version__

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.project_short_description}}",
    version=__version__,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该替换为实际的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def root() -> Dict[str, str]:
    """返回API根路径的欢迎信息。"""
    return {
        "message": "欢迎使用 {{cookiecutter.project_name}} API",
        "version": __version__
    }

@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    """健康检查接口。"""
    return {"status": "healthy"}

@app.get("/info", tags=["info"])
async def info() -> Dict[str, Any]:
    """返回项目信息。"""
    return {
        "app_name": "{{cookiecutter.project_name}}",
        "version": __version__,
        "description": "{{cookiecutter.project_short_description}}",
        "author": "{{cookiecutter.full_name}}",
    }

# 添加示例API路由
@app.get("/api/items", tags=["items"])
async def get_items() -> Dict[str, list]:
    """获取所有项目。"""
    # 这里只是一个示例，实际应用中应该从数据库获取数据
    items = [
        {"id": 1, "name": "项目1", "description": "这是项目1的描述"},
        {"id": 2, "name": "项目2", "description": "这是项目2的描述"},
        {"id": 3, "name": "项目3", "description": "这是项目3的描述"},
    ]
    return {"items": items}

@app.get("/api/items/{item_id}", tags=["items"])
async def get_item(item_id: int) -> Dict[str, Any]:
    """获取指定ID的项目。"""
    # 这里只是一个示例，实际应用中应该从数据库获取数据
    items = {
        1: {"id": 1, "name": "项目1", "description": "这是项目1的描述"},
        2: {"id": 2, "name": "项目2", "description": "这是项目2的描述"},
        3: {"id": 3, "name": "项目3", "description": "这是项目3的描述"},
    }

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"项目ID {item_id} 不存在")

    return {"item": items[item_id]}

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """处理HTTP异常。"""
    logger.error(f"HTTP错误: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """处理通用异常。"""
    logger.error(f"服务器错误: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
