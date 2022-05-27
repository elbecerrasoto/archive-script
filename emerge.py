#!/usr/bin/env python3

import os
from pathlib import Path

ARCHIVED=Path("archived")

if not os.path.exists(ARCHIVED):
    os.makedirs(ARCHIVED)
else:
    if ARCHIVED.is_file():
        print(f"Error, {ARCHIVED} is a file")

include = []
for file in os.listdir():
    print(f"{file}")
