# django cacheable model
A cacheable model for django.

* A generic way of creating cache keys from Django model fields
* Retrieve django models from cache with field values (cache along the way if not found)
* Retrieve all the model instances (suitable for small set of models)

See usage example below

# 1. Github
https://github.com/harisankar-krishna-swamy/django_cacheable_model

# 2. Install
pip install django_cacheable_model

# 3. Usage

See samples in  `example_django_project` views.py and models.py.

### 3.1. Create a model that inherits from CacheableModel
```python
class Question(CacheableModel):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(CacheableModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

### 3.2. Use cache operations from django_cacheable_model.utils
```python
from django_cacheable_model.utils import all_ins_from_cache, model_ins_from_cache_by_fields

# Get all instances of model from cache (use for smaller set of models)
context['choices'] = all_ins_from_cache(Choice)

# Get all instances with select_related and order_by
choices = all_ins_from_cache(Choice, 
                             select_related=('question',), 
                             order_by_fields=('-pk',))

# Get a single model
context['choice'] = model_ins_from_cache_by_fields(Choice, {'id': 5})[-1]
```

# 4. To do
a) Add more tests  
b) Document use of prefetch_related  
c) Remove Python2 styles


# 5. License
Apache2 License
