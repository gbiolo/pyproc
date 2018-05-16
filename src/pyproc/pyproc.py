
"""PyProc is a library to easily read Linux running processes info.

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

from process import Process
from proclist import ProcList


class PyProc:
    """Main library class.

    Attributes of the class:
        boot_ts : datetime object of the system boot timestamp
        procs   : dictionary containing all the running processes on the system;
                  keys are the process ID and values are Process objects
        users   : dictionary conatining all the users of the local system; keys
                  are the users ID and values are the users name
    """

    def __init__(self):
        """Main class constructor. Just declare and empty dictionary for the users."""
        # Dictionary with all users of the system from password database
        self.users = {}

    def __call__(self):
        self.users = {}
        # Extract all the system users and insert into the dictionary
        for user in pwd.getpwall():
            self.users[int(user.pw_uid)] = user.pw_name
        # A new ProcList object to return to the user
        new_proclist = ProcList(self.users)
        # Extract all process from the /proc directory and add to the ProcList
        for dir_name in os.listdir("/proc"):
            try:
                if os.path.isdir("/proc/" + dir_name) and re.match("\d+$", dir_name):
                    if os.path.exists("/proc/" + dir_name + "/cmdline"):
                        new_proc = Process(int(dir_name))
                        if new_proc:
                            new_proc.uname = self.users[new_proc.uid]
                            new_proclist.append(new_proc)
            except Exception:
                pass
        # Return the new ProcList just created
        return new_proclist
