#!/usr/bin/env python
##############################################################################
#
# task.py
#
##############################################################################



#=============================================================================
class task( object ):
    """
    Object created and used by a worker process to start and monitor a task.
    Adding a new task interface requires implementing a child of this class.
    Child classes must implement the following methods:
        abort           Called to stop the task before completion
        start           Called to start the task
    Child classes should also implement the following method:
        get_progress    Called to retrieve execution progress
    """


    #=========================================================================
    def __init__( self ):
        """
        Constructor.
        """

        pass


    #=========================================================================
    def abort( self ):
        """
        Stops the execution of this task before completion.
        @throws         NotImplementedError
        """

        raise NotImplementedError


    #=========================================================================
    def get_progress( self ):
        """
        Retrieves the most up-to-date task progress state.
        @return         Task progress from 0.0 (none) to 1.0 (done)
        @throws         NotImplementedError
        """

        raise NotImplementedError


    #=========================================================================
    def start( self ):
        """
        Starts the execution of this task.
        @throws         NotImplementedError
        """

        raise NotImplementedError



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

