import os
import sys
import django
import json

# Set up Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic

def fix_titles():
    data = {
        1: {"kz": "Жарық деген не және жарық көздері", "ru": "Что такое свет и источники света"},
        2: {"kz": "Жарықтың түзу сызықты таралуы", "ru": "Прямолинейное распространение света"},
        3: {"kz": "Жарықтың шағылуы. Шағылу заңдары. Жазық айналар", "ru": "Отражение света. Законы отражения. Плоские зеркала"},
        4: {"kz": "Сфералық айналар және сфералық айналар көмегімен кескін алу", "ru": "Сферические зеркала и построение изображений"},
        5: {"kz": "Жарықтың сынуы. Жарықтың сыну заңы. Жарықтың толық ішкі шағылуы", "ru": "Преломление света. Закон преломления"},
        6: {"kz": "Линзалар, линзаның оптикалық күші, жұқа линзаның формуласы, линзадағы кескін", "ru": "Линзы, оптическая сила и формула тонкой линзы"},
        7: {"kz": "Интерференция", "ru": "Интерференция"},
        8: {"kz": "Дифракция", "ru": "Дифракция"},
        9: {"kz": "Дисперсия", "ru": "Дисперсия"},
        10: {"kz": "Поляризация", "ru": "Поляризация"}
    }

    for order, titles in data.items():
        Topic.objects.filter(order=order).update(
            title_ru=titles["ru"],
            title_kz=titles["kz"]
        )
        print(f"Updated titles for Topic {order}")

if __name__ == "__main__":
    fix_titles()
