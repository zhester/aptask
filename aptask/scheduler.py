#=============================================================================
#
# Task Execution Queue and Scheduling
#
# ZIH - this should completely replace raqueue module, and simplify the
# manager module
#
# The queue has three modes of insertion based on the priority of the
# requested task.  The user may request NORMAL, NEXT, or LAST insertion.
#
# NORMAL insertion is the default and attempts to place the requested task
# after all exsting tasks that are waiting to execute.
#
# NEXT insertion allows the user to schedule new tasks ahead of tasks that
# were scheduled with NORMAL priority.
#
# LAST insertion allows the user to schedule a low-priority task.  Tasks with
# LAST priority will only execute after all other priorities have been
# started.
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

        # Task ID lookup table
        self._taskids = {}

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

        # Check for a task that needs to wait for other tasks.
        if len( task_context.waitfor ) > 0:
            ### ZIH
            pass

        # Check for a task that might have dependencies.
        if task_context.jobid is not None:
            ### ZIH
            pass

        # Add task to ready queue.
        ### ZIH
        # .priority, .group, .jobid, .waitfor

        # Add this task reference to lookup tables.
        self._taskids[ task_context.id ] = task_context

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

        # Scan tasks in the ready queue.
        for index, task in enumerate( self._ready ):

            # Look for queued tasks that are not currently blocked.
            if self._blocked( task ) == False:

                # Remove this task from the ready queue.
                context = self._ready.pop( index )

                # Transition the context's state.
                context.state = context.RUNNING

                # Put the task context in the running/done queue.
                self._tasks.append( context )

                # Return the reference to this task context.
                return context

        # No tasks in the ready queue are ready for execution.
        raise Empty()


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

        # Check task ID.
        if taskid not in self._taskids:
            raise ValueError( 'Invalid/unknown task ID: {}'.format( taskid ) )

        # Reference the task context object.
        context = self._taskids[ taskid ]

        # Check ready queue for the task.
        if context in self._ready:
            self._ready.remove( context )

        # Check task queue for the task.
        elif context in self._tasks:
            self._ready.remove( context )

        # Defensive else
        else:
            raise RuntimeError( 'Scheduler integrity: task missing.' )

        # Remove from lookup table.
        del self._taskids[ context.id ]

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
    def _blocked( self, context ):
        """
        Tests if a task in the ready queue is waiting for another task to
        finish.

        @param taskid The task context object to test
        @return       True if the task must wait, otherwise False
        """

        # Check if this task depends on other tasks.
        if len( context.waitfor ) == 0:

            # No dependencies, task is free to run now.
            return False

        # Scan the task list for jobs that must complete first.
        for wait in context.waitfor:

            # ZIH - refactoring to use new group.Manager

            # The given task must wait.
            return True

        # The task is free to run now.
        return False


    #=========================================================================
    def _rescan( self ):
        """
        Performs a complete scan of the ready queue checking each scheduled
        task for updates.  This has the potential to change scheduling
        priorities based on new information.
        """
        ### ZIH
        pass


    #=========================================================================
    def _task_by_id( self, taskid ):
        """
        Retrieve any task context object given its ID.

        @param taskid    The ID of the task to fetch
        @return          The task context object with this ID
        @throws KeyError If the ID is not present in the scheduler
        description
        """

        # Catch invalid task IDs to produce a better exception message.
        if taskid not in self._taskids:
            raise KeyError( 'Unknown task ID: {}'.format( taskid ) )

        # Return the reference to the task context object.
        return self._taskids[ taskid ]

