#!/usr/bin/env bash

set -euo pipefail

wf_log() {
  printf '[workflow] %s\n' "$*"
}

wf_set() {
  local key="$1"
  local value="$2"
  local kind="${3:-string}"

  python3 - "$WORKFLOW_OUTPUT_PATH" "$key" "$value" "$kind" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
key = sys.argv[2]
value = sys.argv[3]
kind = sys.argv[4]

if path.exists():
    data = json.loads(path.read_text(encoding='utf-8'))
else:
    data = {}

if kind == 'number':
    data[key] = float(value) if '.' in value else int(value)
elif kind == 'boolean':
    data[key] = value.lower() in {'1', 'true', 'yes', 'y'}
elif kind == 'json':
    data[key] = json.loads(value)
else:
    data[key] = value

path.write_text(json.dumps(data), encoding='utf-8')
PY
}

wf_get() {
  local key="$1"

  python3 - "$WORKFLOW_DATA_JSON" "$key" <<'PY'
import json
import sys

data = json.loads(sys.argv[1])
key = sys.argv[2]
value = data.get(key, '')
if isinstance(value, bool):
    print('true' if value else 'false')
elif value is None:
    print('')
else:
    print(value)
PY
}