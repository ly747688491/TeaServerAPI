import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from config.setting import setting
from setup import (
    logger_init,
    setup_cors,
    setup_database,
    setup_exception,
    setup_mount,
    setup_redis,
    setup_router,
)
from setup.setup_logger import logger


async def create_app(application):
    logger_init()
    setup_mount(application)
    setup_exception(application)
    setup_router(application)
    await setup_database(application)
    await setup_redis(application)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info(f"{setting.TITLE}开始启动")
    await create_app(application)
    logger.info(f"{setting.TITLE}启动成功")
    yield
    logger.info(f"{setting.TITLE}结束运行")


app = FastAPI(
    title=setting.TITLE,
    description=setting.DESCRIPTION,
    version=setting.VERSION,
    lifespan=lifespan,
    root_path=setting.API_PREFIX,
    docs_url=setting.DOCS_URL,
    openapi_url=setting.OPENAPI_URL,
    redoc_url=setting.REDOC_URL,
)

setup_cors(app)
# setup_middleware(app)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=setting.UVICORN_HOST,
        port=setting.UVICORN_PORT,
        reload=setting.UVICORN_RELOAD,
    )
