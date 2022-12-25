# fastapi snippets
---
```python
app = FastAPI(title=app_settings.title)
app.include_router(sessions.router, prefix=f"/{app_settings.version}")
```
session.py
```python
from fastapi import APIRouter, Response, Depends, status as http_status_codes, Body

class RequestResponse(BaseModel):
    status: str = "OK"
class ErrorRespose(BaseModel):
    status: str = "ERROR"
    error: str

@router.get("/sessions")
def get_sessions(response: Response):
    try:
        return RequestResponse(content={"data": data})
    except Exception as e:
        response.status_code = http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorRespose(error=str(e))
```

---
```python
@router.put("/data")
def put_sessions(
    response: Response,
    my_data: TriggerBatch = Body(
        examples={
            "Example": {
                "summary": "Example",
                "description": "Here is an example"
                "of how to use.",
                "value": {
                    "jobs": ["vim1", "filemetadata"],
                    "ids": ["8072c","421", "4fa"],
                },
            }
        },
    ),
    credentials: HTTPBasicCredentials = Depends(security),
):
    """
    Description of method
    :param my_data: List of data
    :return: [dict]: stored data
    """
    try:
        # user_authenticator.verify_user_credentials(credentials)        
        return RequestResponse(content={"data": data})
    except Exception as e:
        response.status_code = http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorRespose(error=str(e))
```

---
```python
from prometheus_fastapi_instrumentator import Instrumentator
@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

```