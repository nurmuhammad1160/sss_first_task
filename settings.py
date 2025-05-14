# settings.py
import os
from dotenv import load_dotenv
import logging

load_dotenv()

BROKER1_CONFIG = {
    "host": os.getenv("BROKER1_IP"),
    "port": int(os.getenv("BROKER1_PORT", 1883)),
    "user": os.getenv("BROKER1_USER"),
    "password": os.getenv("BROKER1_PASSWORD"),
    "client_id": "broker1_client" 
}

BROKER2_CONFIG = {
    "host": os.getenv("BROKER2_IP"),
    "port": int(os.getenv("BROKER2_PORT", 1883)),
    "user": os.getenv("BROKER2_USER"),
    "password": os.getenv("BROKER2_PASSWORD"),
    "client_id": "broker2_client" 
}

MQTT_TOPIC_SUBSCRIBE = os.getenv("MQTT_TOPIC_SUBSCRIBE")

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
HISTORICAL_COLLECTION_NAME = os.getenv("HISTORICAL_COLLECTION_NAME")
LAST_DATA_COLLECTION_NAME = os.getenv("LAST_DATA_COLLECTION_NAME")

SENSORS_JSON_PATH = os.getenv("SENSORS_JSON_PATH")
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL_STR, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if not all([BROKER1_CONFIG["host"], BROKER2_CONFIG["host"], MONGO_CONNECTION_STRING]):
    logger.error("DIQQAT: .env faylidan barcha kerakli sozlamalar o'qilmadi! .env faylini tekshiring.")