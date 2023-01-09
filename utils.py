#!/usr/bin/env python3
import datetime as dt
import pickle


def gen_naming_scheme(prefix: str = "", suffix: str = "") -> str:
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F")  # ISO date
    week_day = NOW.strftime(".%V-%u")  # Week 1..53, and Day 1..7 starting on Monday
    return prefix + iso_date + week_day + suffix


def unpickle_path(path):
    with open(path, "rb") as f:
        x = pickle.load(path)
    return x


def pickle_obj(x, path):
    with open(path, "wb") as f:
        pickle.dump(x, f)
