#!/usr/bin/env python

"""
Task Execution Manager

Provides the top-level control and tracking of long-running worker processes.
"""


#=============================================================================
class Manager( object ):
    """
    """


    #=========================================================================
    def __init__( self ):
        """
        Constructor.
        """

        self.workers = []


    #=========================================================================



#=============================================================================
class Worker( object ):
    """
    """


    #=========================================================================
    def __init__( self ):
        """
        Constructor.
        """

        self.command_queue   = None
        self.process         = None
        self.status_queue    = None
        self.task_descriptor = None



#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """



    # return success
    return 0

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

