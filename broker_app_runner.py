# broker_app_runner.py
import paho.mqtt.client as mqtt
import time
import logging
from concurrent.futures import ThreadPoolExecutor

from common_handlers import on_connect_factory, on_message_factory

logger = logging.getLogger(__name__)

def run_mqtt_client(broker_config, topic_to_subscribe, target_sensor_codes_set, mongo_collections):
    """
    Berilgan konfiguratsiya bilan MQTT klientini ishga tushiradi.
    mongo_collections: (mongo_client, historical_collection, last_data_collection) tuple
    """
    mongo_client, historical_collection, last_data_collection = mongo_collections

   
    if not target_sensor_codes_set: 
        logger.error(f"Broker {broker_config['host']} uchun maqsadli sensor kodlari topilmadi/yuklanmadi. Ishga tushmadi.")
        return
    
    if historical_collection is None or last_data_collection is None:
        logger.error(f"Broker {broker_config['host']} uchun MongoDB kolleksiyalari topilmadi/sozlanmadi. Ishga tushmadi.")
        return

    executor = ThreadPoolExecutor(max_workers=5)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=broker_config.get("client_id", f"client_{broker_config['host']}"))
    client.username_pw_set(broker_config["user"], broker_config["password"])

    client.on_connect = on_connect_factory(broker_config["host"], topic_to_subscribe)
    client.on_message = on_message_factory(target_sensor_codes_set, historical_collection, last_data_collection, executor)

    try:
        logger.info(f"{broker_config['host']}:{broker_config['port']} manziliga ulanishga harakat qilinmoqda...")
        client.connect(broker_config["host"], broker_config["port"], 60)
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info(f"Dastur ({broker_config['host']}) foydalanuvchi tomonidan to'xtatildi.")
    except Exception as e:
        logger.error(f"({broker_config['host']}) Ulanishda yoki asosiy tsiklda xatolik: {e}", exc_info=True)
    finally:
        logger.info(f"({broker_config['host']}) Executor yopilmoqda...")
        executor.shutdown(wait=True)
        if client.is_connected(): 
            client.disconnect()
            logger.info(f"({broker_config['host']}) Brokerdan uzildi.")