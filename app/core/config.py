import logging
import os
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


def configure_logging():
    os.makedirs("./logs", exist_ok=True)
    # Create a TimedRotatingFileHandler
    handler = TimedRotatingFileHandler(
        "./logs/platform-integration-api.log",  # Log file path
        when="midnight",  # Rotate at midnight
        interval=1,  # Every 1 day
        backupCount=7,  # Keep last 7 days of logs
    )

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s  - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set the logging level globally
    root_logger.addHandler(handler)

    # Optional: Adding console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # detailed logs
    detailed_handler = TimedRotatingFileHandler(
        "./logs/detailed.platform-integration-api.log",  # Log file path
        when="midnight",  # Rotate at midnight
        interval=1,  # Every 1 day
        backupCount=7,  # Keep last 7 days of logs
    )
    detailed_handler.setFormatter(formatter)
    detailed_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(detailed_handler)


class Settings(BaseSettings):
    APP_TITLE: str = "Automation Platform Integration"
    VERSION: str = "1.0"
    RELEASE_ID: str = "0.1"
    API_V1_STR: str = "/api/v1"
    MONGODB_URI: str
    DATABSE_NAME: str = "agents-platform-integration"
    ALLOWED_ORIGINS: str = "*"
    QUEST_AI_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str
    AZURE_REDIRECT_URI: str
    AZURE_SCOPE: list[str] = [
        "https://management.azure.com/user_impersonation"
    ]


settings = Settings()
configure_logging()
