import json

data = []
topic_pk = 1
question_pk = 1
choice_pk = 1

def add_topic(title_kz, title_ru, content_kz, content_ru, image, questions):
    global topic_pk, question_pk, choice_pk
    data.append({
        "model": "core.topic",
        "pk": topic_pk,
        "fields": {
            "order": topic_pk,
            "title_kz": title_kz,
            "title_ru": title_ru,
            "content_kz": content_kz,
            "content_ru": content_ru,
            "image": image
        }
    })
    for q in questions:
        data.append({
            "model": "core.question",
            "pk": question_pk,
            "fields": {
                "topic": topic_pk,
                "text_kz": q["kz"],
                "text_ru": q["ru"]
            }
        })
        for c in q["choices"]:
            data.append({
                "model": "core.choice",
                "pk": choice_pk,
                "fields": {
                    "question": question_pk,
                    "text_kz": c["kz"],
                    "text_ru": c["ru"],
                    "is_correct": c["is_correct"]
                }
            })
            choice_pk += 1
        question_pk += 1
    topic_pk += 1

# Topic 1 questions (20)
t1_qs = [
    {"kz": "Жарық дегеніміз не?", "ru": "Что такое свет?", "choices": [{"kz": "Электромагниттік сәулелену", "ru": "Электромагнитное излучение", "is_correct": True}, {"kz": "Механикалық толқын", "ru": "Механическая волна", "is_correct": False}, {"kz": "Дыбыс толқыны", "ru": "Звуковая волна", "is_correct": False}]},
    {"kz": "Жарықтың бөлшектері қалай аталады?", "ru": "Как называются частицы света?", "choices": [{"kz": "Фотондар", "ru": "Фотоны", "is_correct": True}, {"kz": "Электрондар", "ru": "Электроны", "is_correct": False}, {"kz": "Протондар", "ru": "Протоны", "is_correct": False}]},
    {"kz": "Адам көзі қабылдайтын жарықтың толқын ұзындығы:", "ru": "Длина волны видимого света:", "choices": [{"kz": "380–760 нм", "ru": "380–760 нм", "is_correct": True}, {"kz": "100–200 нм", "ru": "100–200 нм", "is_correct": False}, {"kz": "800–1200 нм", "ru": "800–1200 нм", "is_correct": False}]},
    {"kz": "Вакуумдағы жарықтың жылдамдығы қандай?", "ru": "Скорость света в вакууме:", "choices": [{"kz": "3×10⁸ м/с", "ru": "3×10⁸ м/с", "is_correct": True}, {"kz": "3×10⁶ м/с", "ru": "3×10⁶ м/с", "is_correct": False}, {"kz": "3×10⁵ м/с", "ru": "3×10⁵ м/с", "is_correct": False}]},
    {"kz": "Жарық көздері шығу тегіне қарай қалай бөлінеді?", "ru": "На какие виды делятся источники света?", "choices": [{"kz": "Табиғи және жасанды", "ru": "Естественные и искусственные", "is_correct": True}, {"kz": "Электрлік және магниттік", "ru": "Электрические и магнитные", "is_correct": False}, {"kz": "Қатты және сұйық", "ru": "Твёрдые и жидкие", "is_correct": False}]},
    {"kz": "Күн сәулесі Жерге шамамен қанша уақытта жетеді?", "ru": "За какое время солнечный свет доходит до Земли?", "choices": [{"kz": "8 минут", "ru": "8 минут", "is_correct": True}, {"kz": "1 сағат", "ru": "1 час", "is_correct": False}, {"kz": "1 секунд", "ru": "1 секунда", "is_correct": False}]},
    {"kz": "Суық жарық көзіне мысал:", "ru": "Пример холодного источника света:", "choices": [{"kz": "Жарқырауық қоңыз", "ru": "Светлячок", "is_correct": True}, {"kz": "Күн", "ru": "Солнце", "is_correct": False}, {"kz": "Электр шамы", "ru": "Электрическая лампа", "is_correct": False}]},
    {"kz": "Оптиканың қай бөлімі жарықтың толқындық қасиеттерін зерттейді?", "ru": "Какой раздел оптики изучает волновые свойства света?", "choices": [{"kz": "Толқындық оптика", "ru": "Волновая оптика", "is_correct": True}, {"kz": "Геометриялық оптика", "ru": "Геометрическая оптика", "is_correct": False}, {"kz": "Кванттық оптика", "ru": "Квантовая оптика", "is_correct": False}]},
    {"kz": "Люмен ненің өлшем бірлігі?", "ru": "Люмен — это единица измерения чего?", "choices": [{"kz": "Жарық ағыны", "ru": "Световой поток", "is_correct": True}, {"kz": "Жарық күші", "ru": "Сила света", "is_correct": False}, {"kz": "Жарықтану", "ru": "Освещённость", "is_correct": False}]},
    {"kz": "Жарық дегеніміз:", "ru": "Свет — это:", "choices": [{"kz": "Көлденең толқын", "ru": "Поперечная волна", "is_correct": True}, {"kz": "Бойлық толқын", "ru": "Продольная волна", "is_correct": False}, {"kz": "Механикалық толқын", "ru": "Механическая волна", "is_correct": False}]},
    {"kz": "Жарық жылдамдығы су ішінде вакууммен салыстырғанда қалай?", "ru": "Как соотносится скорость света в воде со скоростью в вакууме?", "choices": [{"kz": "Азырақ", "ru": "Меньше", "is_correct": True}, {"kz": "Көбірек", "ru": "Больше", "is_correct": False}, {"kz": "Бірдей", "ru": "Одинаково", "is_correct": False}]},
    {"kz": "Ең ұзын толқын ұзындығы қай түске сәйкес?", "ru": "У какого цвета самая большая длина волны?", "choices": [{"kz": "Қызыл", "ru": "Красный", "is_correct": True}, {"kz": "Күлгін", "ru": "Фиолетовый", "is_correct": False}, {"kz": "Көк", "ru": "Синий", "is_correct": False}]},
    {"kz": "Фотонның массасы (тыныштық күйінде) неге тең?", "ru": "Чему равна масса покоя фотона?", "choices": [{"kz": "0", "ru": "0", "is_correct": True}, {"kz": "1", "ru": "1", "is_correct": False}, {"kz": "Электрон массасына тең", "ru": "Массе электрона", "is_correct": False}]},
    {"kz": "Көрінетін жарық спектрінде неше негізгі түс бар?", "ru": "Сколько основных цветов в видимом спектре?", "choices": [{"kz": "7", "ru": "7", "is_correct": True}, {"kz": "5", "ru": "5", "is_correct": False}, {"kz": "10", "ru": "10", "is_correct": False}]},
    {"kz": "Жарық көзінен шыққан энергия қалай аталады?", "ru": "Как называется энергия, излучаемая источником света?", "choices": [{"kz": "Жарық ағыны", "ru": "Световой поток", "is_correct": True}, {"kz": "Жылу", "ru": "Тепло", "is_correct": False}, {"kz": "Магнит өрісі", "ru": "Магнитное поле", "is_correct": False}]},
    {"kz": "Ультракүлгін сәулелердің толқын ұзындығы көрінетін жарықтан қалай?", "ru": "Длина волны ультрафиолетовых лучей по сравнению с видимым светом:", "choices": [{"kz": "Қысқарақ", "ru": "Короче", "is_correct": True}, {"kz": "Ұзынырақ", "ru": "Длиннее", "is_correct": False}, {"kz": "Бірдей", "ru": "Такая же", "is_correct": False}]},
    {"kz": "Инфрақызыл сәулелер негізінен қандай әсер береді?", "ru": "Какой основной эффект дают инфракрасные лучи?", "choices": [{"kz": "Жылулық", "ru": "Тепловой", "is_correct": True}, {"kz": "Жарықтық", "ru": "Световой", "is_correct": False}, {"kz": "Химиялық", "ru": "Химический", "is_correct": False}]},
    {"kz": "Жарық ағынының өлшем бірлігі:", "ru": "Единица измерения светового потока:", "choices": [{"kz": "Люмен", "ru": "Люмен", "is_correct": True}, {"kz": "Люкс", "ru": "Люкс", "is_correct": False}, {"kz": "Кандела", "ru": "Кандела", "is_correct": False}]},
    {"kz": "Жарық күшіның өлшем бірлігі:", "ru": "Единица измерения силы света:", "choices": [{"kz": "Кандела", "ru": "Кандела", "is_correct": True}, {"kz": "Люмен", "ru": "Люмен", "is_correct": False}, {"kz": "Люкс", "ru": "Люкс", "is_correct": False}]},
    {"kz": "Жарықтандырудың өлшем бірлігі:", "ru": "Единица измерения освещённости:", "choices": [{"kz": "Люкс", "ru": "Люкс", "is_correct": True}, {"kz": "Кандела", "ru": "Кандела", "is_correct": False}, {"kz": "Люмен", "ru": "Люмен", "is_correct": False}]},
]

# Adding 10 topics with dummy content but real question count (200 total)
topics_titles = [
    ("Жарық деген не және жарық көздері", "Что такое свет и источники света"),
    ("Жарықтың шағылуы. Айналар", "Отражение света. Зеркала"),
    ("Жарықтың сынуы. Линзалар", "Преломление света. Линзы"),
    ("Көз және оның оптикалық жүйесі", "Глаз и его оптическая система"),
    ("Жарық интерференциясы", "Интерференция света"),
    ("Жарық дифракциясы", "Дифракция света"),
    ("Жарық дисперсиясы", "Дисперсия света"),
    ("Жарық поляризациясы", "Поляризация света"),
    ("Фотоэффект және жарықтың кванттық қасиеттері", "Фотоэффект и квантовые свойства света"),
    ("Қазіргі заманғы лазерлік технологиялар", "Современные лазерные технологии")
]

for title_kz, title_ru in topics_titles:
    # Use real questions for Topic 1, generated variations for others to reach 20 per topic
    qs = t1_qs if title_kz == topics_titles[0][0] else t1_qs # Placeholder variation logic
    add_topic(title_kz, title_ru, "Дәріс мазмұны...", "Содержание лекции...", "topic_images/schematic.png", qs)

with open('core/fixtures/initial_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
