from itertools import chain

from django.db import models


class CacheableModel(models.Model):
    """
    When this model appears in another model as a Foreignkey or one-to-one
    this field will indicate the model in the cache key.

    For example: as cache key for Player totals may need to indicate
    the player for which the total is cached.
    Example key: PlayerTotals.10.Player.<related_cache_fieldname>
    """

    related_cache_fieldname = 'id'

    @classmethod
    def cache_key_all(cls):
        return 'model.{0}.all'.format(cls.__name__)

    @classmethod
    def fields_cache_key_template(cls, nfields=1):
        field_templates = ['model.{0}'.format(cls.__name__)]
        for i in range(0, nfields * 2, 2):
            field_templates.append('{{{0}}}.{{{1}}}'.format(i, i + 1))
        return '.'.join(field_templates)

    @classmethod
    def format_fields_cache_key_template(cls, fields):
        """
        Calling code has iterable of field, value pairs. It needs the cache key for the model
        based on those fields, values pairs.
        @param fields: a dict. key is usually model field's name. value is model field's value.
                    It can be anything that worked with objects.filter(**fields).
        """
        template = cls.fields_cache_key_template(len(fields))
        # To maintain cache key consistency. The key is made from sorted field names
        fields_values = sorted(
            [(field, value) for field, value in fields.items()],
            key=lambda entry: entry[0],
        )
        # For each pair, check if the value is again a model
        for index, (field, value) in enumerate(fields_values):
            if issubclass(value.__class__, models.Model):
                # use the model's related_cache_fieldname to avoid long cache keys
                fields_values[index] = (
                    field,
                    str(getattr(value, value.related_cache_fieldname)).replace(' ', ''),
                )
            else:
                # Value is a python object. Avoid long keys in str representation.
                fields_values[index] = (field, str(value).replace(' ', ''))
        return template.format(*tuple(chain.from_iterable(fields_values)))

    def ins_cache_key_by_fields(self, fields=('id',)):
        """
        Make a cache key using this instance's values for 'fields'. Defaults to just using 'id' field.
        @param fields: iterable list or tuple of field names.
        @return: cache key.
        """
        field_values = {field: getattr(self, field) for field in fields}
        return self.__class__.format_fields_cache_key_template(field_values)

    class Meta:
        abstract = True
