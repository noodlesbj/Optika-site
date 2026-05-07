import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_app.settings')
django.setup()

from core.models import Topic, Question, Choice

def update_quizzes():
    # Clear existing questions to avoid duplicates for the first topics
    # (In a real app, we'd be more careful, but here we want to replace placeholders)
    
    # Topic 1: Жарық деген не және жарық көздері
    t1 = Topic.objects.filter(order=1).first()
    if t1:
        Question.objects.filter(topic=t1).delete()
        
        q1 = Question.objects.create(topic=t1, text_kz="Жарық дегеніміз не?", text_ru="Что такое свет?")
        Choice.objects.create(question=q1, text_kz="Механикалық толқын", text_ru="Механическая волна", is_correct=False)
        Choice.objects.create(question=q1, text_kz="Электромагниттік сәулелену", text_ru="Электромагнитное излучение", is_correct=True)
        Choice.objects.create(question=q1, text_kz="Дыбыс толқыны", text_ru="Звуковая волна", is_correct=False)

        q2 = Question.objects.create(topic=t1, text_kz="Жарықтың бөлшектері қалай аталады?", text_ru="Как называются частицы света?")
        Choice.objects.create(question=q2, text_kz="Электрондар", text_ru="Электроны", is_correct=False)
        Choice.objects.create(question=q2, text_kz="Фотондар", text_ru="Фотоны", is_correct=True)
        Choice.objects.create(question=q2, text_kz="Протондар", text_ru="Протоны", is_correct=False)

        q3 = Question.objects.create(topic=t1, text_kz="Вакуумдағы жарықтың жылдамдығы қандай?", text_ru="Какова скорость света в вакууме?")
        Choice.objects.create(question=q3, text_kz="3x10^8 м/с", text_ru="3x10^8 м/с", is_correct=True)
        Choice.objects.create(question=q3, text_kz="3x10^5 м/с", text_ru="3x10^5 м/с", is_correct=False)
        Choice.objects.create(question=q3, text_kz="3x10^6 м/с", text_ru="3x10^6 м/с", is_correct=False)

    # Topic 2: Жарықтың шағылуы. Айналар
    t2 = Topic.objects.filter(order=2).first()
    if t2:
        Question.objects.filter(topic=t2).delete()
        
        q1 = Question.objects.create(topic=t2, text_kz="Түсу бұрышы шағылу бұрышына тең бе?", text_ru="Равен ли угол падения углу отражения?")
        Choice.objects.create(question=q1, text_kz="Иә, әрқашан", text_ru="Да, всегда", is_correct=True)
        Choice.objects.create(question=q1, text_kz="Жоқ, ешқашан", text_ru="Нет, никогда", is_correct=False)
        Choice.objects.create(question=q1, text_kz="Тек кейде", text_ru="Только иногда", is_correct=False)

        q2 = Question.objects.create(topic=t2, text_kz="Жазық айнадағы кескін қандай болады?", text_ru="Какое изображение получается в плоском зеркале?")
        Choice.objects.create(question=q2, text_kz="Нақты, төңкерілген", text_ru="Действительное, перевернутое", is_correct=False)
        Choice.objects.create(question=q2, text_kz="Жалған, тура, өлшемі бірдей", text_ru="Мнимое, прямое, равное по размеру", is_correct=True)
        Choice.objects.create(question=q2, text_kz="Кішірейтілген", text_ru="Уменьшенное", is_correct=False)

    print("Quizzes updated for main topics.")

if __name__ == "__main__":
    update_quizzes()
