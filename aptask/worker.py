#=============================================================================
#
# Worker Process
#
#=============================================================================


"""
Worker Process
==============

The worker module implements the process management class `Worker` that uses
the process entry point `worker` to execute tasks in a separate process from
the aptask manager/scheduler.

The worker is responsible for handling commands from the manager, and
reporting its status as the task is executing.  Well-written routines will
allow the worker process to refresh the status regularly.
"""


import importlib
import multiprocessing
import Queue

import data
import routine
import watchdog


#=============================================================================
class Command( data.Data ):
    """
    Worker control command data objects
    """


    #=========================================================================
    CONTINUE = 0 # Default command (basically a no-op)
    ABORT    = 1 # Worker commanded to abort further task execution


    #=========================================================================
    _fields = [
        ( 'command_id', CONTINUE ) # Command message identifier
    ]


    #=========================================================================
    def __eq__( self, other ):
        """
        Allow comparison operator to work with command objects.

        @param other The other instance to compare to the current instance
        @return      True if both instances are functionally equal
        """
        return self.command_id == other.command_id


#=============================================================================
# Create the commonly-used abort command.
ABORT_COMMAND = Command( Command.ABORT )


#=============================================================================
class Worker( multiprocessing.Process ):
    """
    Worker process interface object

    Instances of this object are intended to be used to control and interact
    with worker processes from a parent process.  No memory is shared with the
    worker process.
    """


    #=========================================================================
    INIT     = 0 # Initialized, ready to run
    RUNNING  = 1 # Running
    STOPPING = 2 # Shutting down process


    #=========================================================================
    state_strings = ( 'initialized', 'running', 'stopping' )


    #=========================================================================
    def __init__( self, descriptor, group = None ):
        """
        Initializes a Worker instance.

        @param descriptor Routine execution descriptor dictionary
        @param group      Task namespace group
        """

        # Create the IPC message queues.
        self._command_queue = multiprocessing.Queue()
        self._status_queue  = multiprocessing.Queue()

        # Initialize parent state.
        super( Worker, self ).__init__(
            target = worker,
            args   = ( self._command_queue, self._status_queue, descriptor ),
            name   = 'aptask_worker_' + descriptor[ 'name' ]
        )

        # Initialize object state.
        self.group   = group
        self._state  = self.INIT
        self._status = None


    #=========================================================================
    def get_status( self ):
        """
        Retreives the latest status for this task.

        @return A Report object describing the routine's status
        """

        # Set invalid status to detect if there was a status update.
        status = None

        # Loop until the status queue is empty.
        while True:

            # Attempt to dequeue the next item in the status queue.
            try:
                status = self._status_queue.get_nowait()

            # No new status reports from routine.
            except Queue.Empty:
                break

        # Check for an update to the status.
        if status is not None:

            # Update the tracked status.
            self._status = status

        # Return most recent status update.
        return self._status


    #=========================================================================
    def is_active( self ):
        """
        Check to see if the worker is actively processing its task.

        @return True if the worker is active, otherwise False
        """
        return self._state == self.RUNNING


    #=========================================================================
    def start( self ):
        """
        Start executing the task.
        """

        # Change state to running.
        self._state = self.RUNNING

        # Use parent implementation to start the process.
        super( Worker, self ).start()


    #=========================================================================
    def stop( self ):
        """
        Stop executing the task.
        """

        # See if the task is currently in the running state.
        if self._state == self.RUNNING:

            # Send abort command to task.
            self._command_queue.put_nowait( ABORT_COMMAND )

        # Change state to stopping.
        self._state = self.STOPPING


#=============================================================================
def worker( command_queue, status_queue, descriptor ):
    """
    Function to execute as a worker process.

    @param command_queue IPC command queue from parent process
    @param status_queue  IPC status queue to parent process
    @param descriptor    Routine descriptor dictionary
    """

    # Set up a watchdog timer.
    dog = watchdog.Timer()

    # Create the routine object according to the descriptor.
    rtn = routine.create( descriptor[ 'name' ], descriptor[ 'arguments' ] )

    # Initialize the task's routine.
    #   Some routines will initialize here and start processing later.
    #   Some routines will block here until complete.
    #   Some routines won't implement this.
    try:
        rtn.initialize()
    except NotImplementedError:
        pass

    # Loop until the task reports completion.
    while rtn.is_done() == False:

        # Check the watchdog timer for a timeout after a stuck abort.
        if dog.check() == False:
            break

        # Check for any pending command messages.
        try:
            command = command_queue.get_nowait()
        except Queue.Empty:
            pass
        else:

            # Check for an abort command.
            if command == ABORT_COMMAND:

                # Try to abort the task.
                try:
                    rtn.abort()

                # Not supported, just stop processing.
                except NotImplementedError:
                    break

                # Start a timer to make sure we abort the process.
                else:
                    dog.start()

        # Spend time executing task.
        #   Some routines will quickly update status here.
        #   Some routines will block here until complete.
        #   Some routines won't implement this.
        try:
            rtn.process()
        except NotImplementedError:
            pass

        # Send status and progress to manager.
        try:
            status_queue.put_nowait( rtn.report )
        except Queue.Full:
            pass

