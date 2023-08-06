# Django easy route

```
pip install djeasyroute
```

To use:

routes.py

```python
from djeasyroute import EasyRoute, route

class RouteClass(EasyRoute):

    @route('testing/<userid:int>/<name>', name="test_method")
    def testmethod(userid, name):
        print userid, name
```

urls.py

```python
from .routes import RouteClass
...
    url(r'^route/', include(RouteClass().urls)),
...
```
