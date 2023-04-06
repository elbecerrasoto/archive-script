#!/usr/bin/env python3
import argparse
import datetime as dt
import pickle
from pathlib import Path

ARCHIVED = Path("./archived/")


def gen_naming_scheme(prefix: str = "", suffix: str = "") -> str:
    NOW = dt.datetime.now()
    iso_date = NOW.strftime("%F")  # ISO date
    week_day = NOW.strftime(".%V-%u")  # Week 1..53, and Day 1..7 starting on Monday
    return prefix + iso_date + week_day + suffix


def unpickle_path(path):
    with open(path, "rb") as f:
        x = pickle.load(f)
    return x


def pickle_obj(x, path):
    with open(path, "wb") as f:
        pickle.dump(x, f)


def get_cliparser():
    parser = argparse.ArgumentParser()

    parser.description = f"""Get out of my way! I don't want to deal with you!
        Move files into {ARCHIVED}"""

    parser.add_argument("targets", nargs="*", help="Files to archive.", default=list())

    parser.add_argument(
        "--dry",
        "-d",
        action="store_true",
        help="Dry run.",
    )

    parser.add_argument("--unarchive", "-u", action="store_true", help="Undo action.")

    parser.add_argument(
        "--suffix", "-s", help="Suffix for the destination. DATE_SUFFIX", default=None
    )

    return parser
