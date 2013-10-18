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
    def __init__( self, config, logger ):
        """
        Constructor.
        @param config
        @param logger
        """

        self.config     = config
        self.log        = logger
        self.task_index = None
        self.workers    = []

        self._update_environment()


    #=========================================================================
    def handle_request( self, request ):
        """
        """

        req = json.loads( request )

        # ZIH - auth check request here

        if 'request' not in req:
            res = { 'status' : 'error', 'message' : 'unspecified request' }

        elif req[ 'request' ] == 'index':
            res = {
                "status" : "ok",
                "response" : "index",
                "index" : self.task_index
            }

        elif req[ 'request' ] == 'start':
            # ZIH - verify task name
            # ZIH - allocate worker, determine portable ID
            res = {
                "status" : "ok",
                "response" : "start",
                # ZIH
                "taskid" : 42
            }

        elif req[ 'request' ] == 'stop':
            # ZIH - verify task ID, send abort
            res = {
                "status" : "ok",
                "response" : "stop",
                # ZIH
                "taskid" : 42
            }

        elif req[ 'request' ] == 'active':
            res = {
                "status" : "ok",
                "response" : "active",
                # ZIH
                "active" : []
            }

        else:
            res = { 'status' : 'error', 'message' : 'invalid request' }

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

        self.task_index = self.config.get_task_index()


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

    import configuration
    import log
    conf = configuration.load_configuration( 'aptaskd.json' )
    logger = log.Log( conf.get_log_file() )

    m = Manager( conf, logger )

    print m.handle_request( '{"request":"index"}' )

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
