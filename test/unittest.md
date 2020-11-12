```python
import unittest


def broken_function():
    raise Exception('not yet implemented')


class MyTestCase(unittest.TestCase):
    def test(self):
        with self.assertRaises(Exception) as context:
            broken_function()

        self.assertTrue('This is broken' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
```

fix environ
```python
import os
from unittest import TestCase, mock


@mock.patch.dict(os.environ, {"IMAGE_LOCAL_STORAGE": "test"})
class TestAmemberUtils(TestCase):
```

check exception, test exception
```python
self.assertRaises(ValueError, read_user_id, PHPSESSID)
```
