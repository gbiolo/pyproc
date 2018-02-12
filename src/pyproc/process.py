
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


import os
import re


class Process:
    """Object that rappresent a running process on the current Linux system."""

    def __init__(self):
        """Initialization of an empty Process object."""
        # Vales extracted from the stat virtual file
        self.pid = None          # (1) Process ID
        self.comm = None         # (2) Process binary file name
        self.stat = None         # (3) Process actual state (R/S/D/Z/T/t/W/X/x/K/W/P)
        self.ppid = None         # (4) Parent process ID
        self.pgrp = None         # (5) Process group ID of the process
        self.session = None      # (6) The session ID of the process.
        self.tty = None          # (7) The controlling terminal of the process
        self.utime = None        # (14) Amount of time that this process has been scheduled in user mode
        self.stime = None        # (15) Amount of time that this process has been scheduled in kernel mode
        self.cutime = None       # (16) Amount of time that this process's waited-for children have been scheduled in user mode
        self.cstime = None       # (17) Amount of time that this process's waited-for children have been scheduled in kernel mode
        self.nice = None         # 19) The nice value, a value in therange 19 (low priority) to -20 (high priority).
        self.num_threads = None  # (20) Number of threads in this process
        self.starttime = None    # (22) The time the process started after system boot
        self.vsize = None        # (23) Virtual memory size in bytes.
        self.rss = None          # (24) Resident Set Size: number of pages the process has in real memory
        self.processor = None    # (39) CPU number last executed on.
        self.rt_priority = None  # (40) Real-time scheduling priority (0 for non-real-time processes)
        # Values extracted from the cmdline virtual file
        self.cmdline = None      # Full execution command (will be use an array structure)
        # Values extracted from the environ virtual file
        self.environ = None      # Full process environment

    def _extract_stat(content):
        """Split the stat file content in fields."""
        fields = re.split("\s+", content)
        output = []
        output.append(int(fields[0]))   # Process ID
        output.append(fields[1])        # Process binary file name
        output.append(fields[2])        # Process actual state (R/S/D/Z/T/t/W/X/x/K/W/P)
        output.append(int(fields[3]))   # Parent process ID
        output.append(int(fields[4]))   # Process group ID of the process
        output.append(int(fields[5]))   # The session ID of the process.
        output.append(fields[6])        # The controlling terminal of the process
        output.append(int(fields[13]))  # Amount of time that this process has been scheduled in user mode
        output.append(int(fields[14]))  # Amount of time that this process has been scheduled in kernel mode
        output.append(int(fields[15]))  # Amount of time that this process's waited-for children have been scheduled in user mode
        output.append(int(fields[16]))  # Amount of time that this process's waited-for children have been scheduled in kernel mode
        output.append(int(fields[18]))  # The nice value, a value in therange 19 (low priority) to -20 (high priority).
        output.append(int(fields[19]))  # Number of threads in this process
        output.append(int(fields[21]))  # The time the process started after system boot
        output.append(int(fields[22]))  # Virtual memory size in bytes.
        output.append(int(fields[23]))  # Resident Set Size: number of pages the process has in real memory
        output.append(int(fields[38]))  # CPU number last executed on.
        output.append(int(fields[39]))  # Real-time scheduling priority (0 for non-real-time processes)

    def load_proc(self, proc_pid):
        """Load the value of a running process from a given PID."""
        # Continue only if the proc directory exists (the process is running)
        proc_path = "/proc/" + str(proc_pid)
        if os.path.exists(proc_path):
            try:
                with open(proc_path + "/stat", "r") as handler:
                    stat_content = handler.read()
                stat_fields = self._extract_stat(stat_content)
                self.pid = stat_fields[0]
                self.comm = stat_fields[1]
                self.stat = stat_fields[2]
                self.ppid = stat_fields[3]
                self.pgrp = stat_fields[4]
                self.session = stat_fields[5]
                self.tty = stat_fields[6]
                self.utime = stat_fields[7]
                self.stime = stat_fields[8]
                self.cutime = stat_fields[9]
                self.cstime = stat_fields[10]
                self.nice = stat_fields[11]
                self.num_threads = stat_fields[12]
                self.starttime = stat_fields[13]
                self.vsize = stat_fields[14]
                self.rss = stat_fields[15]
                self.processor = stat_fields[16]
                self.rt_priority = stat_fields[17]
            except IOError:
                # The process is not still running, so the directory into proc
                # doesn't exists anymore... but we don't care now!
                return False
            except IndexError:
                raise IndexError("Error in parsing stat file for PID " + proc_pid)
        else:
            return False
