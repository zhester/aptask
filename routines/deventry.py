#=============================================================================
#
# Simplified Entry-point-style Routine for Development
#
#=============================================================================

"""
Simplified Entry-point-style Routine for Development
====================================================

This routine implements the entry-point-style for creating new routines.  This
requires a much smaller burden on adding new routines.  This module can be
used as a template for creating new custom routines, or for development and
testing purposes.

Function
--------

Simple entry points are defined as a module-level function named `routine()`.
This function is treated as a generator.  This means it must return either an
iterable object or successively `yield` values from a control loop.

### Function Docstring

The function's docstring is made available to clients as potentially helpful
information on how to use the routine.

Arguments
---------

The entry point's argument list is reported to the application's clients.  The
function should formally define all arguments it accepts.  All arguments
_should_ specify default values.  The default values are also made available
to clients, and can avoid issues when clients don't fully specify all
arguments (either on purpose or by mistake/defect).

Return Values
-------------

This system attempts to implement a flexible, un-typed communication channel
between routines and the calling user.  Therefore, different types and values
imply different state changes and statuses in the routine.

### `float` Values

A typical minimal status can be given with a `float` value.  When the caller
receives a fractional number, it assumes that values between 0.0 and 1.0 are
reports on the progress of the routine.  The meanings of the various values
are as indicated below.

| Value         | Meaning                                       |
| ------------- | --------------------------------------------- |
| 0.0           | Routine is successfully initialized.          |
| 0.0 < v < 1.0 | Routine is making progress towards its goal.  |
| 1.0           | Routine has successfully finished processing. |
| v < 0.0       | Routine has encountered an error.             |
| v > 1.0       | Undefined/reserved for future use.            |

### `int` Values

The caller will treat integer values similarly to a shell-style exit code.

| Value | Meaning                             |
| ----- | ----------------------------------- |
| 0     | Routine successfully completed.     |
| v > 0 | Routine encountered an error.       |
| v < 0 | Undefined/reserved for future user. |

### Any Other Object

The caller will assume that all other objects imply the routine has finished.
The object will be serialized and made available to clients in the processing
results.

Minimal Example
---------------

The following two routines take no arguments, and always indicates they have
completed.

    def routine():
        yield 0

    def routine():
        return [ 0 ]

Example with Progress
---------------------

    def routine():
        progress = 0.0
        while progress <= 1.0:
            time.sleep( 1 )
            yield progress
            progress += 0.1

"""


import time


__version__ = '0.0.0'


#=============================================================================
def routine( arg1 = 1, arg2 = 2.0, arg3 = '3', arg4 = None, wait = 0.0 ):
    """
    Development and testing routine.

    @param * List of arguments with default values (see: module's docstring)
    @return  A routine status value (see: module's docstring)
    """
    progress = 0.0
    while progress <= 1.0:
        time.sleep( wait )
        yield progress
        progress += 0.1

