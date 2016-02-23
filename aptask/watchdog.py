#=============================================================================
#
# Watchdog Timer
#
#=============================================================================


"""
Watchdog Timer
"""


import time


#=============================================================================
class Timer( object ):
    """
    Encapsulates data needed to monitor things that could time out.
    """


    #=========================================================================
    def __init__( self, timeout = 60.0 ):
        """
        Constructor.
        @param timeout  The time to consider an activity timed out (seconds)
        """

        self.timeout = timeout
        self.alive   = None


    #=========================================================================
    def check( self ):
        """
        Check the watchdog to see if the activity has timed out.
        @return         False if timed out, True if still okay
        """

        if ( self.alive is not None ) \
            and ( time.time() > ( self.alive + self.timeout ) ):
            return False
        return True


    #=========================================================================
    def service( self ):
        """
        Service the watchdog timer to indicate activity is still progressing.
        """

        self.alive = time.time()


    #=========================================================================
    def start( self ):
        """
        Start the watchdog timer.
        """

        self.service()

