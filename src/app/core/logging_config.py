# src/app/core/logging_config.py

import logging
import logging.config
import os

# 🔹 Ensure logs directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 🔹 Define log file paths
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
DB_LOG_FILE = os.path.join(LOG_DIR, "db.log")
CHATBOT_LOG_FILE = os.path.join(LOG_DIR, "chatbot.log")
USER_LOG_FILE = os.path.join(LOG_DIR, "user.log")  #  user log file
PATIENT_LOG_FILE = os.path.join(LOG_DIR, "patient.log")  #  patient log file

# 🔹 Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        },
        "simple": {
            "format": "[%(levelname)s] %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        "file_app": {
            "class": "logging.FileHandler",
            "filename": APP_LOG_FILE,
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file_db": {
            "class": "logging.FileHandler",
            "filename": DB_LOG_FILE,
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file_chatbot": {
            "class": "logging.FileHandler",
            "filename": CHATBOT_LOG_FILE,
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file_user": {  #   user handler
            "class": "logging.FileHandler",
            "filename": USER_LOG_FILE,
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file_patient": {  #   patient handler
            "class": "logging.FileHandler",
            "filename": PATIENT_LOG_FILE,
            "formatter": "detailed",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "db": {
            "handlers": ["console", "file_db"],
            "level": "DEBUG",
            "propagate": False,
        },
        "chatbot": {
            "handlers": ["console", "file_chatbot"],
            "level": "DEBUG",
            "propagate": False,
        },
        "user": {  #   user logger
            "handlers": ["console", "file_user"],
            "level": "DEBUG",
            "propagate": False,
        },
        "patient": {  #   patient logger
            "handlers": ["console", "file_patient"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# 🔹 Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# 🔹 Create loggers
app_logger = logging.getLogger("app")
db_logger = logging.getLogger("db")
chatbot_logger = logging.getLogger("chatbot")
user_logger = logging.getLogger("user")  #  Separate user logger
patient_logger = logging.getLogger("patient")  #  Separate patient logger
