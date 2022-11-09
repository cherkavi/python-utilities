# logging

## log example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/logging/log-example.py) -->
<!-- The below code snippet is automatically added from ../../python/logging/log-example.py -->
```py
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',level=logging.INFO)
logging.info("standard logging")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


