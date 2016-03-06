#=============================================================================
#
# Task Execution Context Information
#
#=============================================================================

"""
Task Execution Context Information
==================================

This module provides the core objects used to centralize all the information
needed to enqueue and schedule tasks for execution.  A _task_ is defined as a
unique execution of a _routine_ to carry out a requested job.
"""


#=============================================================================
class Context( object ):
    """
    The Context object is responsible for providing a consistent interface to
    all the information necessary to monitor and schedule a requested routine.
    A new Context instance is created every time a job is requested.
    """


    #=========================================================================
    # Queue processing states
    ERROR    = -1 # Task encountered an error, and can not proceed
    INIT     =  0 # Object/state initialized
    ENQUEUED =  1 # Task is waiting in queue
    WAITING  =  2 # Task is waiting for a dependent task to complete
    RUNNING  =  3 # Task is currently running the routine
    STOPPING =  4 # Task is currently trying to stop the routine
    DONE     =  5 # Task has finished running, results available
    DEQUEUED =  6 # Task no longer belongs to any queue


    #=========================================================================
    # Queue scheduling priorities
    PRI_NEXT   = 0  # Higher insertion priority
    PRI_NORMAL = 1  # Normal insertion priority
    PRI_LAST   = 2  # Lower insertion priority


    #=========================================================================
    # Queue priority strings (indexed by state value)
    states = ( 'NEXT', 'NORMAL', 'LAST' )


    #=========================================================================
    # Queue state strings (indexed by state value)
    states = (
        'initialized', 'enqueued', 'waiting', 'running',
        'stopping', 'done', 'error'
    )


    #=========================================================================
    def __init__(
        self,
        ident,                 # Unique task execution identifier
        descriptor,            # Routine descriptor dictionary
        priority = PRI_NORMAL, # Requested priority
        group    = None,       # Request namespace group
        jobid    = None,       # Requested job identifer
        waitfor  = None        # List of job IDs that must complete first
    ):
        """
        Initializes a Context instance.
        """

        # Initialize object state.
        self.id         = ident
        self.state      = self.INIT
        self.descriptor = descriptor
        self.result     = None

        # Initialize the optional/requested object state.
        self.group    = group
        self.priority = priority
        self.jobid    = jobid
        self.waitfor  = []

