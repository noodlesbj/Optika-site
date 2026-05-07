from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topic/<int:topic_id>/lecture/', views.lecture, name='lecture'),
    path('topic/<int:topic_id>/quiz/', views.quiz, name='quiz'),
    path('topic/<int:topic_id>/result/', views.result, name='result'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('comprehensive-quiz/', views.comprehensive_quiz, name='comprehensive_quiz'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set-lang/<str:lang>/', views.set_lang, name='set_lang'),
    path('about/', views.about, name='about'),
    path('clear-results/', views.clear_results, name='clear_results'),
]
