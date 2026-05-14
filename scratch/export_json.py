import os
import sys
import django
import json

# Set up Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic

def export_topics():
    topics = Topic.objects.all().order_by('order')
    data = []
    for topic in topics:
        data.append({
            "model": "core.topic",
            "pk": topic.pk,
            "fields": {
                "title_ru": topic.title_ru,
                "title_kz": topic.title_kz,
                "content_ru": topic.content_ru,
                "content_kz": topic.content_kz,
                "image": str(topic.image) if topic.image else "",
                "order": topic.order
            }
        })
    
    os.makedirs('core/fixtures', exist_ok=True)
    with open('core/fixtures/initial_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Exported {len(data)} topics to core/fixtures/initial_data.json")

if __name__ == "__main__":
    export_topics()
