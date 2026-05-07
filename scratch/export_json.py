import os
import django
import sys
import json
from django.core import serializers

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic, Question, Choice

def export_data():
    data = serializers.serialize("json", list(Topic.objects.all()) + list(Question.objects.all()) + list(Choice.objects.all()), indent=2)
    
    os.makedirs('core/fixtures', exist_ok=True)
    with open('core/fixtures/initial_data.json', 'w', encoding='utf-8') as f:
        f.write(data)
    print("Data exported successfully to core/fixtures/initial_data.json")

if __name__ == "__main__":
    export_data()
