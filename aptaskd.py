#!/usr/bin/env python

"""
Asynchronous Parallel Task Execution Daemon Script
"""

__version__ = '0.0.0'


import multiprocessing
import os
import signal
import sys
import time

import configuration
import log
import manager
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
    @param config       Application configuration object
    @return             Exit code (0 = normal)
    """

    # global control flag
    global _is_running

    # add tasks directory to import path list
    sys.path.append( config.get_path( 'tasks' ) )

    # initialize the logging facility
    logger = log.Log( config.get_log_file(), config.loglevel )
    logger.append_message( 'initializing daemon' )

    # create the network server control and communications pipe
    ( p_pipe, c_pipe ) = multiprocessing.Pipe( True )

    # create network server in its own process
    netd = multiprocessing.Process(
        target = net.net,
        args   = ( c_pipe, config.get_address() ),
        name   = 'aptasknetd'
    )

    # create and start the task manager
    man = manager.Manager( config, logger )
    man.start()

    # set running flag
    _is_running = True

    # start the network server process
    netd.start()

    # enter daemon loop
    while _is_running == True:

        # check for requests from netd
        if p_pipe.poll() == True:

            # get message data and send to message handler
            message = p_pipe.recv()
            message.data = man.handle_request( message.data )
            p_pipe.send( message )

        # allow manager to process worker queues
        man.process()

        # poll interval (may not be needed, or could be adaptive)
        #if _is_running == True:
        #    time.sleep( 0.005 )

    # shut down task manager
    man.stop()

    # shut down network server
    p_pipe.send( net.QUIT )
    netd.join()

    # indicate shut down and close log
    logger.append_message( 'shutting down daemon' )
    logger.close()

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
    config = configuration.load_configuration( args.config )

    # check configuration
    if config is None:
        print 'invalid configuration'
        return -1

    # run the daemon until shut down
    exit_code = start( config )

    # return exit code
    return exit_code


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )
