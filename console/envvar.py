#!/usr/bin/env python

# print environment variables

import os
import sys

for key, value in os.environ.items():
    s = '%s=%s' % (key, value)
    print(s)
