import json
from dotenv import load_dotenv
import os

def load_json() -> dict:
    # Получаем путь к папке, где лежит текущий файл (with_config.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Собираем путь к конфигу (поднимись на уровень выше или укажи точное место)
    # Если config.json лежит в той же папке, что и этот скрипт:
    config_path = os.path.join(current_dir, "config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_evn() -> str:
    load_dotenv()
    return os.getenv("api_token")