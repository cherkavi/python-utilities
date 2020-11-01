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
