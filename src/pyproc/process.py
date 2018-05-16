
"""pyproc is a library to easily read Linux running processes info.

Description:
    The main target of the project is to provide an easily way to access to
    Linux running processes info.

Author:
    Giuseppe Biolo <giuseppe.biolo@gmail.com> <https://github.com/gbiolo>

License:
    This file is part of pyproc.

    pyproc is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyproc is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyproc. If not, see <http://www.gnu.org/licenses/>.
"""


# Compatibility with Python 2.6+
from __future__ import with_statement

import re
import os
from decimal import Decimal


class Process:
    """Object that rappresent a running process on the current Linux system.

    Attributes of a Process object:
        pid         : Process ID
        uid         : Owner user ID
        uname       : Owner user name
        comm        : Process binary file name
        state       : Process actual state (R/S/D/Z/T/t/W/X/x/K/W/P)
        ppid        : Parent process ID
        pgrp        : Process group ID of the process
        session     : The session ID of the process.
        utime       : Amount of time that this process has been scheduled in
                      user mode
        stime       : Amount of time that this process has been scheduled in
                      kernel mode
        cutime      : Amount of time that this process's waited-for children
                      have been scheduled in user mode
        cstime      : Amount of time that this process's waited-for children
                      have been scheduled in kernel mode
        nice        : The nice value, a value in therange 19 (low priority) to
                      -20 (high priority).
        num_threads : Number of threads in this process
        starttime   : The time the process started after system boot
        vsize       : Virtual memory size in bytes.
        hvsize      : Human versione of the virtual memory size of the process
                      (expressed in xx.x*B form, ex. 16.5 MB)
        rss         : Resident Set Size: number of pages the process has in
                      real memory
        processor   : CPU number last executed on.
        rt_priority : Real-time scheduling priority (0 for non-real-time processes)
        cmdline     : Full execution command (will be use an array structure)
        environ     : Full process environment
    """

    def __init__(self, proc_pid):
        """Process object construction and extraction of values from proc files."""
        self.pid = proc_pid  # Process ID
        self.uid = os.stat("/proc/" + str(self.pid)).st_uid  # User ID
        self.starttime = os.stat("/proc/" + str(self.pid)).st_ctime
        self.uname = ""
        # Extract almost all values from stat file
        with open("/proc/" + str(self.pid) + "/stat", "r") as handler:
            stat_content = handler.read()
        rgx = re.match("\d+\s+\((.+)\)\s(.+)", stat_content)
        if rgx:
            self.comm = rgx.group(1)
            fields = re.split("\s+", rgx.group(2))
            self.state = fields[0]
            self.ppid = int(fields[1])
            self.pgrp = int(fields[2])
            self.session = int(fields[3])
            self.utime = int(fields[11])
            self.stime = int(fields[12])
            self.cutime = int(fields[13])
            self.cstime = int(fields[14])
            self.nice = int(fields[16])
            self.num_threads = int(fields[17])
            self.vsize = int(fields[20])
            self.rss = int(fields[21])
            self.processor = int(fields[36])
            self.rt_priority = int(fields[37])
        # Values extracted from the cmdline virtual file and remove the last
        # one if empty
        with open("/proc/" + str(self.pid) + "/cmdline", "r") as handler:
            self.cmdline = re.split("\x00", handler.read())
        if self.cmdline[-1] == "":
            self.cmdline.pop()
        # Values extracted from the environ virtual file
        self.environ = {}
        try:
            with open("/proc/" + str(self.pid) + "/environ", "r") as handler:
                env_vars = handler.read()
            for env_var in re.split("\x00", env_vars):
                rgx = re.match("([^=]+)=(.+)", env_var)
                if rgx:
                    self.environ[rgx.group(1)] = rgx.group(2)
        except IOError:
            # Probabily the user doesn't have enought grant to read the process
            # environ file... but we don't care... just trace with the None value
            self.environ = None
            pass
        # Base unit
        unit = "B"
        size = Decimal(self.vsize)
        while size > 1024 and unit != "Y":
            size = (size / 1024)
            # Kilo Byte
            if unit == "B":
                unit = "K"
            # Mega Byte
            elif unit == "K":
                unit = "M"
            # Giga Byte
            elif unit == "M":
                unit = "G"
            # Tera Byte
            elif unit == "G":
                unit = "T"
            # Peta Byte
            elif unit == "T":
                unit = "P"
            # Exa Byte
            elif unit == "P":
                unit = "E"
            # Zetta Byte
            elif unit == "E":
                unit = "Z"
            # Yotta Byte
            elif unit == "Z":
                unit = "Y"
        # Set the value of the class attribute
        self.hvsize = "{0:.1f}{1}".format(size, unit)
