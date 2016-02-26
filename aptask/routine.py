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

OOP Protocol
------------

The routine protocol defines the following methods that may be optionally
implemented by any class that needs to be used to provide task execution.  All
methods are optional for any routine, but defining no methods means your
routine will never be successfully executed.

### `abort`

Users and the scheduler may request "graceful" shutdown of a routine before it
has completed the task.  Defining this method allows routines to perform any
necessary cleanup.  If this method is not defined, the system will revert to
forcibly killing the process, and starting a new worker process.

### `initialize`

This method is called to initialize or start the routine.  The intent is to
place one-time initialization of the routine in this method.  However, it can
also be used to run the entirety of the routine.  In this secondary use, your
routine will be unable to report incremental progress.

### `process`

This method is successively called to allow the routine to make progress
towards its goal.  The method is (typically) called in a very tight loop which
means that the routine may arbitrate the granularity of progress updates.  If
the routine makes "significant" progress, it should return an update on that
progress, and wait for the next invocation of the method.

### Reporting

The routine protocol allows any method to return an integer, a float, a
string, or an instance of the Report class.

#### `float` Values

A typical minimal status can be given with a `float` value.  When the caller
receives a fractional number, it assumes that values between 0.0 and 1.0 are
reports on the progress of the routine.  The meanings of the various values
are as indicated below.

| Value         | Meaning                                       |
| ------------- | --------------------------------------------- |
| 0.0           | Routine is successfully initialized.          |
| 0.0 < v < 1.0 | Routine is making progress towards its goal.  |
| 1.0           | Routine has successfully finished processing. |
| v < 0.0       | Routine has encountered an error.             |
| v > 1.0       | Undefined/reserved for future use.            |

#### `int` Values

The caller will treat integer values similarly to a shell-style exit code.

| Value | Meaning                             |
| ----- | ----------------------------------- |
| 0     | Routine successfully completed.     |
| v > 0 | Routine encountered an error.       |
| v < 0 | Undefined/reserved for future user. |

#### `Report` Objects

The most formal reporting is done by using a `Report` object.  This object can
be used to report state, progress, and a message for clients.

"""


import inspect

import data


#=============================================================================
def get_function_arguments( function ):
    """
    Retrieves the list of function arguments of a given function for use in a
    Routine's argument specification list.

    @param function The reference to the function to query
    @return         A list of two-tuples describing the arguments
    """

    # Get argument specification for this function.
    argspec = inspect.getargspec( function )

    # Construct a list of two-tuples describing the arguments.
    arguments = []

    # Default values as a (mutable) list.
    if argspec.defaults is not None:
        defaults = list( argspec.defaults )
    else:
        defaults = []

    # Count the number of required arguments.
    num_required = len( argspec.args ) - len( defaults )

    # Iterate through the arguments in order.
    for index, name in enumerate( argspec.args ):

        # Check for arguments without a default.
        if index < num_required:
            default = '__required__'

        # This argument has a default value.
        else:
            default = defaults.pop( 0 )

        # Create the two-tuple entry for the argument.
        arguments.append( ( name, default ) )

    # Return the constructed list of arguments.
    return arguments


#=============================================================================
class Report( data.Data ):
    """
    The object sent to the worker when reporting the status and progress of
    a task.
    """


    #=========================================================================
    # Task execution states
    ERROR   = -1 # task encountered an error
    INIT    = 0  # task is initialized
    RUNNING = 1  # task is executing as normal
    DONE    = 2  # task is done executing


    #=========================================================================
    # Descriptive strings of task execution states (by sequence index)
    STATES = ( 'initialized', 'running', 'done', 'error' )


    #=========================================================================
    # List of fields to serialize in Report instances
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
    `_arguments` as a list of two-tuples specifying the name and default value
    of each argument.
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

        # Check for declared arguments.
        if self._arguments is not None:

            # Set default values for the routine's arguments.
            self.arguments.update( self._arguments )

            # Set initial argument values.
            for index, value in enumerate( args ):
                self.arguments[ self._arguments[ index ][ 0 ] ] = value
            for key, value in kwargs.items():
                self.arguments[ key ] = value


    #=========================================================================
    @classmethod
    def getargs( cls ):
        """
        Retrieves the routine's declared arguments.

        @return A list of dictionaries containing the name and default value
                of each argument for this routine
        """

        # Check for declared arguments.
        if cls._arguments is None:
            return []

        # Return a list of dictionaries describing the arguments.
        return [ { 'name' : n, 'default' : d } for n, d in cls._arguments ]


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

        @return                     Task progress, state, or report
        @throws NotImplementedError Subclass does not support this method
        """
        raise NotImplementedError()


    #=========================================================================
    def initialize( self ):
        """
        Initializes or starts the execution of this task.

        @return                     Task progress, state, or report
        @throws NotImplementedError Subclass does not support this method
        """
        raise NotImplementedError()


    #=========================================================================
    def process( self ):
        """
        Called iteratively until the task reports completion.

        @return                     Task progress, state, or report
        @throws NotImplementedError Subclass does not support this method
        """
        raise NotImplementedError()


#=============================================================================
class RoutineEntry( Routine ):
    """
    Implements the necessary Routine protocol to handle simplified
    entry-point-style routine modules.
    """


    #=========================================================================
    def __init__( self, function, *args, **kwargs ):
        """
        Initializes a RoutineEntry object.

        @param function The entry-point function reference
        @param *args    Initial argument values by position
        @param **kwargs Initial argument values by keyword
        """

        # Set the routine's argument specification.
        self._arguments = get_function_arguments( function )

        # Initialize the parent state.
        super( RoutineEntry, self ).__init__( *args, **kwargs )

        # Initialize object state.
        self.function = function
        self.iterator = None
        self.report   = Report()


    #=========================================================================
    def abort( self ):
        """
        Prevents further execution of the routine (if possible).

        @return Task (early) completion status
        """

        # Set the done status in the report.
        self.report.status = Report.DONE

        # Report done status.
        return self.report


    #=========================================================================
    def gethelp( self ):
        """
        Retrieves the routine's docstring.
        """

        # Provide the function's docstring.
        return inspect.getdoc( self.function )


    #=========================================================================
    def initialize( self ):
        """
        Initializes the routine iterator.

        @return Task progress, state, or report
        """

        # Construct positional argument list for declared arguments.
        args = []
        if self._arguments is not None:
            for name, default in self._arguments:
                args.append( self.arguments[ name ] )

        # Create the iterable object for this routine.
        self.iterator = self.function( *args )


    #=========================================================================
    def process( self ):
        """
        Provides iterative execution of the routine.

        @return Task progress, state, or report
        """

        # Check for early termination of the routine.
        if self.report.is_done() == True:
            return self.report

        # Check for natural termination of the routine.
        if self.report.progress >= 1.0:
            return self.report

        # Execute the next iteration of the routine.
        try:
            result = self.iterator.next()
        except StopIteration:
            result = 0

        # Update task state for simple routines.
        if type( result ) is int:
            if result < 0:
                self.report.status = Report.ERROR
            else:
                self.report.status = Report.DONE

        # Update task state for progress-reporting routines.
        elif type( result ) is float:
            if result < 0.0:
                self.report.status = Report.ERROR
            elif result >= 1.0:
                self.report.status = Report.DONE
            else:
                self.report.progress = result

        # Update task state for all other routines.
        else:
            self.report.status = Report.DONE
            if isinstance( result, basestring ):
                self.report.message = result

        # Report routine progress or state.
        return self.report

