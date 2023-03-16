from typing import Iterable

from django.conf import settings
from django.core.cache import cache
from django.db import models

TIMEOUT = settings.CACHE_TIMEOUT


def chunked_list(long_list, chunk_size=20):
    """Break a long list into chunks"""
    for i in range(0, len(long_list), chunk_size):
        yield long_list[i : i + chunk_size]


def all_ins_from_cache(
    model_cls, order_by_fields=None, select_related=(None,), prefetch_objs=(None,)
) -> Iterable:
    """
    For Model class model_cls get 'all' instances from cache or get from DB and update cache.
    Depending on the size of the table, this may become unviable. So use on small tables.
    @param model_cls: Django model class
    @param order_by_fields: as it would work in Django queryset doc.
    @param select_related: tuple of fields to apply to queryset select_related
    @param prefetch_objs: tuple of Prefetch class objects. *WARNING* on size of prefetched rows. Bring in only needed
    columns using .only on Prefetch queryset. Ensure .only also has foreign keys.
    Example: PageWordCount.objects.all().only('id', 'created_at', 'web_page').order_by('-created_at')
    Ref: https://docs.djangoproject.com/en/1.10/ref/models/querysets/#prefetch-objects
    @return: list of all instances of model_cls currently in db
    """
    assert model_cls is not None
    assert issubclass(model_cls, models.Model)
    cache_set_many_limit = getattr(settings, 'CACHE_SET_MANY_LIMIT', 5)

    cache_key = model_cls.cache_key_all()
    instances = cache.get(cache_key)
    if instances is None:
        if not order_by_fields:
            order_by_fields = (model_cls._meta.pk.name,)
        instances = list(
            model_cls.objects.all()
            .select_related(*select_related)
            .prefetch_related(*prefetch_objs)
            .order_by(*order_by_fields)
        )
        each_ins_dict = {}
        if len(instances):
            # loop in chunked lists
            for chunk in chunked_list(instances, chunk_size=cache_set_many_limit):
                # For each model instance set the cache entries by pk
                each_ins_dict.update(
                    {
                        instance.ins_cache_key_on_fields(): (instance,)
                        for instance in chunk
                    }
                )
                cache.set_many(each_ins_dict)
                each_ins_dict.clear()
            # set the cache entry for all
            cache.set(cache_key, instances)
    return instances


def model_ins_from_cache(
    model_cls,
    fields: dict,
    latest_field_name: str = None,
    select_related: Iterable = (None,),
    prefetch_objs: Iterable = (None,),
) -> Iterable:
    """
    Try to get cached model instance with primary key pk. If not get from db and store in cache.
    @param model_cls: Django model class
    @param fields: dict key value pairs
    @param latest_field_name: model with most recent value of this field will be fetched.
    @param select_related: Tuple (iterable) of fields to apply to queryset select_related
    @param prefetch_objs: Tuple (iterable) of Prefetch class objects. *WARNING* on size of prefetched rows. Bring in only needed
    columns using .only on Prefetch queryset. Ensure .only also has foreign keys.
    Example: Choice.objects.all().only('id', 'created_at', 'question').order_by('-created_at')
    Ref: https://docs.djangoproject.com/en/1.10/ref/models/querysets/#prefetch-objects
    @return: Tuple of model instances that match or (None, ) if not found
    """
    assert model_cls is not None
    assert issubclass(model_cls, models.Model)
    assert len(fields) > 0

    cache_key = model_cls.ins_cache_key_with_field_values(fields)
    model_ins = cache.get(cache_key)
    if model_ins is None:
        try:
            # queryset
            model_ins = (
                model_cls.objects.filter(**fields)
                .select_related(*select_related)
                .prefetch_related(*prefetch_objs)
            )
            if latest_field_name:
                model_ins = (model_ins.latest(latest_field_name),)
            else:
                model_ins = tuple(model_ins)

            if model_ins:
                cache.set(cache_key, model_ins)
            else:
                model_ins = (None,)
        except Exception:
            return (None,)

    return model_ins


def get_cache_data(key):
    """
    Get data with key from cache
    :param key: cache key
    :return: the data else none
    """
    try:
        data = cache.get(key)
        return data
    except Exception:
        return None


def set_cache_key(key, data, timeout=TIMEOUT):
    """
    Set data to cache with key
    :param key: cache key
    :param data: cacheable data
    :return: True if everything went ok else False
    """
    try:
        cache.set(key, data, timeout=timeout)
        return True
    except Exception:
        return False


def invalidate_cache_on_model_updates(obj, fields):
    """
    1. Invalidate model instance's cache key on each field in fields
    2. Invalidate model instance's all entries cache key
    :param instance: a CacheableModel class
    :return: True on success. False on failure
    """
    try:
        cache_key_on_fields = obj.ins_cache_key_with_field_values(fields)
        cache_key_all = obj.cache_key_all()
        cache.delete(cache_key_on_fields)
        cache.delete(cache_key_all)
        return True
    except Exception:
        return False
