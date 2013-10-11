#!/usr/bin/env python
##############################################################################
#
# aptaskd.py
#
# aptask Daemon Script
#
##############################################################################




#=============================================================================
def daemon():
    """
    Daemon function allows this to be used from a wrapper script.
    """

    while( 1 ):
        pass


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    # ZIH - do program configuration here
    # ZIH - do basic initialization, install signal handlers, etc

    # run the daemon until shut down
    exit_code = daemon()

    # return exit code
    return exit_code

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

