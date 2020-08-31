http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/  
[nice example](https://github.com/postrational/rest_api_demo)

throw exception
```python
                # raise werkzeug.exceptions.NotFound('LawFirms not exists by id')
                lawfirm_namespace.abort(404, 'LawFirm not exists by provided id')
```

flask view, flask complex return view
```python
    'pgroups': fields.List(cls_or_instance=fields.String(required=True, description='id of groups'),
                           attribute=lambda x: x["pgroups"].split(",")),
    'practices': fields.List(cls_or_instance=fields.String(required=True, description='practices'),
                             attribute=lambda x: x["practices"].split(","))
```
