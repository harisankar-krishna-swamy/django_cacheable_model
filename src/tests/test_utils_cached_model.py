from ddt import data, ddt, unpack
from django.test import TestCase
from polls.models import Choice

from django_cacheable_model.utils import model_ins_from_cache
from tests.factories import ChoiceFactory, QuestionFactory


@ddt
class TestUtilsCachedModel(TestCase):
    def setUp(self) -> None:
        self.question = QuestionFactory()
        self.choice = ChoiceFactory(question=self.question)

    def assert_models_equality(self, model_cls, model_1, model_2):
        self.assertTrue(
            model_cls == model_1.__class__ == model_2.__class__,
            f'Model instance classes did not match expected {model_cls.__name__}',
        )
        fields_1 = model_1._meta.get_fields()
        fields_2 = model_1._meta.get_fields()
        self.assertEquals(
            len(fields_1), len(fields_2), 'Fields count did not match on cached model'
        )
        for f in fields_1:
            self.assertEquals(
                getattr(model_1, f.name),
                getattr(model_2, f.name),
                f'Value mismatch on field {f} between ' f'model and cached model',
            )

    choice_fields_values = (
        ({'id': 1},),
        ({'id': 1, 'question': 1},),
    )

    @data(*choice_fields_values)
    @unpack
    def test_choice__model_from_cache(self, fields={'id': 1}):
        # trigger retrieval and store to cache
        _ = model_ins_from_cache(Choice, fields)[0]
        cached = model_ins_from_cache(Choice, fields)[0]
        self.assert_models_equality(Choice, self.choice, cached)
