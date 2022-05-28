import os
import re
import datetime as dt

# Doing the small stuff first
# Leave the high level for later

def gen_archiving_name():
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F") # ISO date
    week_day = NOW.strftime(".%V-%u") # Week 1..53, and Day 1..7 starting on Monday
    return iso_date + week_day

def get_archive_target():

    RE_EXCLUDE = re.compile(r"^\.|^EM")

    for file in os.listdir():
        if not re.match(RE_EXCLUDE, file):
            print(file)

print(gen_archiving_name())
