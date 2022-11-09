# images

## image operations

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/images/image-operations.py) -->
<!-- The below code snippet is automatically added from ../../python/images/image-operations.py -->
```py
from PIL import Image

image = Image.open('1.jpg')
# image.show()
# image.save('1.png')
image.thumbnail((50,50))
image.rotate(90).save('2.jpg')
```
<!-- MARKDOWN-AUTO-DOCS:END -->


