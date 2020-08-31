http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/  
[nice example](https://github.com/postrational/rest_api_demo)

throw exception
```python
                # raise werkzeug.exceptions.NotFound('LawFirms not exists by id')
                lawfirm_namespace.abort(404, 'LawFirm not exists by provided id')
```
