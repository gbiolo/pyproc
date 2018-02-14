#!/usr/bin/env python

# Import the new print function (can be removed with the python3 interpreter)
from __future__ import print_function

import sys

# Import the sheel-menu libraries
sys.path.append("../src/pyproc")
from pyproc import pyproc

# Print ps-like header
print("{:<10} {:<6} {:<6} {:<6} {:<20} {}".format("USER", "STATE", "PID", "PPID",
                                                  "BINARY", "CMDLINE"))

# Print all processes values
for proc in pyproc().get_procs():
    print("{:<10} {:<6} {:<6} {:<6} {:<20} {}".format(
          proc.uname, proc.state, proc.pid, proc.ppid,
          proc.comm, " ".join(proc.cmdline)))
