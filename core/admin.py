from django.contrib import admin
from .models import Topic, Question, Choice, QuizResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text_ru', 'topic')
    list_filter = ('topic',)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('order', 'title_ru', 'title_kz')
    ordering = ('order',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(QuizResult)
