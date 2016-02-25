#=============================================================================
#
# Application Routine Interface
#
#=============================================================================

"""
Application Routine Interface
=============================

This module should be used to implement new task execution routines.
Semantically, a "routine" is the object a worker creates and manipulates to
execute long-running code or programs.
"""


import inspect

import data


#=============================================================================
class Argument( object ):
    """
    Manages a single argument given to a routine.
    """


    #=========================================================================
    def __init__(
        self,
        name,
        default  = None,
        required = False,
        ahelp    = None,
        atype    = None
    ):
        """
        Initializes an Argument object.

        @param name     The name of the argument
        @param default  The default value of the argument when not given
        @param required Specify to require this argument's presence
        @param ahelp    A helpful description of the argument
        @param atype    The expected type (if a default is not given)
        """
        self.name     = name
        self.default  = default
        self.required = required
        self.ahelp    = ahelp
        if atype is None:
            self.atype = type( self.default )
        else:
            self.atype = self.atype


#=============================================================================
class NotSupported( NotImplementedError ):
    """
    Exception raised by methods that are not supported by the current task
    instance.
    """


    #=========================================================================
    def __str__( self ):
        """
        Converts the exception object to a string representation.
        @return A string describing the exception
        """

        # Return a generic message.
        return 'Method not supported by this object.'


#=============================================================================
class Report( data.Data ):
    """
    The object sent to the worker when reporting the status and progress of
    a task.
    """


    #=========================================================================
    ERROR   = -1 # task encountered an error
    INIT    = 0  # task is initialized
    RUNNING = 1  # task is executing as normal
    DONE    = 2  # task is done executing


    #=========================================================================
    STATES = ( 'initialized', 'running', 'done', 'error' )


    #=========================================================================
    _fields = [
        ( 'status',   INIT ), # Current task status (ERROR|INIT|RUNNING|DONE)
        ( 'progress',  0.0 ), # Current task progress (0.0 to 1.0)
        ( 'message',  None )  # User-friendly message about progress (string)
    ]


    #=========================================================================
    def is_done( self ):
        """
        Informs interested parties if the task has completed.

        @return True when task has finished executing
        """

        # Produce a Boolean value for the done state.
        return self.status == self.DONE


#=============================================================================
class Routine( object ):
    """
    Object created and used by a worker process to start and monitor a task.
    Adding a new task interface requires implementing a child of this class.

    Child classes may implement the following methods:

    | Method       | When it is called                             |
    | ------------ | --------------------------------------------- |
    | `abort`      | Called to stop the task before completion     |
    | `initialize` | Called to initialize or start the task        |
    | `process`    | Called iteratively until the task is complete |

    All methods must return a `Report` object describing its status.

    Child classes specify a list of arguments they can accept for customizing
    per-task execution.  This is done by defining a class attribute
    `_arguments` as a list of tuples and dictionaries.  Each tuple is treated
    as positional arguments to the `Argument` initializer.  Each dictionary is
    treated as keyword arguments to the `Argument` initializer.
    """


    #=========================================================================
    _arguments = None


    #=========================================================================
    def __init__( self, *args, **kwargs ):
        """
        Initializes a Routine instance.

        @param *args    Initial argument values by position
        @param **kwargs Initial argument values by keyword
        """

        # Initialize object state.
        self.arguments = {}
        self._argspecs = []

        # Make sure there are declared arguments.
        if self._arguments is not None:

            # Create argument specifiers.
            for argument in self._arguments:
                if isinstance( argument, ( tuple, list ) ):
                    self._argspecs.append( Argument( *argument ) )
                elif isinstance( argument, dict ):
                    self._argspecs.append( Argument( **argument ) )

            # Set initial argument values.
            for index, value in enumerate( args ):
                self.arguments[ self._argspecs[ index ].name ] = value
            for key, value in kwargs.items():
                self.arguments[ key ] = value


    #=========================================================================
    @classmethod
    def gethelp( cls ):
        """
        Retrieves any helpful information that should be sent to the user.

        @return The docstring for the inheriting routine's class
        """

        # No need to provide the base class' docstring.
        if cls is Routine:
            return '(Task description unavailable.)'

        # Provide the inheriting class' docstring.
        return inspect.getdoc( cls )


    #=========================================================================
    def abort( self ):
        """
        Stops the execution of this task before completion.

        @return              A Report describing the routine's state
        @throws NotSupported Descendant class does not support this method
        """

        raise NotSupported()


    #=========================================================================
    def initialize( self ):
        """
        Initializes or starts the execution of this task.

        @return              A Report describing the routine's state
        @throws NotSupported Descendant class does not support this method
        """

        raise NotSupported()


    #=========================================================================
    def process( self ):
        """
        Called iteratively until the task reports completion.

        @return              A Report describing the routine's state
        @throws NotSupported Descendant class does not support this method
        """

        raise NotSupported()

