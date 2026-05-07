from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Topic, Question, Choice, QuizResult
from django.urls import reverse
from django.http import HttpResponseRedirect

def set_lang(request, lang):
    if lang in ['ru', 'kz']:
        request.session['lang'] = lang
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def get_lang(request):
    return request.session.get('lang', 'ru')

def home(request):
    topics = Topic.objects.all().order_by('order')
    topics_data = []
    
    for topic in topics:
        best_score = None
        if request.user.is_authenticated:
            results = QuizResult.objects.filter(user=request.user, topic=topic).order_by('-score')
            if results.exists():
                best_score = results.first()
                
        topics_data.append({
            'topic': topic,
            'best_score': best_score
        })
        
    return render(request, 'home.html', {'topics_data': topics_data})

def lecture(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'lecture.html', {'topic': topic})

@login_required
def quiz(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = Question.objects.filter(topic=topic)
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        
        # Save correct answers to session to show in result
        user_answers = {}
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                user_answers[str(q.id)] = choice_id
                if choice.is_correct:
                    score += 1
                    
        QuizResult.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total=total
        )
        
        request.session[f'recent_quiz_score_{topic.id}'] = score
        request.session[f'recent_quiz_total_{topic.id}'] = total
        request.session[f'recent_quiz_answers_{topic.id}'] = user_answers
        
        return redirect('result', topic_id=topic.id)

    return render(request, 'quiz.html', {'topic': topic, 'questions': questions})

@login_required
def result(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = Question.objects.filter(topic=topic)
    
    score = request.session.get(f'recent_quiz_score_{topic.id}', 0)
    total = request.session.get(f'recent_quiz_total_{topic.id}', 0)
    user_answers = request.session.get(f'recent_quiz_answers_{topic.id}', {})
    
    q_data = []
    for q in questions:
        correct_choice = Choice.objects.filter(question=q, is_correct=True).first()
        user_choice_id = user_answers.get(str(q.id))
        user_choice = Choice.objects.get(id=user_choice_id) if user_choice_id else None
        
        q_data.append({
            'question': q,
            'correct_choice': correct_choice,
            'user_choice': user_choice,
            'is_correct': user_choice and user_choice.is_correct
        })
        
    return render(request, 'result.html', {
        'topic': topic,
        'score': score,
        'total': total,
        'q_data': q_data
    })

@login_required
def profile(request):
    if request.user.is_staff:
        # Преподаватель видит всех студентов и их результаты
        all_results = QuizResult.objects.select_related('user', 'topic').order_by('-date_taken')
        students = User.objects.filter(is_staff=False).order_by('username')

        # Статистика по каждому студенту
        student_stats = []
        for student in students:
            student_results = all_results.filter(user=student)
            total_attempts = student_results.count()
            avg_score = 0
            if total_attempts > 0:
                avg_score = round(sum(r.score for r in student_results) / total_attempts, 1)
            student_stats.append({
                'user': student,
                'total_attempts': total_attempts,
                'avg_score': avg_score,
                'results': student_results[:5],  # последние 5 попыток
            })

        return render(request, 'profile_teacher.html', {
            'all_results': all_results,
            'student_stats': student_stats,
        })
    else:
        # Обычный студент видит только свои результаты
        results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
        return render(request, 'profile.html', {'results': results})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')

def about(request):
    scientists = [
        {'emoji': '🍎', 'name': 'Исаак Ньютон', 'years': '1643–1727', 'contribution_ru': 'Корпускулярная теория света, дисперсия', 'contribution_kz': 'Корпускулалық теория, дисперсия'},
        {'emoji': '🌊', 'name': 'Христиан Гюйгенс', 'years': '1629–1695', 'contribution_ru': 'Волновая теория света', 'contribution_kz': 'Жарықтың толқындық теориясы'},
        {'emoji': '⚡', 'name': 'Джеймс Максвелл', 'years': '1831–1879', 'contribution_ru': 'Электромагнитная природа света', 'contribution_kz': 'Жарықтың электромагниттік табиғаты'},
        {'emoji': '🔆', 'name': 'Альберт Эйнштейн', 'years': '1879–1955', 'contribution_ru': 'Фотоэффект, квантовая теория', 'contribution_kz': 'Фотоэффект, кванттық теория'},
        {'emoji': '🔬', 'name': 'Томас Юнг', 'years': '1773–1829', 'contribution_ru': 'Интерференция света, опыт Юнга', 'contribution_kz': 'Жарықтың интерференциясы'},
        {'emoji': '💡', 'name': 'Макс Планк', 'years': '1858–1947', 'contribution_ru': 'Квант действия, квантовая физика', 'contribution_kz': 'Кванттық физика негізі'},
    ]

    applications = [
        {'emoji': '👓', 'name_ru': 'Очки и линзы', 'name_kz': 'Көзілдіріктер'},
        {'emoji': '📷', 'name_ru': 'Фотоаппарат', 'name_kz': 'Фотоаппарат'},
        {'emoji': '🔭', 'name_ru': 'Телескоп', 'name_kz': 'Телескоп'},
        {'emoji': '🔬', 'name_ru': 'Микроскоп', 'name_kz': 'Микроскоп'},
        {'emoji': '💻', 'name_ru': 'LCD экраны', 'name_kz': 'LCD экрандар'},
        {'emoji': '🌐', 'name_ru': 'Оптоволокно', 'name_kz': 'Оптикалық талшық'},
        {'emoji': '🔴', 'name_ru': 'Лазеры', 'name_kz': 'Лазерлер'},
        {'emoji': '🏥', 'name_ru': 'Медицина', 'name_kz': 'Медицина'},
        {'emoji': '☀️', 'name_ru': 'Солнечные панели', 'name_kz': 'Күн батареялары'},
        {'emoji': '🌈', 'name_ru': 'Радуга', 'name_kz': 'Кемпірқосақ'},
    ]

    return render(request, 'about.html', {
        'scientists': scientists,
        'applications': applications,
    })
    
from django.shortcuts import redirect
from .models import QuizResult # Проверь название модели в models.py!

def clear_results(request):
    if request.method == 'POST' and request.user.is_staff:
        # Используем ПРАВИЛЬНОЕ название модели - QuizResult
        QuizResult.objects.all().delete()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
def comprehensive_quiz(request):
    # Select 20 random questions from all topics
    questions = list(Question.objects.all())
    import random
    if len(questions) > 20:
        selected_questions = random.sample(questions, 20)
    else:
        selected_questions = questions
    
    if request.method == 'POST':
        score = 0
        total = len(selected_questions)
        for q in selected_questions:
            selected_choice_id = request.POST.get(f'question_{q.id}')
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                if choice.is_correct:
                    score += 1
        
        # We don't save general quiz to results for now, or we can save it with topic=None if we modify model
        # For now, just show result
        return render(request, 'result.html', {
            'score': score,
            'total': total,
            'is_comprehensive': True
        })

    return render(request, 'quiz.html', {
        'questions': selected_questions,
        'topic': {'title_ru': 'Общий тест', 'title_kz': 'Жалпы тест'},
        'is_comprehensive': True
    })
