# django cacheable model
A cacheable model for django.

* A generic way of creating cache keys from Django model fields
* Retrieve django models from cache with field values (cache on the way if cache missed)
* Retrieve all the model instances (suitable for small set of models)

See usage example below

# 1. Github
https://github.com/harisankar-krishna-swamy/django_cacheable_model

# 2. Install
pip install django_cacheable_model

# 3. Configuration
* `CACHE_SET_MANY_LIMIT` is chunk size for calls to `cache.set_many`.  
   when `all_ins_from_cache` brings in all entries from cache, it will set each object  
   in chunks to control request size. Default is `5` i.e if there are 10 instances of a model  
   from db this config will set each of the models to the cache in two groups of `5`

# 4. Usage

See samples in  `example_django_project` views.py and models.py.

### 4.1. Create a model that inherits from CacheableModel
```python
class Question(CacheableModel):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(CacheableModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

### 4.2. Use cache operations from django_cacheable_model.utils

```python
from django_cacheable_model.utils import all_ins_from_cache, model_ins_from_cache

# Get all instances of model from cache (use for smaller set of models)
context['choices'] = all_ins_from_cache(Choice)

# Get all instances with select_related and order_by
choices = all_ins_from_cache(Choice,
                             select_related=('question',),
                             order_by_fields=('-id',))

# Get a single model. Note this method returns a list of matching objects
context['choice'] = model_ins_from_cache(Choice, {'id': 5})[-1]
```

# 5. To do
a) Example and document use of prefetch_related  
b) Doc and tests for util methods  
c) `timeout` in documentation

# 6. License
Apache2 License

# 7. Development

## 7.1 Python

Python 3.10.10 is used for development. Pyenv is used for managing Python versions.  
Install dev requirements in `dev-requirements.txt`
```bash
# in root folder
# Set python version for project folder using pyenv
pyenv local 3.10.10
# Create virtual environment 
python3 -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
# Install all packages
pip install -r dev-requirements.txt
pre-commit install
```
## 7.2 IDE (PyCharm) setup
Set Python interpreter to the virtual env created  
Set `.venv` folder as excluded in Pycharm  
Set `src` folder as source root  
For test runs from IDE set `src` as working directory
## 7.3 Test
1. Start memcached container for caching
```bash
cd src/tests/containers
# pull container and 
docker-compose pull
docker-compose up -d
# Check container is running
docker ps
```
2. Run tests
```bash
cd src
pytest
```
