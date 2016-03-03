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
class DependsError( RuntimeError ):
    """
    Exception raised when a dependency violation would result from the
    requested action.
    """
    pass


#=============================================================================
class Empty( StopIteration ):
    """
    Exception used to indicate an empty queue state when an item is requested.
    """
    pass


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

        # List of ready-to-run task context objects in the queue in order of
        # execution priority
        self._ready = []

        # List of task context objects that are running or have completed
        self._tasks = []

        # Lookup tables
        self._tables = {
            'taskid' : {},
            'jobid'  : {},
            'wait'   : {}
        }

        # The next unique ID to assign to a task
        self._next_id = 1


    #=========================================================================
    def create_task( self, descriptor, *args, **kwargs ):
        """
        Creates a new task context object and automatically schedules it for
        execution.  All keyword/defaulted arguments are passed as-is to the
        Task object initializer.  It is recommended to only use this method as
        the factory for generating new task contexts.

        @param descriptor The routine descriptor used for this task
        @param args       @see task.Context.__init__()
        @param kwargs     @see task.Context.__init__()
        @return           A reference to the context object that was
                          created/enqueued
        """

        # Create a new task scheduling Context.
        context = task.Context( self._next_id, descriptor, *args, **kwargs )

        # Enqueue this task context.
        self.enqueue( context )

        # Increment the next task ID.
        self._next_id += 1

        # Return the context reference.
        return context


    #=========================================================================
    def enqueue( self, task_context ):
        """
        Enqueues a new task context object for scheduling.

        @param task_context The task Context object to enqueue
        """
        ### ZIH
        # perform a circular dependency check
        # add to ready queue (schedule priority)
        # add reference to lookup tables

        # Transition the context's state.
        task_context.state = context.ENQUEUED


    #=========================================================================
    def next( self ):
        """
        Retrieves a reference to the next task object that is ready to begin
        execution.

        @return A task Context object that is allowed to start execution
        @throws Empty if there are no tasks in the ready queue
        """

        # Make sure there is at least one task in the ready queue.
        if len( self._ready ) == 0:
            raise Empty()

        # Remove the next task context from the ready queue.
        context = self._ready.pop( 0 )

        # Transition the context's state.
        context.state = context.RUNNING

        # Put the task context in the running/done queue.
        self._tasks.append( context )

        # Return the reference to this task context.
        return context


    #=========================================================================
    def remove( self, taskid ):
        """
        Removes a task from the scheduler.

        @param taskid Task ID of the task to remove from the scheduler
        @return       A reference to the task Context that was removed
        @throws       ValueError if the task ID is not in any queue
        @throws       DependsError if the task has dependencies
        @throws       RuntimeError if the scheduler encountered a problem
        """

        # Reference the task context reference lookup tables.
        jobs  = self._tables[ 'jobid' ]
        tasks = self._tables[ 'taskid' ]
        waits = self._tables[ 'wait' ]

        # Check task ID.
        if taskid not in tasks:
            raise ValueError( 'Invalid/unknown task ID: {}'.format( taskid ) )

        # Reference the task context object.
        context = tasks[ taskid ]

        # Check ready queue for the task.
        if context in self._ready:
            if context.id in waits:
                raise DependsError( 'Unable to remove task with dependents.' )
            self._ready.remove( context )

        # Check task queue for the task.
        elif context in self._tasks:
            self._ready.remove( context )

        # Defensive else
        else:
            raise RuntimeError( 'Scheduler integrity: task missing.' )

        # Remove from lookup tables.
        if ( context.jobid is not None ) and ( context.jobid in jobs ):
            del self._tables[ 'jobid' ][ context.jobid ]
        if context.id in waits:
            del self._tables[ 'wait' ][ context.id ]
        del self._tables[ 'taskid' ][ context.id ]

        # Transition the context state.
        context.state = context.DEQUEUED

        # Return a reference to the task context.
        return context


    #=========================================================================
    def update( self, taskid = None ):
        """
        Requests an update of task execution state across all tasks in the
        scheduler, or informs the scheduler of an update in a task's execution
        status.

        @param taskid Optional task ID of which to update
        """
        ### ZIH
        pass


    #=========================================================================
    def _rescan( self ):
        """
        Performs a complete scan of the ready queue checking each scheduled
        task for updates.  This has the potential to change scheduling
        priorities based on new information.
        """
        ### ZIH
        pass

