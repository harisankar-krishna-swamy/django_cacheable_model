from polls.models import Choice, Question
from polls.serializers import ChoiceSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from django_cacheable_model.utils import (all_ins_from_cache,
                                          model_ins_from_cache)


class AllChoices(APIView):
    def get(self, request, format=None):
        choices = all_ins_from_cache(
            Choice, select_related=('question',), order_by_fields=('-pk',)
        )
        serializer = ChoiceSerializer(choices, context={'request': request}, many=True)
        return Response(serializer.data)


class AllQuestions(APIView):
    def get(self, request, format=None):
        questions = all_ins_from_cache(Question, order_by_fields=('-pk',))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionDetail(APIView):
    def get(self, request, id=None, format=None):
        question = model_ins_from_cache(Question, {'id': id})[0]
        serializer = QuestionSerializer(question, many=False)
        return Response(serializer.data)


class ChoicesOnQuestion(APIView):
    def get(self, request, id=None, format=None):
        choices = model_ins_from_cache(Choice, {'question': id})
        serializer = ChoiceSerializer(choices, context={'request': request}, many=True)
        return Response(serializer.data)
