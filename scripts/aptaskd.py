#!/usr/bin/env python2
#=============================================================================
#
# aptask Daemon Script
#
#=============================================================================


__version__ = '0.0.0'



"""
Asynchronous Parallel Task Queue Daemon Script
==============================================
"""


__version__ = '0.0.1'


import logging
import multiprocessing
import os
import signal
import sys
import time


# Allow development-only importing.
try:
    import aptask
except ImportError:
    script_path = os.path.realpath( __file__ )
    script_dir  = os.path.dirname( script_path )
    proj_dir    = os.path.dirname( script_dir )
    sys.path.insert( 0, proj_dir )
    import aptask


# Initialize the logging sub-system.
logging.basicConfig()

# Create the root logger.
_logger = logging.getLogger()


#=============================================================================
_is_running = False               # daemon control flag


#=============================================================================
def signal_handler( signal_number, frame ):
    """
    Implements the daemon's signal handler.

    @param signal_number The signal number from the OS interrupt
    @param frame         The frame
    """

    # Stop the daemon.
    stop()


#=============================================================================
def start( config ):
    """
    Allows this to be used from a wrapper script.

    @param config Application configuration object
    @return       Shell exit code (0 = normal)
    """

    # Global control flag
    global _is_running

    # Add tasks directory to import path list.
    sys.path.append( config.get_path( 'tasks' ) )

    # Notify the log that we're starting.
    _logger.info( 'Initializing daemon.' )

    # Create the network server control and communications pipe.
    ( p_pipe, c_pipe ) = multiprocessing.Pipe( True )

    # Create network server in its own process.
    netd = multiprocessing.Process(
        target = aptask.net.net,
        args   = ( c_pipe, config.get_address() ),
        name   = 'aptasknetd'
    )

    # Create and start the task manager.
    man = aptask.manager.Manager( config )
    man.start()

    # Set running flag.
    _is_running = True

    # Start the network server process.
    netd.start()

    # Enter daemon loop.
    while _is_running == True:

        # Check for requests from netd.
        if p_pipe.poll() == True:

            # Get message data and send to message handler.
            message = p_pipe.recv()
            message.data = man.handle_request( message.data )
            p_pipe.send( message )

        # Allow manager to process worker queues.
        man.process()

        # poll interval (may not be needed, or could be adaptive)
        #if _is_running == True:
        #    time.sleep( 0.005 )

    # Shut down task manager.
    man.stop()

    # Shut down network server.
    p_pipe.send( aptask.net.QUIT )
    netd.join()

    # Notify the log that we're stopping.
    _logger.info( 'Shutting down daemon.' )

    # Return exit code.
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
        '-i',
        '--config',
        default = 'conf/aptaskd.json',
        help    = 'Load configuration file from this location.'
    )
    parser.add_argument(
        '-v',
        '--version',
        default = False,
        help    = 'Display script version and exit.',
        action  = 'version',
        version = __version__
    )

    # parse the arguments
    args = parser.parse_args( argv[ 1 : ] )

    # load configuration
    config = aptask.configuration.load_configuration( args.config )

    # check configuration
    if config is None:
        print 'invalid configuration'
        return -1

    # Adjust logging level.
    _logger.setLevel( config.loglevel )

    # run the daemon until shut down
    exit_code = start( config )

    # return exit code
    return exit_code


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

