from django.core.cache import cache
from django.test import TestCase
from polls.models import Choice, Question

from django_cacheable_model.utils import all_ins_from_cache, model_ins_from_cache
from tests.factories import ChoiceFactory, QuestionFactory


class TestUtilsSQLQueryCount(TestCase):
    def setUp(self) -> None:
        cache.clear()
        q1, q2 = QuestionFactory(), QuestionFactory()
        self.questions = (
            q1,
            q2,
        )
        c1, c2, c3 = (
            ChoiceFactory(question=q1),
            ChoiceFactory(question=q2),
            ChoiceFactory(question=q1),
        )
        self.choices = (c1, c2, c3)

    def test_utils_sql_query_count__all_ins_from_cache(self):
        # trigger retrieval and store to cache
        _ = all_ins_from_cache(Question)
        with self.assertNumQueries(0):
            _ = all_ins_from_cache(Question)
            # each individual instance should also have been store to cache on pk field
            _ = model_ins_from_cache(Question, fields={'id': 1})
            _ = model_ins_from_cache(Question, fields={'id': 1})

    def test_utils__sql_query_count__model_ins_from_cache(self):
        # trigger retrieval and store to cache
        _ = model_ins_from_cache(Choice, fields={'question': 1})
        with self.assertNumQueries(0):
            _ = model_ins_from_cache(Choice, fields={'question': 1})
