###############
## usage
########
#    mapfile -t my_list < <(python3 rrules-parse-after-nmarkdown-header.py < $DIR_PROJECT/1.md | grep -v '#######' | awk -F 'task:' '{print $2}')
#    for each_value in "${my_list[@]}"; do
#        if [[ ! -f "$REGULAR_TASKS_COMPLETED" ]] || ! grep -Eq -- "^##+[[:space:]]*${each_value//\/\\}$" "$REGULAR_TASKS_COMPLETED"; then
#            echo "$each_value"
#        fi
#    done
########
#  ### clean up screenshots 
#  RRULE:FREQ=WEEKLY;BYDAY=FR
#  ```sh
#  ranger ~/screenshots
#  ```

from __future__ import annotations

import sys
import re
from datetime import datetime, timedelta
from dateutil.rrule import rrulestr, rruleset
from dateutil.parser import isoparse

heading_re = re.compile(r"^###\s+(.*)")
ical_re = re.compile(r"^(DTSTART|RRULE|RDATE|EXDATE):(.*)$")

local_tz = datetime.now().astimezone().tzinfo
now = datetime.now().astimezone()
today = now.date()
day_start = datetime(today.year, today.month, today.day, tzinfo=local_tz)
day_end = day_start + timedelta(days=1)

def parse_dt(value: str) -> datetime:
    # If no tz info, assume local time
    dt = isoparse(value.strip())
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=local_tz)
    return dt

def finalize_block(heading: str | None, block: dict[str, list[str]]):
    if not heading or not block:
        return
    rs = rruleset()

    dtstart = None
    if "DTSTART" in block:
        dtstart = parse_dt(block["DTSTART"][0])

    for rule_text in block.get("RRULE", []):
        try:
            rule = rrulestr("RRULE:" + rule_text, dtstart=dtstart or day_start)
            rs.rrule(rule)
        except Exception:
            pass

    for dates in block.get("RDATE", []):
        for item in dates.split(","):
            try:
                rs.rdate(parse_dt(item))
            except Exception:
                pass

    for dates in block.get("EXDATE", []):
        for item in dates.split(","):
            try:
                rs.exdate(parse_dt(item))
            except Exception:
                pass

    if rs.between(day_start, day_end, inc=True):
        print(f"#############")
        print(f"regular task: {heading}")


if __name__=='__main__':
    current_heading = None
    current_block: dict[str, list[str]] = {}

    for raw in sys.stdin.read().splitlines():
        m = heading_re.match(raw)
        if m:
            finalize_block(current_heading, current_block)
            current_heading = m.group(1).strip()
            current_block = {}
            continue

        im = ical_re.match(raw.strip())
        if im and current_heading:
            key, value = im.group(1), im.group(2)
            current_block.setdefault(key, []).append(value.strip())

    finalize_block(current_heading, current_block)