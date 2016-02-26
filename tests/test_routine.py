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
def _testentry( a, b = 2.22, c = 'hello' ):
    '_test_entry_point_function_'
    yield 0.0
    loops = a if type( a ) is int else 3
    for loop in range( 1, loops + 1 ):
        yield loop / loops


#=============================================================================
class _SubRoutine( aptask.routine.Routine ):
    '_test_sub_routine_class_'
    _arguments = [
        ( 'a', 1 ),
        ( 'b', 2.22 ),
        ( 'c', 'hello' ),
        ( 'd', None )
    ]
    def abort( self ):
        return 0
    def initialize( self ):
        return 0
    def process( self ):
        return 0


#=============================================================================
class Test_get_function_arguments( unittest.TestCase ):
    """
    Tests the get_function_arguments() module function
    """

    #=========================================================================
    def test_gfa( self ):
        """
        Tests the get_function_arguments() module function
        """

        # Test functions without arguments.
        def _testempty():
            return
        actual   = aptask.routine.get_function_arguments( _testempty )
        expected = []
        self.assertListEqual( expected, actual )

        # Test functions with all optional arguments.
        def _testopts( a = 1, b = 2 ):
            return
        actual   = aptask.routine.get_function_arguments( _testopts )
        expected = [ ( 'a', 1 ), ( 'b', 2 ) ]
        self.assertListEqual( expected, actual )

        # Test functions with all required arguments.
        def _testreqs( a, b ):
            return
        actual   = aptask.routine.get_function_arguments( _testreqs )
        expected = [ ( 'a', '__required__' ), ( 'b', '__required__' ) ]
        self.assertListEqual( expected, actual )

        # Test functions with some required arguments.
        actual   = aptask.routine.get_function_arguments( _testentry )
        expected = [
            ( 'a', '__required__' ),
            ( 'b', 2.22 ),
            ( 'c', 'hello' )
        ]
        self.assertListEqual( expected, actual )


#=============================================================================
class TestReport( unittest.TestCase ):
    """
    Tests the Report class in the routine module
    """

    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """
        report = aptask.routine.Report()
        self.assertEqual( report.status, report.INIT )
        self.assertEqual( report.progress, 0.0 )
        self.assertIsNone( report.message )


    #=========================================================================
    def test_is_done( self ):
        """
        Tests the is_done() Report method.
        """
        report = aptask.routine.Report()
        self.assertFalse( report.is_done() )
        report.status = report.DONE
        self.assertTrue( report.is_done() )


#=============================================================================
class TestRoutine( unittest.TestCase ):
    """
    Tests the Routine class in the routine module
    """

    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """

        # Base class has no arguments.
        routine = aptask.routine.Routine()
        self.assertDictEqual( routine.arguments, {} )

        # Example subclass has arguments with defaults.
        routine = _SubRoutine()
        names   = [ a[ 0 ] for a in _SubRoutine._arguments ]
        for index, name in enumerate( names ):
            self.assertIn( name, routine.arguments )
            self.assertEqual(
                _SubRoutine._arguments[ index ][ 1 ],
                routine.arguments[ name ]
            )


    #=========================================================================
    def test_getargs( self ):
        """
        Tests the getargs() Routine method.
        """

        # Create a routine without arguments.
        routine = aptask.routine.Routine()
        self.assertListEqual( [], routine.getargs() )

        # Create a routine with arguments.
        routine  = _SubRoutine()
        expected = [
            {
                'name'    : _SubRoutine._arguments[ 0 ][ 0 ],
                'default' : _SubRoutine._arguments[ 0 ][ 1 ]
            },
            {
                'name'    : _SubRoutine._arguments[ 1 ][ 0 ],
                'default' : _SubRoutine._arguments[ 1 ][ 1 ]
            },
            {
                'name'    : _SubRoutine._arguments[ 2 ][ 0 ],
                'default' : _SubRoutine._arguments[ 2 ][ 1 ]
            },
            {
                'name'    : _SubRoutine._arguments[ 3 ][ 0 ],
                'default' : _SubRoutine._arguments[ 3 ][ 1 ]
            }
        ]
        self.assertListEqual( expected, routine.getargs() )


    #=========================================================================
    def test_gethelp( self ):
        """
        Tests the gethelp() Routine method.
        """

        # Create a routine with a simple docstring.
        routine = _SubRoutine()
        self.assertEqual( '_test_sub_routine_class_', routine.gethelp() )


    #=========================================================================
    def test_abort( self ):
        """
        Tests the abort() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()
        self.assertRaises( NotImplementedError, routine.abort )

        # Create a routine subclass.
        routine = _SubRoutine()
        self.assertEqual( 0, routine.abort() )


    #=========================================================================
    def test_initialize( self ):
        """
        Tests the initialize() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()
        self.assertRaises( NotImplementedError, routine.initialize )

        # Create a routine subclass.
        routine = _SubRoutine()
        self.assertEqual( 0, routine.initialize() )


    #=========================================================================
    def test_process( self ):
        """
        Tests the process() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()
        self.assertRaises( NotImplementedError, routine.process )

        # Create a routine subclass.
        routine = _SubRoutine()
        self.assertEqual( 0, routine.process() )


#=============================================================================
class TestRoutineEntry( unittest.TestCase ):
    """
    Tests the RoutineEntry class in the routine module
    """

    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        ### TODO

    ### TODO
    # abort
    # gethelp
    # initialize
    # process


