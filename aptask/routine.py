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
the routine makes "significant" progress, it should update the provided
`.report` attribute, return, and wait for the next invocation of the method.

### Reporting

Subclasses of Routine should report status, progress, and any user-targeted
messages in the provided `.report` attribute.  This attribute is monitored for
changes in the routine while it is executed.  Changing its `status` attribute
will inform the task scheduler if your routine has started successfully, is
making progress, or is complete.

Additionally, the `.report` may be updated using the following simple values.
These values will automatically cause status and progress changes in the
routine.

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

#### `str` or Serializable Values

Values that are strings or can be serialized into strings will indicate that
the routine has completed successfully.  The string is sent as feedback in the
report, so it may contain helpful information for users of the routine.

"""


import glob
import importlib
import inspect
import os
import sys

import data


#=============================================================================
def create( name, arguments = None ):
    """
    Creates Routine objects using the name and supplied arguments.

    Note: This assumes the "routines" directory is already in Python's path.

    @param name      The module name of the routine
    @param arguments The list of arguments to pass to the routine
    """

    # Default the arguments list.
    if arguments is None:
        arguments = []

    # Attempt to import the routine's module.
    try:
        module = importlib.import_module( name )
    except ImportError:
        raise RuntimeError( 'Invalid routine module "{}"'.format( name ) )

    # Look for modules with a routine function.
    funcref = getattr( module, 'routine', None )
    if ( funcref is not None ) and callable( funcref ):

        # Create the entry-point routine instance.
        return RoutineEntry( funcref, *arguments )

    # Look for modules with a Routine class.
    classref = getattr( module, 'Routine', None )
    if ( classref is not None ) and issubclass( classref, Routine ):

        # Create the routine instance.
        return classref( *arguments )

    # Requested module does not support the API.
    raise RuntimeError( 'Invalid routine module "{}"'.format( name ) )


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
def get_index( directory ):
    """
    Retrieves a list of valid routine implementations in the given directory.

    @param directory The directory to search
    @return          A list of dictionaries describing each routine
    """

    # Check for directory in Python's path.
    if directory not in sys.path:
        sys.path.insert( 0, directory )

    # Initialize the list of routines.
    index = []

    # Get a list of all Python modules in the given directory.
    modules = glob.glob( directory + '/*.py' )

    # Scan each Python module.
    for modfile in modules:

        # Derive module name from file name.
        modname = os.path.basename( modfile )[ : -3 ]

        # Import the module by name.
        # ZIH - protect against modules with invalid code
        module = importlib.import_module( modname )

        # Retrieve list of symbols in the module.
        symbols = dir( module )

        # Look for a function named "routine."
        if 'routine' in symbols:

            # Get a reference to the apparent function.
            funcref = getattr( module, 'routine' )

            # Ensure this is a function.
            if callable( funcref ):

                # Create a temporary routine object to interrogate the
                # function.
                rtn = RoutineEntry( funcref )

                # Append routine description dictionary to list.
                index.append(
                    {
                        'name'      : modname,
                        'arguments' : rtn.get_args(),
                        'help'      : rtn.get_help()
                    }
                )

        # Look for a class named "Routine."
        if 'Routine' in symbols:

            # Get reference to the apparent class.
            classref = getattr( module, 'Routine' )

            # Ensure this is a Routine class.
            if issubclass( classref, Routine ):

                # Append routine description dictionary to list.
                index.append(
                    {
                        'name'      : modname,
                        'arguments' : classref.get_args(),
                        'help'      : classref.get_help()
                    }
                )

    # Return list of available routines.
    return index


#=============================================================================
def update( report, result ):
    """
    Updates a given report instance with the result of a routine method.
    """

    # Simple, shell-like results.
    if type( result ) is int:
        report.progress = 1.0
        if result < 0:
            report.status = report.ERROR
        else:
            report.status = report.DONE

    # Execution progress results.
    elif type( result ) is float:
        if result < 0.0:
            report.status = report.ERROR
            result = 1.0
        elif result >= 1.0:
            report.status = report.DONE
            result = 1.0
        elif result == 0.0:
            report.status = report.INIT
        else:
            report.status = report.RUNNING
        report.progress = result

    # String results.
    elif isinstance( result, basestring ):
        report.progress = 1.0
        report.status   = report.DONE
        report.message  = result

    # Formal report results.
    elif isinstance( result, Report ):
        report.__dict__.update( result.__dict__ )

    # Any other results.
    else:
        report.progress = 1.0
        report.status   = report.DONE
        report.message  = str( result )


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
    # Bind the `update()` function to the class.
    update = update


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
        self.report    = Report()

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
    def abort( self ):
        """
        Stops the execution of this task before completion.

        @throws NotImplementedError Subclass does not support this method
        """
        raise NotImplementedError()


    #=========================================================================
    @classmethod
    def get_args( cls ):
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
    def get_help( cls ):
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
    def get_status( self ):
        """
        Gets the routine's current status.

        @return The routine's current status value
        """
        return self.report.status


    #=========================================================================
    def initialize( self ):
        """
        Initializes or starts the execution of this task.

        @throws NotImplementedError Subclass does not support this method
        """
        raise NotImplementedError()


    #=========================================================================
    def is_done( self ):
        """
        Interface to see if the routine is in a done state.
        """
        return self.report.status == self.report.DONE


    #=========================================================================
    def process( self ):
        """
        Called iteratively until the task reports completion.

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
        self._function = function
        self._iterator = None


    #=========================================================================
    def abort( self ):
        """
        Prevents further execution of the routine (if possible).
        """

        # Set the done status in the report.
        self.report.status = Report.DONE


    #=========================================================================
    def get_args( self ):
        """
        Retrieves the routine's argument specification.
        """

        # Check for declared arguments.
        if self._arguments is None:
            return []

        # Return a list of dictionaries describing the arguments.
        return [ { 'name' : n, 'default' : d } for n, d in self._arguments ]


    #=========================================================================
    def get_help( self ):
        """
        Retrieves the routine's docstring.
        """

        # Provide the function's docstring.
        return inspect.getdoc( self._function )


    #=========================================================================
    def initialize( self ):
        """
        Initializes the routine iterator.
        """

        # Construct positional argument list for declared arguments.
        args = []
        if self._arguments is not None:
            for name, default in self._arguments:
                args.append( self.arguments[ name ] )

        # Create the iterable object for this routine.
        self._iterator = self._function( *args )

        # Execute the routine once to allow it to initialize.
        self.process()


    #=========================================================================
    def process( self ):
        """
        Provides iterative execution of the routine.
        """

        # Check to see if the routine was aborted or otherwise terminated.
        if self.report.status == self.report.DONE:
            return

        # Execute the next iteration of the routine.
        try:
            result = self._iterator.next()
        except StopIteration:
            result = 0

        # Update the report.
        self.report.update( result )


