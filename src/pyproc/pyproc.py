
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
import pwd
from datetime import datetime, timedelta

from process import Process


class pyproc:
    """Main library class.

    Attributes of the class:
        boot_ts : datetime object of the system boot timestamp
        procs   : dictionary containing all the running processes on the system;
                  keys are the process ID and values are Process objects
        users   : dictionary conatining all the users of the local system; keys
                  are the users ID and values are the users name
    """

    def __init__(self):
        """Main class constructor.

        The first step calculate the timestamp of the system boot (boot_ts), to
        decode all processes time infos that are expressed in seconds after the
        system boot.
        """
        # Read system uptime
        with open("/proc/uptime", "r") as handler:
            # Seconds of system uptime
            uptime_sec = int(re.split("\s+", handler.read())[0])
        # System boot timestamp
        self.boot_ts = datetime.now() - timedelta(seconds=uptime_sec)
        # Dictionary with all active processes
        self.procs = None
        # Dictionary with all users of the system from password database
        self.users = None
        # First load of all values
        self.up()

    def up(self):
        """Method to update all pyproc values."""
        # Reset the dictionary containing the active processes
        self.procs = {}
        # Extract all process from the /proc directory
        for dir_name in os.listdir("/proc"):
            if os.path.isdir("/proc/" + dir_name) and re.match("\d+$", dir_name):
                if os.path.exists("/proc/" + dir_name + "/cmdline"):
                    self.procs[int(dir_name)] = Process(int(dir_name))
        # Reset the dictionary containing the system user
        self.procs = {}
        # Extract a new users list
        for user in pwd.getpwall():
            self.users[int(user.pwd_uid)] = user.pw_name
