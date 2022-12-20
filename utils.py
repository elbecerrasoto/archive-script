#!/usr/bin/env python3

import datetime as dt


def gen_naming_scheme(prefix: str = "", suffix: str = "") -> str:
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F")  # ISO date
    week_day = NOW.strftime(".%V-%u")  # Week 1..53, and Day 1..7 starting on Monday
    return prefix + iso_date + week_day + suffix
