"""The main application."""

import uvicorn
from fastapi import FastAPI
from properties import config, settings
from utils.logging import logger

# Create FastAPI app instance after logging configuration
app = FastAPI(
    title=settings.project.name,
    description=settings.project.description,
    version=settings.project.version,
    # docs_url="/",
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


@app.get("/produce_error")
async def produce_error():
    try:
        a = 1
        b = "2"
        a + b
    except TypeError as e:
        logger.exception(e)


@logger.catch
@app.get("/produce_zero_division_error")
async def produce_zero_division_error():
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.exception(e)


@app.get("/produce_custom_logs")
async def produce_custom_logs():
    customerLogger = logger.bind(customer_id="LEWI")
    customerLogger.info("This is a custom log message.")
    customerLogger.trace("This is a custom log message.")
    customerLogger.debug("This is a custom log message.")
    customerLogger.success("This is a custom log message.")
    customerLogger.warning("This is a custom log message.")
    customerLogger.error("This is a custom log message.")
    customerLogger.critical("This is a custom log message.")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.api.host,
        port=config.api.port,
        reload=False,
        access_log=True,
        log_config=None,
        log_level=None,
    )
