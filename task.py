#!/usr/bin/env python

"""
User Task Interface

This module should be used to implement new task execution drivers.
Semantically, a task is the object a worker creates and manipulates to execute
long-running code or programs.
"""


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
class Report( object ):
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
    def __init__( self ):
        """
        Constructor.
        """

        self.message  = None
        self.progress = 0.0
        self.status   = self.INIT


    #=========================================================================
    def __str__( self ):
        """
        String casting.
        """

        return self.message


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
    These three methods must all return a Report object.
    """


    #=========================================================================
    def __init__( self, arguments = None ):
        """
        Constructor.
        """

        self.arguments = arguments
        self.report    = Report()


    #=========================================================================
    @staticmethod
    def getargs():
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


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """



    # return success
    return 0

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

