#!/usr/bin/env python

import sys
import os
import re
import datetime as dt
from pathlib import Path

# Doing the small stuff first
# Leave the high level for later

def generate_name():
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F") # ISO date
    week_day = NOW.strftime(".%V-%u") # Week 1..53, and Day 1..7 starting on Monday
    print("generate_name function")
    print(iso_date + week_day)
    return iso_date + week_day

def get_targets():
    print("get_targets function")
    RE_EXCLUDE = re.compile(r"archived|^\.|^EM|^em_")

    return [i for i in os.listdir() if not re.match(RE_EXCLUDE, i)]

def check_create(path):
    path = Path(path)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if path.is_file():
            sys.exit(f"Error: {path} is a file, doing NOTHING")

if __name__ == "__main__":

    BASE = "archived/"
    DAY = generate_name()

    check_create(BASE + DAY)

    TARGETS = get_targets()

    for target in TARGETS:
        ...
