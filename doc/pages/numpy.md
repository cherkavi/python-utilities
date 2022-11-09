# numpy

## numpy example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/numpy/numpy-example.py) -->
<!-- The below code snippet is automatically added from ../../python/numpy/numpy-example.py -->
```py
import numpy as np

ar_strings = np.array(["one", "two", "three", "four", "five", "six", "seven"])
ar_numbers = np.array([1,2,3,4,5])
ar_numbers2 = np.array([
    [11,12,13,14,15],
    [21,22,23,24,25],
    [31,32,33,34,35]
])
print(type(ar_strings))

print("type of elements ")
print(ar_strings.dtype)
print(ar_numbers.dtype)

ar_numbers.size
ar_numbers.ndim
ar_numbers.shape
ar_numbers[0:2]=7,8
print(ar_numbers*2)
print(ar_numbers + ar_numbers)
print(ar_numbers * ar_numbers)

print("pi")
print(np.pi)
print("sin pi")
print(np.sin(np.pi))

print("digits in range")
print(np.linspace(-10,10,21))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


