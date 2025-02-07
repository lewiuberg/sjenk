"""The main application."""

from datetime import UTC, datetime

from database import create_db_and_tables
from fastapi import FastAPI
from utils import get_logger, launch_settings, secrets

APP_NAME = str(launch_settings.project.name)

# TODO: Make the FastAPI logger use the custom logger.

logger = get_logger(slack_webhook=str(secrets.SLACK_WEBHOOK_URL))

start_time = datetime.now(UTC)

logger.debug(f"Creating {APP_NAME} database and tables...")
create_db_and_tables()

logger.debug(f"Starting {APP_NAME}...")

app = FastAPI(
    title=APP_NAME,
    description="A simple FastAPI demo application.",
    version="0.1",
    docs_url="/",
    redoc_url=None,
)
