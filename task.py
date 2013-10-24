#!/usr/bin/env python

"""
User Task Interface

This module should be used to implement new task execution drivers.
Semantically, a task is the object a worker creates and manipulates to execute
long-running code or programs.
"""


import inspect

import data


#=============================================================================
class NotSupported( NotImplementedError ):
    """
    Exception raised by methods that are not supported by the current task
    instance.
    """


    #=========================================================================
    def __str__( self ):
        """
        Convert to string representation.
        @return         A string describing the exception
        """

        return 'Method not supported by this object.'


#=============================================================================
class Report( data.Data ):
    """
    The object sent to the worker when reporting the status and progress of
    a task.
    """


    #=========================================================================
    ERROR   = -1                    # task encountered an error
    INIT    = 0                     # task is initialized
    RUNNING = 1                     # task is executing as normal
    DONE    = 2                     # task is done executing


    #=========================================================================
    status_strings = ( 'initialized', 'running', 'done' )


    #=========================================================================
    def __init__( self, status = INIT, progress = 0.0, message = None ):
        """
        Constructor.
        @param status   Current task status (ERROR, INIT, RUNNING, DONE)
        @param progress Current task progress (0.0 to 1.0)
        @param message  User-friendly message about progress (string)
        """

        # load arguments into object state
        self.super_init( vars() )


    #=========================================================================
    def is_done( self ):
        """
        Informs interested parties if the task has completed.
        @return         True when task has finished executing
        """

        return self.status == self.DONE


#=============================================================================
class Task( object ):
    """
    Object created and used by a worker process to start and monitor a task.
    Adding a new task interface requires implementing a child of this class.
    Child classes may implement the following methods:
        abort           Called to stop the task before completion
        getargs         Used to describe acceptable arguments
        initialize      Called to initialize or start the task
        process         Called iteratively until the task is complete
    abort, initialize, and process must all return a Report object.
    """


    #=========================================================================
    def __init__( self, arguments = None ):
        """
        Constructor.
        @param arguments
                        Argument values requested for task execution
        """

        self.arguments       = None
        self.report          = Report()
        self.valid_arguments = self._load_args( arguments )


    #=========================================================================
    @classmethod
    def getargs( cls ):
        """
        Retrieves the argument list for this task.
        An argument list is a list of dicts.  Each dict describes an argument
        with the following keys:
            name        Binding name
            default     Default value if not supplied (implies type)
            required    True if this must always be specified
            help        Brief description of the purpose of this argument
            type        Argument type (if no default is given)
                        (int|float|str) later: (list|dict)
        """

        return []


    #=========================================================================
    @classmethod
    def gethelp( cls ):
        """
        Retrieves any helpful information that should be sent to the user.
        """

        if cls is Task:
            return '(Task description unavailable.)'

        return inspect.getdoc( cls )


    #=========================================================================
    def abort( self ):
        """
        Stops the execution of this task before completion.
        @throws NotSupported
                        Descendant class does not support this method
        """

        raise NotSupported()


    #=========================================================================
    def initialize( self ):
        """
        Initializes or starts the execution of this task.
        @throws NotSupported
                        Descendant class does not support this method
        """

        raise NotSupported()


    #=========================================================================
    def process( self ):
        """
        Called iteratively until the task reports completion.
        @return         Task progress from 0.0 (none) to 1.0 (done)
        @throws NotSupported
                        Descendant class does not support this method
        """

        raise NotSupported()


    #=========================================================================
    def _load_args( self, args ):
        """
        Load given arguments into object state.
        @param args     List or dict of requested argument values
        """

        # flag to indicate valid argument input
        result = True

        # build a list of arguments expected by this task driver
        self._arg_list = self.getargs()

        # build a lookup table of known arguments
        self._arg_table = dict( ( a[ 'name' ], a ) for a in self._arg_list )

        # create a dictionary to keep the argument values and set defaults
        self.arguments = dict(
            ( a[ 'name' ], a[ 'default' ] )
                for a in self._arg_list
                    if 'default' in a
        )

        # handle dictionary input
        if type( args ) is dict:

            # use our known arguments to extract values into the object
            for key, arg in self._arg_table.items():

                # see if the input specified this argument
                if key in args:
                    if self._load_arg( key, args[ key ] ) == False:
                        result = False

        # handle list input
        elif type( args ) is list:

            # argument value list index
            index = 0

            # use our known arguments to extract values into the object
            for key, arg in self._arg_table.items():

                # see if the input specified this argument
                if index < len( args ):
                    if self._load_arg( key, args[ index ] ) == False:
                        result = False
                    index += 1

        # make sure all required arguments were specified
        reqs = [ a[ 'name' ] for a in self._arg_list if 'required' in a ]
        keys = self.arguments.keys()

        # the difference between two sets should be an empty set if the entire
        #   first set is a subset of the second set
        num_diff = len( set( reqs ) - set( keys ) )
        if num_diff != 0:
            result = False

        # return status of argument loading
        return result


    #=========================================================================
    def _load_arg( self, key, value ):
        """
        Load a given argument into object state.
        @param key      Name of argument to load
        @param value    Value to load
        @return         True if successfully loaded
        """

        # check key against table of arguments
        if key not in self._arg_table:
            return False

        # reference the argument specifier
        spec = self._arg_table[ key ]

        # determine argument type
        if 'default' in spec:
            type_name = type( spec[ 'default' ] ).__name__
        elif 'type' in spec:
            type_name = spec[ 'type' ]
        else:
            type_name = 'str'

        # pull name of type of value
        value_type_name = type( value ).__name__

        # validate argument type
        if value_type_name != type_name:
            return False

        # store value in object state
        self.arguments[ key ] = value
        return True


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    import tasks.devtask
    t = tasks.devtask.DevTask()
    t._load_args( {} )
    print t.arguments
    #print t.gethelp()
    #print Task.gethelp()

    # return success
    return 0

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

