#!/usr/bin/env python

# Import the new print function (can be removed with the python3 interpreter)
from __future__ import print_function

# Import the pyproc libraries
import sys
sys.path.append("../src/pyproc")
from pyproc import PyProc

# PyProc library object
pyproc = PyProc()

# Output format
output_format = "{:<10} {:<6} {:<6} {:<6} {:<20} {:<6} {}"
# Print ps-like header

print(output_format.format("USER", "STATE", "PID", "PPID", "BINARY", "VSIZE",
                           "CMDLINE"))

# Print all processes values
for proc in pyproc().select_user("giuseppe").search_cmdline("sh"):
    print(output_format.format(proc.uname, proc.state, proc.pid, proc.ppid,
                               proc.comm, proc.hvsize, " ".join(proc.cmdline)))
