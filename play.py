#!/usr/bin/env python

import os
import re
import datetime as dt

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
    RE_EXCLUDE = re.compile(r"^\.|^EM|^em_")

    for file in os.listdir():
        if not re.match(RE_EXCLUDE, file):
            print(file)

generate_name()
get_targets()
