#!/usr/bin/env bash
cat input.data | python mapper.py | sort | python reducer.py