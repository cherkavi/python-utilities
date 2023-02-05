xml yaml json toml formats

```python
import yaml
import json
import dicttoxml
import toml
import xml
```


```python
values=toml.load(path_to_file)
values=json.load(path_to_file)

yaml.safe_dump(values)
dicttoxml.dicttoxml(values)
json.safe_dumps(json.loads(json_dumps(json_string_value))
```
