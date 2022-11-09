```python
app=Flask("new_app")
app.db_configuration = create_db_configuration()
```

```python
from flask import current_app

def get_job_status(job_id: str) -> JobStatus:
    current_app.db_configuration
    ...
```
