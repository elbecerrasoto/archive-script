#!/usr/bin/env python3
import os
import shutil
import sys
from collections import deque, namedtuple
from pathlib import Path

from utils import gen_naming_scheme, get_cliparser, pickle_obj, unpickle_path

ARCHIVED_NAME = "0-archived"

DAY = Path(gen_naming_scheme())
ARCHIVED = Path(f"./{ARCHIVED_NAME}/").resolve()
HISTORY_FILE = Path(f"./{ARCHIVED_NAME}/.archive_history.pickle").resolve()

Target = namedtuple("Target", ["Poriginal", "Parchived"])



if __name__ == "__main__":

    PARSER = get_cliparser()

    args = PARSER.parse_args()

    DRY = args.dry
    TARGETS = set(args.targets) - {'.', str(ARCHIVED), ''}
    UNARCHIVE = args.unarchive


    def args_help():
        # print usage to stdout
        PARSER.print_help(file=None)
        sys.exit()

    if not TARGETS and not UNARCHIVE:
        args_help()

    if UNARCHIVE and not HISTORY_FILE.exists():
        print("No history to undo.")
        args_help()

    SUFFIX = args.suffix
    destination = ARCHIVED / DAY if SUFFIX is None else ARCHIVED / (str(DAY) + '_' + SUFFIX)

    try:
        if DRY and not destination.exists():
            print(f"{destination} would've been created.")
        else:
            destination.mkdir(parents=True)
    except FileExistsError:
        if destination.is_file():
            # if sys.exit print a string sends error code 256 ?!
            print("Error: there is a file blocking the archiving.")
            sys.exit()


    try:
        history = unpickle_path(HISTORY_FILE)
    except FileNotFoundError:
        history = deque()

    # Main loop
    if UNARCHIVE:
        # Pop history
        to_undo = history.pop()
        for target in to_undo:
            try:
                shutil.move(str(target.Parchived),str(target.Poriginal.parent))
            except FileNotFoundError:
                print(f"File Not Found: {str(target.Parchived)}")

        # then check for an empty dir and delete it
        path2archived = target.Parchived.parent
        if path2archived.exists() and os.listdir(path2archived) == []:
            os.rmdir(path2archived)

        pickle_obj(history,HISTORY_FILE)
    else:
        # to be popoulated of Target named tuples
        single_run = list()
        for target in TARGETS:

            target = Path(target)

            if DRY:
                print(f"{target} --> {destination})")
            else:
                try:
                    shutil.move(str(target), str(destination))
                    single_run.append(Target(Poriginal=target, Parchived= destination / target.name ))
                except shutil.Error as e:
                    print("Blocking files/dirs were found", e)
                    sys.exit()

        if not DRY:
            # Push (append) to history stack, grows on the right.
            history.append(tuple(single_run))
            pickle_obj(history, HISTORY_FILE)
