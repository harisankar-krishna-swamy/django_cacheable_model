from polls.models import Choice, Question
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date']


class ChoiceSerializer(serializers.ModelSerializer):
    question = HyperlinkedRelatedField(
        lookup_field='id', view_name='question', read_only=True
    )

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']
