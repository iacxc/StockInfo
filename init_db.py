#!/usr/bin/python3 -O

import sys

from model import Repository


if len(sys.argv) > 1 and sys.argv[1] == "clean":
    cleandb = True
else:
    cleandb = False

repository = Repository()
repository.init(cleandb)

print("Initialization completed")
