from django.contrib import admin
from .models import QuestionModel, Categories, Answers, QuestionView, Like, Rate


admin.site.register(Like)
admin.site.register(Rate)
admin.site.register(Answers)
admin.site.register(Categories)
admin.site.register(QuestionView)
admin.site.register(QuestionModel)
