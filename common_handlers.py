# common_handlers.py
import json
import pymongo
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)



def load_sensor_codes(json_file_path):
    sensor_codes = set() 
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            sensors_data = json.load(f)
            for sensor in sensors_data:
                if 'code' in sensor:
                    sensor_codes.add(str(sensor['code'])) 
            logger.info(f"Jami {len(sensor_codes)} ta maqsadli sensor kodi '{json_file_path}' dan yuklandi.")
    except FileNotFoundError:
        logger.error(f"Xatolik: '{json_file_path}' fayli topilmadi.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Xatolik: '{json_file_path}' faylini o'qishda JSON formati xatosi.")
        return None
    return sensor_codes

def get_mongo_collections(connection_string, db_name, hist_coll_name, last_coll_name):
    try:
        mongo_client = pymongo.MongoClient(connection_string)
        mongo_client.admin.command('ping') 
        db = mongo_client[db_name]
        historical_collection = db[hist_coll_name]
        last_data_collection = db[last_coll_name]
        logger.info(f"MongoDB ga muvaffaqiyatli ulanildi: {connection_string}")
        logger.info(f"Ma'lumotlar bazasi: '{db_name}', Kolleksiyalar: '{hist_coll_name}', '{last_coll_name}'")
        return mongo_client, historical_collection, last_data_collection
    except pymongo.errors.ConnectionFailure as e:
        logger.error(f"MongoDB ga ulanishda xatolik: {e}")
    except Exception as e_mongo:
        logger.error(f"MongoDB ni sozlashda boshqa xatolik: {e_mongo}")
    return None, None, None

def save_to_mongodb_logic(topic, sensor_code, payload_json, historical_collection, last_data_collection):
    if not historical_collection or not last_data_collection:
        logger.warning("MongoDB kolleksiyalari mavjud emas, ma'lumot saqlanmadi.")
        return

    try:
        message_type = topic.split('/')[-1]

        historical_doc = {
            "sensor_code": sensor_code,
            "topic": topic,
            "message_type": message_type,
            "payload": payload_json,
            "received_at": datetime.now()
        }
        historical_collection.insert_one(historical_doc)

        last_data_filter = {"sensor_code": sensor_code}
        update_fields = {
            f"last_{message_type}_payload": payload_json,
            f"last_{message_type}_topic": topic,
            f"last_{message_type}_received_at": datetime.now()
        }
        last_data_collection.update_one(
            last_data_filter,
            {"$set": update_fields, "$setOnInsert": {"sensor_code": sensor_code, "first_seen_at": datetime.now()}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"MongoDB ga yozishda xatolik ({sensor_code}): {e}", exc_info=False) # exc_info=True ko'proq ma'lumot beradi

def on_connect_factory(broker_host, topic_to_subscribe):
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info(f"Brokerga muvaffaqiyatli ulanildi: {broker_host}")
            logger.info(f"'{topic_to_subscribe}' mavzusiga obuna bo'linmoqda...")
            client.subscribe(topic_to_subscribe)
        else:
            logger.error(f"Brokerga ({broker_host}) ulanishda xatolik, kod: {rc}")
    return on_connect

def on_message_factory(target_sensor_codes_set, historical_collection, last_data_collection, executor):
    def on_message(client, userdata, msg):
        try:
            payload_str = msg.payload.decode('utf-8')
            payload_json = json.loads(payload_str)

            if isinstance(payload_json, dict) and "i" in payload_json:
                sensor_code_from_payload = str(payload_json["i"])

                if sensor_code_from_payload in target_sensor_codes_set:
                    logger.info(f"MAQSADLI SENSOR XABARI! Sensor: {sensor_code_from_payload}, Mavzu: {msg.topic}")
                    executor.submit(save_to_mongodb_logic, msg.topic, sensor_code_from_payload, payload_json, historical_collection, last_data_collection)
        except json.JSONDecodeError:
            logger.warning(f"JSON o'qish xatosi: {msg.payload.decode('utf-8', errors='ignore')[:100]} mavzuda: {msg.topic}")
        except UnicodeDecodeError:
            logger.warning(f"UTF-8 o'qish xatosi: {msg.payload[:30]} mavzuda: {msg.topic}")
        except Exception as e:
            logger.error(f"Xabar bilan ishlashda noma'lum xatolik: {e} mavzuda: {msg.topic}", exc_info=False)
    return on_message