#!/usr/bin/env python

"""
Task Execution Manager

Provides the top-level control and tracking of long-running worker processes.
"""


import json

import worker


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
        self.workers    = WorkerFIFO()

        self._update_environment()


    #=========================================================================
    def handle_request( self, request ):
        """
        """

        try:
            req = json.loads( request )
        except ValueError:
            res = { 'status' : 'error', 'message' : 'malformed request' }

        # ZIH - move auth check and incorporate type of request

        if 'key' not in req:
            res = { 'status' : 'error', 'message' : 'unspecified auth key' }

        elif self.config.is_user( req[ 'key' ] ) == False:
            res = { 'status' : 'error', 'message' : 'invalid auth key' }

        else:

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
                task_id = self.workers.add( Worker( req ) )
                res = {
                    "status" : "ok",
                    "response" : "start",
                    "taskid" : task_id
                }

            elif req[ 'request' ] == 'stop':
                wrkr = self.workers.remove( req[ 'taskid' ] )
                if wrkr is None:
                    res = {
                        "status" : "error",
                        "response" : "stop",
                        "taskid" : req[ 'taskid' ]
                    }
                else:
                    wrkr.send_abort()
                    # ZIH - 'join' to worker process after response is sent
                    res = {
                        "status" : "ok",
                        "response" : "stop",
                        "taskid" : req[ 'taskid' ]
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
    def _abort( self, id ):
        """
        """

        for w in self.workers:
            if w.id == id:
                w.send_abort()
                break


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
    def __init__( self, descriptor ):
        """
        Constructor.
        """

        self.command_queue   = None
        self.process         = None
        self.status_queue    = None
        self.task_descriptor = descriptor


    #=========================================================================
    def send_abort( self ):
        """
        """

        self.command_queue.send( worker.ABORT )


#=============================================================================
class WorkerFIFO( object ):
    """
    """


    #=========================================================================
    def __init__( self ):
        """
        Constructor.
        """

        self.next_id = 1
        self.queue   = []
        self.workers = {}


    #=========================================================================
    def add( self, wrkr ):
        """
        """

        task_id = str( self.next_id )
        self.next_id += 1
        self.queue.append( task_id )
        self.workers[ task_id ] = wrkr
        return task_id


    #=========================================================================
    def remove( self, task_id = None ):
        """
        """

        if task_id is None:
            index = 0
        else:
            try:
                index = self.queue.index( task_id )
            except ValueError:
                return None

        try:
            task_id = self.queue.pop( index )
        except IndexError:
            return None

        wrkr = self.workers[ task_id ]
        del self.workers[ task_id ]
        return wrkr


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
