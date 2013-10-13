#!/usr/bin/env python
##############################################################################
#
# aptaskd.py
#
# aptask Daemon Script
#
##############################################################################


import signal


#=============================================================================
def daemon():
    """
    Daemon function allows this to be used from a wrapper script.
    """

    # ZIH - start/check sqlite history database
    # ZIH - know host and port for net server
    # ZIH - start net server in its own process
    # ZIH - monitor the net request queue
    # ZIH - monitor active workers

    while( 1 ):
        pass


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

    # install some signal handlers to override what Python installed
    signal.signal( signal.SIGTERM, signal_handler )
    signal.signal( signal.SIGINT,  signal_handler )

    # ZIH - use proper argument handling to override default config file
    #   location

    # ZIH - do program configuration here

    # run the daemon until shut down
    exit_code = daemon()

    # return exit code
    return exit_code

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

