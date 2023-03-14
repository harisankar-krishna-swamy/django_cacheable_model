import factory
from factory.django import DjangoModelFactory
from polls.models import Choice, Question


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    question_text = factory.Faker('sentence')
    pub_date = factory.Faker('date_time')


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    choice_text = factory.Faker('sentence')
    votes = factory.Faker('random_element', elements=[0, 4, 7, 10])
