"""The main application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from database import create_db_and_tables, dispose
from fastapi import FastAPI
from properties import config, settings
from routers import user
from utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any]:
    """
    Create a lifespan context manager for the FastAPI app.

    Entities before the yield statement are executed on startup.
    Entities after the yield statement are executed on shutdown.

    Parameters
    ----------
    app : FastAPI
        The FastAPI app instance.

    Returns
    -------
    AsyncGenerator[Any]
        An asynchronous generator.
    """
    # use create_db_and_tables() once on startup
    create_db_and_tables()
    yield
    # close the database engine on shutdown
    dispose()


# Create FastAPI app instance after logging configuration
app = FastAPI(
    debug=config.api.debug,
    title=settings["project"][
        "name"
    ],  # Change to dictionary access due to ".name" being a reserved keyword
    description=settings.project.description,
    version=settings.project.version,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    terms_of_service=settings.project.urls.TermsOfService,
    contact={
        "name": settings["project"]["authors"][0]["name"],
        "email": settings.project.authors[0].email,
    },
    license_info={
        "name": settings.project.license,
        "url": settings["project"]["license-files"][0],
    },
    swagger_ui_parameters={
        "docExpansion": "none",
        "syntaxHighlight.theme": "nord",
        "tryItOutEnabled": True,
        "app_name": settings.project.name,
        # "oauth2RedirectUrl": config.async_api.auth.oauth2_url,  # <-- Future?
    },
    # generate_unique_id_functions=[],
    lifespan=lifespan,
)

# add routers to the FastAPI app
app.include_router(user.router)


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
        reload=config.api.reload,
        access_log=True,
        log_config=None,
        log_level=None,
    )
