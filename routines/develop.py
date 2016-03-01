#=============================================================================
#
# Development Routine
#
#=============================================================================


"""
Development Routine
===================

This routine provides a template for developing other custom routines, as well
as a routine that can be used for synthetic testing and analysis.

See: aptask.routine for more complete documenation of the routine protocol.
"""


import time

import aptask.routine


__version__ = '0.0.0'


#=============================================================================
class Routine( aptask.routine.Routine ):
    """
    Project development and testing routine.
    """


    #=========================================================================
    # Specify the list of arguments to alter per-task execution behavior.
    # Each item in the list is a two-tuple with the following items:
    #
    #    ( name, default )
    #

    _arguments = [
        ( 'devarg',     42 ),
        ( 'abortwait',   0 ),
        ( 'initwait',    0 ),
        ( 'processwait', 0 )
    ]


    #=========================================================================
    def abort( self ):
        """
        Called when the routine needs to stop processing immediately.

        @return A Report object describing its status
        """

        # Sleep the specified amount before aborting.
        time.sleep( self.arguments[ 'abortwait' ] )

        # Report the task is done.
        self.report.status = aptask.routine.Report.DONE
        return self.report


    #=========================================================================
    def initialize( self ):
        """
        Initializes or starts the execution of this task.

        @return A Report describing the routine's state
        """

        # Create a report to report progress.
        self.report = aptask.routine.Report(
            message = '{} with devarg {}'.format(
                self.__class__.__name__,
                self.arguments[ 'devarg' ]
            )
        )

        # Sleep the specified amount before initializing.
        time.sleep( self.arguments[ 'initwait' ] )

        # Report the task is initialized.
        return self.report


    #=========================================================================
    def process( self ):
        """
        Called iteratively until the task reports completion.

        @return A Report describing the routine's state
        """

        # Check to see if this task considers itself complete.
        if self.report.progress >= 1.0:

            # Make sure the report is accurate.
            self.report.status = aptask.routine.Report.DONE

        # The task is still working.
        else:

            # Sleep the specified amount before continuing.
            time.sleep( self.arguments[ 'processwait' ] )

            # Indicate some progress has been made.
            self.report.progress += 0.1

            # Make sure the report is accurate.
            self.report.status = aptask.routine.Report.RUNNING

        # Report the current task status.
        return self.report

