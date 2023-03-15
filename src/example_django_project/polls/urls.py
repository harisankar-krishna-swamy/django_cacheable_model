from django.urls import path

from .views import AllChoices, AllQuestions, ChoicesOnQuestion, QuestionDetail

urlpatterns = [
    path('choices/', AllChoices.as_view(), name='choices'),
    path('questions/', AllQuestions.as_view(), name='questions'),
    path('questions/<int:id>/', QuestionDetail.as_view(), name='question'),
    path(
        'questions/<int:id>/choices/',
        ChoicesOnQuestion.as_view(),
        name='choices-on-question',
    ),
]
