import os
import sys
import django
import json
import io

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.models import Topic

def populate():
    # 1. Read original full Kazakh text
    with open('extracted_full.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    headers = [
        "Жарық деген не және жарық көздері",
        "Жарықтың түзу сызықты таралуы",
        "Жарықтың шағылуы. Шағылу заңдары. Жазық айналар",
        "Сфералық айналар және сфералық айналар көмегімен кескін алу",
        "Жарықтың сынуы. Жарықтың сыну заңы. Жарықтың толық ішкі шағылуы",
        "Линзалар, линзаның оптикалық күші, жұқа линзаның формуласы, линзадағы кескін",
        "Интерференция",
        "Дифракция",
        "Дисперсия",
        "Поляризация"
    ]

    topics_content = []
    current_topic = None
    current_text = []

    for line in lines:
        stripped = line.strip()
        if stripped in headers:
            if current_topic:
                topics_content.append((current_topic, current_text))
            current_topic = stripped
            current_text = []
        else:
            if current_topic and stripped:
                current_text.append(stripped)
    
    if current_topic:
        topics_content.append((current_topic, current_text))

    # 2. Read detailed Russian text
    with open('translations_ru_detailed.json', 'r', encoding='utf-8') as f:
        ru_data = json.load(f)

    ru_titles = {
        "Жарық деген не және жарық көздері": "Что такое свет и источники света",
        "Жарықтың түзу сызықты таралуы": "Прямолинейное распространение света",
        "Жарықтың шағылуы. Шағылу заңдары. Жазық айналар": "Отражение света. Законы отражения. Плоские зеркала",
        "Сфералық айналар және сфералық айналар көмегімен кескін алу": "Сферические зеркала и построение изображений",
        "Жарықтың сынуы. Жарықтың сыну заңы. Жарықтың толық ішкі шағылуы": "Преломление света. Закон преломления",
        "Линзалар, линзаның оптикалық күші, жұқа линзаның формуласы, линзадағы кескін": "Линзы, оптическая сила и формула тонкой линзы",
        "Интерференция": "Интерференция",
        "Дифракция": "Дифракция",
        "Дисперсия": "Дисперсия",
        "Поляризация": "Поляризация"
    }

    db_topics = Topic.objects.all().order_by('order')
    
    for i, (kz_title, kz_content_lines) in enumerate(topics_content):
        if i < len(db_topics):
            topic = db_topics[i]
            
            # Smart formatting for Kazakh text
            formatted_kz = f"# {kz_title}\n\n"
            for line in kz_content_lines:
                # If it's a short sentence ending with colon, make it bold instead of a huge header
                if line.endswith(':'):
                    formatted_kz += f"**{line}**\n\n"
                # If it's very short and has no punctuation at the end, make it a smaller header
                elif len(line) < 50 and not line[-1] in ['.', '!', '?', ';', ',']:
                    formatted_kz += f"### {line}\n\n"
                # If it starts with a bullet point character, keep it as a list item
                elif line.startswith('- ') or line.startswith('* '):
                    formatted_kz += f"{line}\n"
                else:
                    formatted_kz += f"{line}\n\n"
            
            topic.title_kz = kz_title
            topic.title_ru = ru_titles.get(kz_title, kz_title)
            topic.content_kz = formatted_kz.strip()
            
            topic.content_ru = ru_data.get(str(i+1), {}).get("ru", "")
            
            topic.save()
            print(f"Restored FULL text for Topic {i+1}: {kz_title}")

if __name__ == "__main__":
    populate()
