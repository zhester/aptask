#!/usr/bin/env python

"""
Task Execution Manager

Provides the top-level control and tracking of long-running worker processes.
"""


import json


#=============================================================================
class Manager( object ):
    """
    """


    #=========================================================================
    def __init__( self, config, log ):
        """
        Constructor.
        @param config
        @param log
        """

        self.config  = config
        self.log     = log
        self.workers = []


    #=========================================================================
    def handle_request( self, request ):
        """
        """

        req = json.loads( request )
        res = { 'status' : 'ok' }
        return json.dumps( res )


    #=========================================================================
    def process( self ):
        """
        """

        pass


    #=========================================================================
    def start( self ):
        """
        """

        pass


    #=========================================================================
    def stop( self ):
        """
        """

        pass


    #=========================================================================
    def _update_environment( self ):
        """
        """

        # scan tasks directory and load driver docs into memory
        #   used to check task requests and send task index
        pass


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

