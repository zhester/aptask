#=============================================================================
#
# Worker Process
#
#=============================================================================


"""
Worker Process
==============
"""


import importlib
import multiprocessing
import Queue

import data
import task
import watchdog


#=============================================================================
class Command( data.Data ):
    """
    Worker control command.
    """


    #=========================================================================
    CONTINUE = 0
    ABORT    = 1


    #=========================================================================
    _fields = [
        ( 'command_id', CONTINUE ) # Command message identifier
    ]


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
    def __init__( self, descriptor, authkey = None ):
        """
        Constructor.
        @param descriptor
                        Task execution descriptor
        @param authkey  Task owner's authentication key
        """

        # create the IPC message queues
        self.command_queue = multiprocessing.Queue()
        self.status_queue  = multiprocessing.Queue()

        # initialize the parent
        super( Worker, self ).__init__(
            target = worker,
            args   = ( self.command_queue, self.status_queue, descriptor ),
            name   = 'aptaskworker'
        )

        # initialize object state
        self.authkey = authkey
        self.state   = Worker.INIT
        self.status  = None


    #=========================================================================
    def get_status( self ):
        """
        Get the latest status for this task.
        @return         A Report object describing the status
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
        Check to see if the worker is actively processing its task.
        @return         True if the worker is active
        """

        return self.state == Worker.RUNNING


    #=========================================================================
    def start( self ):
        """
        Start executing the task.
        """

        self.state = Worker.RUNNING
        super( Worker, self ).start()


    #=========================================================================
    def stop( self ):
        """
        Stop executing the task.
        """

        if self.state == Worker.RUNNING:
            self.command_queue.send( ABORT )

        self.state = Worker.STOPPING


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
    @param command_queue
                        IPC command queue from parent process
    @param status_queue IPC status queue to parent process
    @param task_descriptor
                        Task descriptor
    """

    # set up a watchdog timer
    dog = watchdog.Timer()

    # create the task object according to the descriptor
    tsk = _create_task( task_descriptor )

    # initialize task
    #   some tasks will initialize here and start processing later
    #   some tasks will block here until complete
    #   some tasks won't implement this
    try:
        report = tsk.initialize()
    except task.NotSupported:
        report = task.Report()

    # loop until the task reports completion
    while report.is_done() == False:

        # check the watchdog timer for a timeout after a stuck abort
        if dog.check() == False:
            break

        # check for any pending messages
        try:
            command = command_queue.get_nowait()
        except Queue.Empty:
            pass
        else:

            # check for an abort command
            if command.id == Command.ABORT:

                # try to abort the task
                try:
                    report = tsk.abort()

                # not supported, just stop processing
                except task.NotSupported:
                    break

                # start a timer to make sure we abort the process
                else:
                    dog.start()

        # spend time executing task
        #   some tasks will quickly update status here
        #   some tasks will block here until complete
        #   some tasks won't implement this
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

    @param descriptor Task descriptor
    @return           Task instance
    """

    # import the task module by name
    module = importlib.import_module( descriptor[ 'name' ].lower() )

    # get the reference to the task driver class
    class_ref = getattr( module, descriptor[ 'name' ] )

    # instantiate the class, and return it
    return class_ref( descriptor[ 'arguments' ] )

