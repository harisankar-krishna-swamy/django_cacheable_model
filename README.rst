# django cacheable model
A cacheable model for django.

* A generic way of creating cache keys from Django model fields
* Retrieve django models from cache with field values (cache along the way if not found). See usage example below
* Retrieve all the model instances (suitable for small set of models)

# 1. Github
https://github.com/harisankar-krishna-swamy/django_cacheable_model

# 2. Install
pip install django_cacheable_model

# 3. Usage

### 3.1. Create a model that inherits from CacheableModel
```python
class Dota2Player(CacheableModel):
    # when this model appears in cache key of another model this is used
    related_cache_fieldname = 'steamid'

    name = models.CharField(unique= False, db_index=True, blank=False, max_length = 30, verbose_name= 'Player name')
    steamid = models.BigIntegerField(verbose_name = 'Steam id', unique = True, blank = False, db_index = True,
                                     validators = [MinValueValidator(1, 'Steamid for player must be greater than 0'),])

    def __str__(self):
        return '{0}(name={1},id={2})'.format(self.__class__.__name__, self.name, self.steamid).replace(' ', '_')
```

### 3.2. cache operations using django_cacheable_model.utils methods
```python
from django_cacheable_model.utils import all_ins_from_cache, model_ins_from_cache_by_fields

# Get all instances of model from cache (use for smaller set of models)
context['players'] = all_ins_from_cache(Dota2Player)

# Get a single model
context['player'] = model_ins_from_cache_by_fields(Dota2Player, {'steamid': steamid})[-1]
```

# 4. To do
a) Add a sample project
b) Migrate tests from AIM


# 5. License
Apache2 License

