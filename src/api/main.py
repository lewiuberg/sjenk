"""The main application."""
import sys  # noqa: F401

import uvicorn
from fastapi import FastAPI
from properties import config, settings
from utils.logging.logging import LoggerConstructor

APP_NAME: str = settings.project.name
API_VERSION: str = settings.project.version
API_DESCRIPTION: str = settings.project.description
API_HOST: str = config.api.host
API_PORT: int = config.api.port

logger_instance = LoggerConstructor()
logger = logger_instance.get_logger()


# Create FastAPI app instance after logging configuration
app = FastAPI(
    title=APP_NAME,
    description=API_DESCRIPTION,
    version=API_VERSION,
    # docs_url="/",
    # redoc_url=None,
    # logger=logger,
)


@app.get("/")
async def read_root():
    logger.info("This is an info message.")
    logger.trace("This is a trace message.")
    logger.debug("This is a debug message.")
    logger.success("This is a success message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
        access_log=True,
        log_config=None,
        log_level=None
    )
