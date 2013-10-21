#!/usr/bin/env python

"""
Task Execution Manager

Provides the top-level control and tracking of long-running worker processes.
"""


import json

import fifo
import request
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
        self.task_names = []
        self.task_index = []
        self.workers    = fifo.WorkerFIFO()

        self._update_environment()


    #=========================================================================
    def get_active( self ):
        """
        """

        # ZIH - need to support auth-key-based "session" lists

        active = []

        # get a list of all task IDs
        task_ids = self.workers.get_task_ids()

        # iterate over all workers in queue
        for task_id in task_ids:

            # get worker object for this task ID
            wrkr = self.workers.get( task_id )

            # convert report object into a dictionary, and make a copy
            report = dict( wrkr.get_status().__dict__ )

            # add process state and task ID
            report[ 'state' ]  = 'active' if wrkr.is_active() else 'inactive'
            report[ 'taskid' ] = task_id

            # add status to list
            active.append( report )

        # return worker status list
        return active


    #=========================================================================
    def handle_request( self, string ):
        """
        """

        # parse request
        req = request.Request( string )

        # check basic request validity
        if req.is_valid() == False:
            res = { 'status' : 'error', 'message' : 'malformed request' }

        # check request authorization
        elif self.config.is_authorized( req.key, req.request ) == False:
            res = { 'status' : 'error', 'message' : 'invalid auth key' }

        # request is, basically, in good shape
        else:

            # handle request for supported task index
            elif req.request == 'index':
                res = {
                    'status'   : 'ok',
                    'response' : 'index',
                    'index'    : self.task_index
                }

            # handle request to start a new task
            elif req.request == 'start':
                if req.name in self.task_names:
                    descr = worker.create_task_descriptor(
                        req.name,
                        req.arguments
                    )
                    task_id = self.workers.add( worker.Worker( descr ) )
                    res = {
                        'status'   : 'ok',
                        'response' : 'start',
                        'taskid'   : task_id
                    }
                else:
                    res = {
                        'status'   : 'error',
                        'response' : 'start',
                        'message'  : 'invalid task name'
                    }

            # handle request to stop an active/queued task
            elif req.request == 'stop':
                wrkr = self.workers.get( req.taskid )
                if wrkr is None:
                    res = {
                        'status'   : 'error',
                        'response' : 'stop',
                        'taskid'   : req.taskid
                    }
                else:
                    wrkr.stop()
                    res = {
                        'status'   : 'ok',
                        'response' : 'stop',
                        'taskid'   : req.taskid
                    }

            # handle request for all active tasks
            elif req.request == 'active':
                res = {
                    "status"   : "ok",
                    "response" : "active",
                    'active'   : self.get_active()
                }

            # unknown request command
            else:
                res = { 'status' : 'error', 'message' : 'invalid request' }

        # return a formatted response
        return json.dumps( res )


    #=========================================================================
    def process( self ):
        """
        """

        # service all the status queues to keep them from filling up
        for wrkr in self.workers:

            # i happen to know the worker object caches his status internally
            wrkr.get_status()

        # get all active task ids
        task_ids = self.workers.get_task_ids( active = True )

        # iterate over active tasks
        for task_id in task_ids:

            # get worker object for this task ID
            wrkr = self.workers.get( task_id )

            # look for workers that can be started (should be abstracted)
            if wrkr.state == worker.Worker.INIT:
                wrkr.start()

            # look for workers that have been stopped
            elif wrkr.state == worker.Worker.STOPPING:

                # let the worker take its time shutting down
                if wrkr.is_alive() == False:
                    wrkr.join()
                    self.workers.remove( task_id )

            # look for active worker status transitions
            else:

                # get latest status
                status = wrkr.get_status()

                # look for workers that are done and should be removed
                if status.is_done() == True:
                    wrkr.join()
                    self.workers.remove( task_id )


    #=========================================================================
    def start( self ):
        """
        """

        # nothing needed here, yet

        pass


    #=========================================================================
    def stop( self ):
        """
        """

        # get a copy of task IDs
        task_ids = self.workers.get_task_ids()

        # iterate over all task_ids in queue
        for task_id in task_ids:

            # get worker object for this task ID
            wrkr = self.workers.get( task_id )

            # check if this worker is active
            if wrkr.is_active() == True:
                wrkr.stop()

            # worker is inactive
            else:
                self.workers.remove( task_id )

        # get current copy of task IDs
        task_ids = self.workers.get_task_ids()

        # iterate over remaining task IDs
        for task_id in task_ids:

            # get worker object for this task ID
            wrkr = self.workers.get( task_id )

            # block until this worker is shut down
            wrkr.join()

            # remove worker from queue
            self.workers.remove( task_id )


    #=========================================================================
    def _update_environment( self ):
        """
        """

        self.task_index = self.config.get_task_index()
        self.task_names = [ x[ 'name' ] for x in self.task_index ]


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
