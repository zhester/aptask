#!/usr/bin/env python

"""
Worker Process
"""


import importlib
import multiprocessing
import Queue

import task


#=============================================================================
class Command( object ):
    """
    Worker control command.
    """


    #=========================================================================
    CONTINUE = 0
    ABORT    = 1


    #=========================================================================
    def __init__( self, command_id = Command.CONTINUE ):
        """
        Constructor.
        @param command_id
                        Command identifier
        """

        self.id = command_id


#=============================================================================
ABORT = Command( Command.ABORT )


#=============================================================================
class Worker( multiprocessing.Process ):
    """
    Worker process interface object.
    Instances of this object are intended to be used to control and interact
    with worker processes from a parent process.  No memory is shared with the
    worker process.
    """


    #=========================================================================
    INIT     = 0                    # initialized, ready to run
    RUNNING  = 1                    # running
    STOPPING = 2                    # shutting down process


    #=========================================================================
    state_strings = ( 'initialized', 'running', 'stopping' )


    #=========================================================================
    def __init__( self, descriptor ):
        """
        Constructor.
        """

        self.command_queue = multiprocessing.Queue()
        self.status_queue  = multiprocessing.Queue()

        super( Worker, self ).__init__(
            target = worker,
            args   = ( self.command_queue, self.status_queue, descriptor ),
            name   = 'aptask_worker'
        )

        self.state  = INIT
        self.status = None


    #=========================================================================
    def get_status( self ):
        """
        """

        # set invalid status to detect if there was a status update
        status = None

        # loop until the status queue is empty
        while True:
            try:
                status = self.status_queue.get_nowait()
            except Queue.Empty:
                break

        # check for an update
        if status is not None:
            self.status = status

        # return most recent status update
        return self.status


    #=========================================================================
    def is_active( self ):
        """
        """

        return self.state == RUNNING


    #=========================================================================
    def start( self ):
        """
        """

        self.state = RUNNING
        super( Worker, self ).start()


    #=========================================================================
    def stop( self ):
        """
        """

        if self.state == RUNNING:
            self.command_queue.send( ABORT )

        self.state = STOPPING


#=============================================================================
def create_task_descriptor( name, arguments ):
    """
    Decouples the structure of a task descriptor from code outside this
    module.  Don't count on the returned object having a consistent type or
    format.
    @param name         Task identifier
    @param arguments    Arguments to pass to the task
    """

    # for now, just use a dict
    return { 'name' : name, 'arguments' : arguments }


#=============================================================================
def worker( command_queue, status_queue, task_descriptor ):
    """
    Function to execute as a worker process.
    @param
    @param
    @param
    """

    command = None
    report  = None

    # create the task object according to the descriptor
    tsk = _create_task( task_descriptor )

    # initialize task
    #   some tasks will initialize here and start processing later
    #   some tasks will block here until complete
    #   some tasks won't implement this
    try:
        report = tsk.initialize()
    except task.NotSupported:
        pass

    # loop until the task reports completion
    while report.is_done() == False:

        # check for any pending messages
        try:
            command = command_queue.get_nowait()
        except Queue.Empty:
            pass
        else:
            if command.id == Command.ABORT:
                try:
                    report = tsk.abort()
                except task.NotSupported:
                    pass
                # ZIH - we're putting too much trust in the driver to
                #  set the done status here... we should keep some local
                # state and time out if we keep processing

        # spend time executing task
        try:
            report = tsk.process()
        except task.NotSupported:
            pass

        # send status and progress to manager
        try:
            status_queue.put_nowait( report )
        except Queue.Full:
            pass


#=============================================================================
def _create_task( descriptor ):
    """
    Creates a task object from a descriptor.
    @param descriptor   Task descriptor
    @return             Task instance
    ###@throws ValueError  When the descriptor can not be resolved
    """

    # import the task module by name
    module = importlib.import_module( descriptor[ 'name' ].lower() )

    # get the reference to the task driver class
    class_ref = getattr( module, descriptor[ 'name' ] )

    # instantiate the class, and return it
    return class_ref( descriptor[ 'arguments' ] )


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
