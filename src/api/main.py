"""The main application."""

import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from database import create_db_and_tables, dispose
from fastapi import FastAPI
from properties import config, settings
from routers import users
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
    logger.info("Starting the application.")
    create_db_and_tables()
    yield
    # close the database engine on shutdown
    logger.info("Shutting down the application.")
    dispose()
    logger.info("Application shutdown complete.")


# Create FastAPI app instance after logging configuration
app = FastAPI(
    debug=config.api.debug,
    title=settings["project"][
        "name"
    ],  # Change to dictionary access due to ".name" being a reserved keyword
    description=settings.project.description,
    version=settings.project.version,
    openapi_url=config.openapi.url,
    openapi_tags=json.loads(config.openapi.tags),
    docs_url="/docs",
    redoc_url="/redoc",
    terms_of_service=settings.project.urls.TermsOfService,
    contact={
        "name": settings["project"]["authors"][0]["name"],
        "email": settings.project.authors[0].email,
    },
    license_info={
        "name": settings.project.license,
        "identifier": "MIT",
        "url": settings["project"]["license-files"][0],
    },
    swagger_ui_parameters={
        "docExpansion": "none",
        "syntaxHighlight": {
            "activated": True,
            "theme": "nord",
        },
        "unsafeMarkdown": False,
        "tryItOutEnabled": True,
        "app_name": settings.project.name,
        # "oauth2RedirectUrl": config.async_api.auth.oauth2_url,  # <-- Future?
    },
    operations_sorter="alpha",
    apis_sorter="alpha",
    lifespan=lifespan,
    # logger=logger,
)

# add routers to the FastAPI app
logger.info("Including users router.")
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(
        app=f"{__name__}:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        access_log=True,
        log_config=None,
        log_level=None,
    )
