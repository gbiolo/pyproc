
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


import re


class UserError(Exception):
    """Exception raised if user is not present on the system."""

    def __init__(self, message):
        """Exception UserError constructor. Nothing special."""
        self.message = message


class ProcList:

    def __init__(self, users):
        # Initialize an empty list of processes
        self.proclist = []
        # Initialize a zero iterator
        self.index = -1
        # Dictionary of system users (UID: username)
        self.users = users

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        if self.index < len(self.proclist):
            return self.proclist[self.index]
        else:
            self.index = -1
            raise StopIteration

    def __nonzero__(self):
        if len(self.proclist) == 0:
            return False
        else:
            return True

    def append(self, proc):
        self.proclist.append(proc)

    def select_user(self, user):
        # User id
        user_id = user
        # Check if the user passed the right argument type
        if type(user) is not int and type(user) is not str:
            raise TypeError("User must be indicated with integer UID or string username")
        # Check if the UID exists...
        if type(user) is int:
            if user not in self.users:
                raise UserError("User with UID " + str(user) + " doesn't exists")
        # ...or check if the username exists
        elif type(user) is str:
            if user not in self.users.values():
                raise UserError("User " + user + " doesn't exists")
            else:
                # Extract the user ID
                for uid in self.users:
                    if self.users[uid] == user:
                        user_id = uid
                        break
        # Check if there are processes into the procs dictionary... if empty
        # return None
        if len(self.proclist) == 0:
            return None
        # Go on with the extraction...
        else:
            # New empty ProcList object
            new_proclist = ProcList(self.users)
            for proc in self.proclist:
                if proc.uid == user_id:
                    new_proclist.append(proc)
            # Return the extracted ProcList
            return new_proclist

    def search_bin(self, bin_name):
        if type(bin_name) is not str:
            raise TypeError("Binary search must be indicated with a string")
        # If the proclist is empty return a None value
        if len(self.proclist) == 0:
            return None
        else:
            # Create a new empty ProcList for the matching processes
            new_proclist = ProcList(self.users)
            # Insertion into the new ProcList of all processes with the right
            # binary command
            for proc in self.proclist:
                if re.search(bin_name, proc.comm):
                    new_proclist.append(proc)
            return new_proclist

    def search_cmdline(self, cmdline_arg):
        if type(cmdline_arg) is not str:
            raise TypeError("Comand argument must be indicated with a string")
        # If the proclist is empty return a None value
        if len(self.proclist) == 0:
            return None
        else:
            # Create a new empty ProcList for the matching processes
            new_proclist = ProcList(self.users)
            # For each process into the self proclist search the passed string
            # The search must be extended to all cmdline arguments
            for proc in self.proclist:
                for arg in proc.cmdline:
                    if re.search(cmdline_arg, arg):
                        new_proclist.append(proc)
                        break
            return new_proclist
