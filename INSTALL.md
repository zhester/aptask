Installation
============

Introduction and Prerequisites
------------------------------



Configuring
-----------

Edit aptaskd.json to change settings.

### Network Configuration ###

`host` specifies the host to which the network service will bind.  Leave this
empty to bind to all addresses on all interfaces.

`port` specifies the TCP port on which the service will listen.

### Environment Configuration ###

`directories.tasks` specifies the directory to find user-defined task drivers.

`directories.data` specifies a directory to which the daemon's owner can write
log files and program state data.

### Authorization Configuration ###

`keys` provides a way to authorize and identify job requests.  Keys in the
admins group can view all current tasks and query the task logs.  Keys in the
users group can request task execution and status for tasks requested under
that key.  Any number of keys may be used in either group.

To disable authentication for a particular group, replace the array with
`null`.
