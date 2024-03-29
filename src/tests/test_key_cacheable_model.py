from ddt import data, ddt, unpack
from django.core.cache import cache
from django.test import TestCase

from tests.factories import ChoiceFactory, QuestionFactory


@ddt
class TestCacheableModelCacheKey(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.question = QuestionFactory()
        self.choice = ChoiceFactory(question=self.question)

    def test_question__cache_key_all(self):
        expected_key = 'Question.v1.all'
        self.assertEqual(expected_key, self.question.cache_key_all())

    def test_choice__cache_key_all(self):
        expected_key = 'Choice.v1.all'
        self.assertEqual(expected_key, self.choice.cache_key_all())

    choice_fields_and_expected_key = (
        (('id',), 'Choice.v1.id.1'),
        (('id', 'question'), 'Choice.v1.id.1.question.1'),
    )

    @data(*choice_fields_and_expected_key)
    @unpack
    def test_choice__ins_cache_key_by_fields(
        self, choice_fields=('id',), expected_key='Choice.v1.id.1'
    ):
        actual_key = self.choice.ins_cache_key_on_fields(fields=choice_fields)
        self.assertEqual(expected_key, actual_key)
