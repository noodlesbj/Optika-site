import os
import sys
import django
import io

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.models import Topic

def populate():
    with open('extracted_full.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Define headers and their indices (approximate or exact)
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
                topics_content.append((current_topic, "".join(current_text)))
            current_topic = stripped
            current_text = []
        else:
            if current_topic:
                # Basic markdown formatting: if line starts with 📌 or bullet, keep it
                # If it's a paragraph, add a newline
                if stripped:
                    current_text.append(line)
    
    if current_topic:
        topics_content.append((current_topic, "".join(current_text)))

    import json
    with open('translations_ru_detailed.json', 'r', encoding='utf-8') as f:
        ru_data = json.load(f)

    # Mapping to Russian titles
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

    # Let's map topic objects by order
    db_topics = Topic.objects.all().order_by('order')
    
    for i, (kz_title, kz_content) in enumerate(topics_content):
        if i < len(db_topics):
            topic = db_topics[i]
            
            # Format KZ content with markdown
            # Adding # for main title and ## for subheadings if found
            formatted_kz = f"# {kz_title}\n\n"
            
            # Simple heuristic for subheaders in the textbook text
            lines = kz_content.split('\n')
            for line in lines:
                stripped = line.strip()
                if not stripped: continue
                # If line is short and doesn't end with a dot, it might be a header
                if len(stripped) < 60 and not stripped.endswith('.') and not stripped.startswith('📌'):
                    formatted_kz += f"\n## {stripped}\n\n"
                else:
                    formatted_kz += f"{line}\n"
            
            topic.title_kz = kz_title
            topic.title_ru = ru_titles.get(kz_title, kz_title)
            topic.content_kz = formatted_kz.strip()
            
            # Get Russian content from JSON (which already has markdown)
            topic.content_ru = ru_data.get(str(i+1), {}).get("ru", "")
            
            print(f"Updating topic {i+1}: {kz_title}")
            topic.save()

if __name__ == "__main__":
    populate()
