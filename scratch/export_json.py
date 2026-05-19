import os
import sys
import django
import json

# Set up Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic

def export_all():
    from core.models import Topic, Question, Choice
    data = []
    
    # 1. Export Topics
    topics = Topic.objects.all().order_by('order')
    for topic in topics:
        data.append({
            "model": "core.topic",
            "pk": topic.pk,
            "fields": {
                "order": topic.order,
                "title_kz": topic.title_kz,
                "title_ru": topic.title_ru,
                "content_kz": topic.content_kz,
                "content_ru": topic.content_ru,
                "image": str(topic.image) if topic.image else ""
            }
        })
        
    # 2. Export Questions
    questions = Question.objects.all()
    for q in questions:
        data.append({
            "model": "core.question",
            "pk": q.pk,
            "fields": {
                "topic": q.topic_id,
                "text_kz": q.text_kz,
                "text_ru": q.text_ru
            }
        })
        
    # 3. Export Choices
    choices = Choice.objects.all()
    for c in choices:
        data.append({
            "model": "core.choice",
            "pk": c.pk,
            "fields": {
                "question": c.question_id,
                "text_kz": c.text_kz,
                "text_ru": c.text_ru,
                "is_correct": c.is_correct
            }
        })
        
    os.makedirs('core/fixtures', exist_ok=True)
    with open('core/fixtures/initial_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully exported {len(topics)} topics, {len(questions)} questions, and {len(choices)} choices to core/fixtures/initial_data.json")

if __name__ == "__main__":
    export_all()
