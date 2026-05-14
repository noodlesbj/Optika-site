import os
import sys
import django
import json

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic

def update_kz():
    with open('translations_kz_detailed.json', 'r', encoding='utf-8') as f:
        kz_data = json.load(f)

    for order_str, data in kz_data.items():
        try:
            topic = Topic.objects.get(order=int(order_str))
            topic.content_kz = data['kz']
            topic.save()
            print(f"Updated Topic {order_str}")
        except Exception as e:
            print(f"Error Topic {order_str}: {e}")

if __name__ == '__main__':
    update_kz()
