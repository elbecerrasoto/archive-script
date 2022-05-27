#!/usr/bin/env python3

import os
from pathlib import Path

ARCHIVED = Path("archived")

if not os.path.exists(ARCHIVED):
    os.makedirs(ARCHIVED)
else:
    if ARCHIVED.is_file():
        print(f"Error, {ARCHIVED} is a file")


# NOT caring for efficiency yet
# travelling the list multiple times
# but the code is stupidly easy

# Remove dot (hidden) files
include = [i for i in os.listdir() if not i.startswith(".")]
include = set(include) - {str(ARCHIVED)}

import shutil

# Fails if destination already exists.
for file in include:
    shutil.move(file, ARCHIVED)

print(os.listdir())
