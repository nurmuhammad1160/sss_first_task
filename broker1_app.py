# broker1_app.py
import settings 
import logging
from common_handlers import load_sensor_codes, get_mongo_collections
from broker_app_runner import run_mqtt_client 

logger = logging.getLogger(__name__) 

if __name__ == "__main__":
    logger.info("Broker 1 ilovasi ishga tushirilmoqda...")

    
    target_sensors = load_sensor_codes(settings.SENSORS_JSON_PATH)
    if target_sensors is None:
        logger.error("Sensor kodlari yuklanmadi, dastur to'xtatilmoqda.")
        exit()

    mongo_conn_tuple = get_mongo_collections(
        settings.MONGO_CONNECTION_STRING,
        settings.MONGO_DATABASE_NAME,
        settings.HISTORICAL_COLLECTION_NAME,
        settings.LAST_DATA_COLLECTION_NAME
    )
    mongo_client_instance = mongo_conn_tuple[0] 

    if not mongo_client_instance:
        logger.error("MongoDB ulanishi o'rnatilmadi, dastur to'xtatilmoqda.")
        exit()

    try:
        run_mqtt_client(
            broker_config=settings.BROKER1_CONFIG,
            topic_to_subscribe=settings.MQTT_TOPIC_SUBSCRIBE,
            target_sensor_codes_set=target_sensors,
            mongo_collections=mongo_conn_tuple
        )
    finally:
        if mongo_client_instance:
            mongo_client_instance.close()
            logger.info("Broker 1 ilovasi: MongoDB ulanishi yopildi.")
    logger.info("Broker 1 ilovasi o'z ishini yakunladi.")