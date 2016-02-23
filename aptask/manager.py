#=============================================================================
#
# Task Execution Manager
#
#=============================================================================


"""
Task Execution Manager
======================

Provides the top-level control and tracking of long-running worker processes.
"""


import json

import fifo
import log
import request
import worker


#=============================================================================
class Manager( object ):
    """
    Implements handling outside requests and managing tasking resources to
    fulfill those requests.
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
        self.task_index = []
        self.task_names = []
        self.workers    = fifo.WorkerFIFO()

        self._update_environment()


    #=========================================================================
    def get_active( self, authkey = None ):
        """
        Retrieves a list of dicts that reports the current status of all
        active tasks.
        @param authkey  Specify to restrict list to tasks owned by that user
        @return         A list of dicts describing the active tasks
        """

        # set up a list to populate
        active = []

        # set up a queue position index
        position = -1

        # get a list of all task IDs
        task_ids = self.workers.get_task_ids()

        # iterate over all workers in queue
        for task_id in task_ids:

            # increment position index
            position += 1

            # get worker object for this task ID
            wrkr = self.workers[ task_id ]

            # check to see if this worker is for the given auth key
            if ( authkey is not None ) and ( wrkr.authkey != authkey ):

                # do not report on other user's tasks
                continue

            # get the most recent task status
            status = wrkr.get_status()

            # make sure the worker has a status to report
            if status is not None:

                # get a copy of the report object as a dictionary
                report = status.__getstate__()

            # the worker does not have a meaningful status to report
            else:
                report = {}

            # add position, process state, and task ID
            report[ 'position' ] = position
            report[ 'taskid' ]   = task_id
            if wrkr.is_active() == True:
                report[ 'state' ] = 'active'
            else:
                report[ 'state' ] = 'inactive'

            # add status to list
            active.append( report )

        # return worker status list
        return active


    #=========================================================================
    def handle_request( self, string ):
        """
        Handles outside requests for task execution, control, and updates.
        @param string   A JSON-formatted request string
        @return         A JSON-formatted response string
        """

        # parse request
        req = request.Request( string )

        # check basic request validity
        if req.is_valid() == False:
            res = { 'status' : 'error', 'message' : 'malformed request' }
            self.log.log( log.CLIENT_ERROR, string )

        # check request authorization
        elif self.config.is_authorized( req.key, req.request ) == False:
            res = { 'status' : 'error', 'message' : 'invalid auth key' }
            self.log.log( log.CLIENT_ERROR, string )

        # request is, basically, in good shape
        else:

            # handle request for supported task index
            if req.request == 'index':
                res = {
                    'status'   : 'ok',
                    'response' : 'index',
                    'index'    : self.task_index
                }
                self.log.log( log.REQUEST, string, req.key )

            # handle request to start a new task
            elif req.request == 'start':
                if req.name in self.task_names:
                    descr = worker.create_task_descriptor(
                        req.name,
                        req.arguments
                    )
                    task_id = self.workers.add(
                        worker.Worker( descr, req.key )
                    )
                    res = {
                        'status'   : 'ok',
                        'response' : 'start',
                        'taskid'   : task_id
                    }
                    self.log.log( log.REQUEST, string, req.key )
                else:
                    res = {
                        'status'   : 'error',
                        'response' : 'start',
                        'message'  : 'invalid task name'
                    }
                    self.log.log( log.CLIENT_ERROR, string, req.key )

            # handle request to stop an active/queued task
            elif req.request == 'stop':
                wrkr = self.workers[ req.taskid ]
                if wrkr is None:
                    res = {
                        'status'   : 'error',
                        'response' : 'stop',
                        'taskid'   : req.taskid
                    }
                    self.log.log( log.CLIENT_ERROR, string, req.key )
                else:
                    wrkr.stop()
                    res = {
                        'status'   : 'ok',
                        'response' : 'stop',
                        'taskid'   : req.taskid
                    }
                    self.log.log( log.REQUEST, string, req.key )

            # handle request for all active tasks
            elif req.request == 'active':
                res = {
                    "status"   : "ok",
                    "response" : "active",
                    'active'   : self.get_active( req.key )
                }
                self.log.log( log.REQUEST, string, req.key )

            # unknown request command
            else:
                res = { 'status' : 'error', 'message' : 'invalid request' }
                self.log.log( log.CLIENT_ERROR, string, req.key )

        # format the response
        response = json.dumps( res )

        # log the response
        self.log.log( log.RESPONSE, response )

        # return a formatted response
        return response


    #=========================================================================
    def process( self ):
        """
        Method to periodically invoke to keep the task manager current.
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
            wrkr = self.workers[ task_id ]

            # look for workers that can be started (should be abstracted)
            if wrkr.state == worker.Worker.INIT:
                wrkr.start()
                self.log.log( log.TASKING, 'starting task %s' % task_id )

            # look for workers that have been stopped
            elif wrkr.state == worker.Worker.STOPPING:

                # let the worker take its time shutting down
                if wrkr.is_alive() == False:
                    wrkr.join()
                    self.workers.remove( task_id )
                    self.log.log( log.TASKING, 'stopping task %s' % task_id )

            # look for active worker status transitions
            else:

                # get latest status
                status = wrkr.get_status()

                # look for workers that are done and should be removed
                if ( status is not None ) and ( status.is_done() == True ):
                    wrkr.join()
                    self.workers.remove( task_id )
                    self.log.log( log.TASKING, 'stopping task %s' % task_id )


    #=========================================================================
    def start( self ):
        """
        Method to call before task management needs to begin.
        """

        # nothing needed here, yet

        pass


    #=========================================================================
    def stop( self ):
        """
        Method to call when task management needs to stop.
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
        Updates expensively-obtained information about the execution
        environment.
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

