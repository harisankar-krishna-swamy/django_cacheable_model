from polls.models import Choice, Question
from polls.serializers import ChoiceSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from django_cacheable_model.utils import all_ins_from_cache


class Choices(APIView):
    def get(self, request, format=None):
        choices = all_ins_from_cache(
            Choice, select_related=('question',), order_by_fields=('-pk',)
        )
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)


class Questions(APIView):
    def get(self, request, format=None):
        questions = all_ins_from_cache(Question, order_by_fields=('-pk',))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
