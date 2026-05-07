from django.db import models
from django.contrib.auth.models import User

# Topic - учебная тема
class Topic(models.Model):
    order = models.IntegerField()
    title_kz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200)
    content_kz = models.TextField()
    content_ru = models.TextField()
    image = models.ImageField(upload_to='topic_images/', null=True, blank=True)

    def __str__(self):
        return self.title_ru

# Question - тестовый вопрос
class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text_kz = models.TextField()
    text_ru = models.TextField()

    def __str__(self):
        return self.text_ru

# Choice - вариант ответа
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_kz = models.TextField()
    text_ru = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text_ru

# QuizResult - результат пользователя
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic.title_ru} - {self.score}/{self.total}"
