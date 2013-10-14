#!/usr/bin/env python

"""
Asynchronous Parallel Task Execution Daemon Script
"""

__version__ = '0.0.0'


import os
import signal

import log


#=============================================================================
def daemon( config ):
    """
    Daemon function allows this to be used from a wrapper script.
    @param config       A dictionary of configuration values
    @return             Exit code (0 = normal)
    """

    # initialize the logging facility
    log_file = config[ 'directories' ][ 'data' ] + os.sep + 'log.sqlite'
    log = log.Log( log_file )
    log.append_message( 'initializing daemon' )

    # create the network control pipe

    # create the task manager

    # start network server in its own process
    # target = net.net
    # args   = ( pipe, ( config[ 'host' ], config[ 'port' ] ), handler )

    # enter the task manager's daemon loop
    #  -- could just be an iterative "process" call

    # return exit code
    return 0


#=============================================================================
def signal_handler( signal_number, frame ):
    """
    Empty signal handler (for now)
    @param signal_number
                        The signal number from the OS interrupt
    @param frame        The frame
    """

    pass


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    # imports when using this as a script
    import argparse
    import json

    # install some signal handlers to override what Python installed
    signal.signal( signal.SIGTERM, signal_handler )
    signal.signal( signal.SIGINT,  signal_handler )

    # create and configure an argument parser
    parser = argparse.ArgumentParser(
        description = 'Asynchronous Parallel Task Execution Daemon Script'
    )
    parser.add_argument(
        '-c',
        '--config',
        default = 'aptaskd.json',
        help    = 'Load configuration file from this location.'
    )
    parser.add_argument(
        '-v',
        '--version',
        default = False,
        help    = 'Display script version.',
        action  = 'store_true'
    )

    # parse the arguments
    args = parser.parse_args( argv[ 1 : ] )

    # check for version request
    if args.version == True:
        print 'Version', __version__
        return 0

    # load configuration
    config = json.load( args.config )

    # check configuration
    if _check_configuration( config ) == False:
        return -1

    # run the daemon until shut down
    exit_code = daemon( config )

    # return exit code
    return exit_code


#=============================================================================
def _check_configuration( config ):
    """
    Checks the supplied configuration against reality.
    @param config       The configuration dictionary
    @return             True if the config will work, false if not
    """

    if 'host' not in config:
        return False

    if 'port' not in config:
        return False

    if 'directories' not in config:
        return False

    dirs = config[ 'directories' ]

    if 'data' not in dirs:
        return false

    if 'tasks' not in dirs:
        return false

    if os.access( dirs[ 'data' ], ( os.R_OK | os.W_OK | os.X_OK ) ) == False:
        return False

    if os.access( dirs[ 'tasks' ], ( os.R_OK | os.X_OK ) ) == False:
        return False

    return True


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

