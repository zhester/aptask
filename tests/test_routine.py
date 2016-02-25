#=============================================================================
#
# routine Module Unit Tests
#
#=============================================================================

"""
routine Module Unit Tests
=========================
"""


import unittest


import aptask.routine


__version__ = '0.0.0'



#=============================================================================
class _SubRoutine( aptask.data.Data ):
    """
    Subclass of the Routine class used for testing.
    """

    _arguments = [
        ( 'a', 1 ),
        ( 'b', 2.22 ),
        ( 'c', 'hello' ),
        ( 'd', None )
    ]


#=============================================================================
class TestRoutine( unittest.TestCase ):
    """
    Tests the Routine class in the routine module
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs test setup.
        """
        pass


    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """
        routine = aptask.routine.Routine()

