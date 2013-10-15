#!/usr/bin/env python

"""
Asynchronous Parallel Task Execution Daemon Script
"""

__version__ = '0.0.0'


import os
import signal

import log
import net


#=============================================================================
_is_running = False                 # daemon control flag


#=============================================================================
def signal_handler( signal_number, frame ):
    """
    Empty signal handler (for now)
    @param signal_number
                        The signal number from the OS interrupt
    @param frame        The frame
    """

    # stop the daemon
    stop()


#=============================================================================
def start( config ):
    """
    Daemon function allows this to be used from a wrapper script.
    @param config       A dictionary of configuration values
    @return             Exit code (0 = normal)
    """

    # global control flag
    global _is_running

    # initialize the logging facility
    log_file = config[ 'directories' ][ 'data' ] + os.sep + 'log.sqlite'
    log = log.Log( log_file )
    log.append_message( 'initializing daemon' )

    # create the network server control pipe
    ( p_pipe, c_pipe ) = multiprocessing.Pipe( True )

    # create network server in its own process
    netd = multiprocessing.Process(
        target = net.net,
        args   = ( c_pipe, ( config[ 'host' ], config[ 'port' ] ), handler ),
        name   = 'aptasknetd'
    )

    # create the task manager
    ### man = Manager()
    ### man.start()

    # set running flag
    _is_running = True

    # start the network server process
    netd.start()

    # enter daemon loop
    while _is_running == True:

        # check (p_pipe.poll()) for requests from netd
            # get responses from man

        # allow manager to also poll worker queues
        #   manager handles list of queues to poll
        ### man.process()


    # shut down task manager
    ### man.stop()

    # shut down network server
    p_pipe.send( net.QUIT )
    netd.join()

    # indicate shut down and close log
    log.append_message( 'shutting down daemon' )
    log.close()

    # return exit code
    return 0


#=============================================================================
def stop():
    """
    Stops the daemon function.
    """

    # global control flag
    global _is_running

    # exit the daemon loop at its next convenience
    _is_running = False


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
        print 'invalid configuration'
        return -1

    # run the daemon until shut down
    exit_code = start( config )

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

