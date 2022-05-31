#!/usr/bin/env python

import datetime as dt
import os
import re
import shutil
import sys
from pathlib import Path

# Doing the small stuff first
# Leave the high level for later


def generate_name(suffix: str = ""):
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F")  # ISO date
    week_day = NOW.strftime(".%V-%u")  # Week 1..53, and Day 1..7 starting on Monday
    return iso_date + week_day + suffix


def get_targets():
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

    DESTINATION = BASE + DAY

    check_create(DESTINATION)

    TARGETS = get_targets()

    for target in TARGETS:
        shutil.move(target, DESTINATION)
