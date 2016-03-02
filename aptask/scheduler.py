#=============================================================================
#
# Task Execution Queue and Scheduling
#
# ZIH - this should completely replace raqueue module, and simplify the
# manager module
#
#=============================================================================

"""
Task Execution Queue and Scheduling
===================================
"""


import task


#=============================================================================
class Schedule( object ):
    """
    Manages the task execution schedule.
    """


    #=========================================================================
    def __init__( self ):
        """
        Initializes a Schedule object.
        """

        # List of ready-to-run task objects in the queue in order of
        # execution priority
        self._ready = []

        # List of tasks objects that are running or have completed
        self._tasks = []

        # Lookup tables
        self._tables = {
            'taskid' : {},
            'jobid'  : {}
        }

        # The next unique ID to assign to a task
        self._next_id = 1


    #=========================================================================
    def create_task( self, *args, **kwargs ):
        """
        Creates a new task object and automatically schedules it for
        execution.  All arguments are passed as-is to the Task object
        initializer with the exception of the `ident` argument.  This argument
        is automatically determined within the scheduler.  Any `ident` passed
        to this method will be overwritten.

        @param @see task.Task.__init__()
        @return     A reference to the task object that was created/enqueued
        """
        ### ZIH
        pass


    #=========================================================================
    def enqueue( self, taskobj ):
        """
        Enqueues a new task object for scheduling.
        """
        ### ZIH
        pass


    #=========================================================================
    def next( self ):
        """
        Retrieves a reference to the next task object that is ready to begin
        execution.

        @return A task object to begin executing
        """
        ### ZIH
        pass


    #=========================================================================
    def remove( self, taskid ):
        """
        Removes a task from the scheduler.

        @param taskid Task ID to remove from scheduler
        """
        ### ZIH
        pass


    #=========================================================================
    def update( self, taskobj = None ):
        """
        Requests an update of task execution state across all tasks in the
        scheduler, or informs the scheduler of an update in a task's execution
        status.

        @param taskid Optional task ID of which to update
        """
        ### ZIH
        pass

