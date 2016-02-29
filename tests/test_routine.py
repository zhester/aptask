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
class _SubRoutine( aptask.routine.Routine ):
    '_test_sub_routine_class_'
    _arguments = [
        ( 'a', 1 ),
        ( 'b', 2.22 ),
        ( 'c', 'hello' ),
        ( 'd', None )
    ]
    def __init__( self, *args, **kwargs ):
        super( _SubRoutine, self ).__init__( *args, **kwargs )
        self._abort_called      = 0
        self._initialize_called = 0
        self._process_called    = 0
    def abort( self ):
        self._abort_called += 1
    def initialize( self ):
        self._initialize_called += 1
    def process( self ):
        self._process_called += 1


#=============================================================================
class Test_get_function_arguments( unittest.TestCase ):
    """
    Tests the get_function_arguments() module function
    """


    #=========================================================================
    def test_get_function_arguments( self ):
        """
        Tests the get_function_arguments() module function
        """

        # Test functions without arguments.
        def _testnone():
            return
        actual   = aptask.routine.get_function_arguments( _testnone )
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
        def _testsome( a, b = 2.22, c = 'hello' ):
            return
        actual   = aptask.routine.get_function_arguments( _testsome )
        expected = [
            ( 'a', '__required__' ),
            ( 'b', 2.22 ),
            ( 'c', 'hello' )
        ]
        self.assertListEqual( expected, actual )


#=============================================================================
class Test_update( unittest.TestCase ):
    """
    Tests the update() module function
    """


    #=========================================================================
    def test_update( self ):
        """
        Tests the update() module function
        """

        # Create a report to update.
        report = aptask.routine.Report()

        # Check initial state.
        self.assertEqual( report.status, report.INIT )
        self.assertEqual( report.progress, 0.0 )
        self.assertIsNone( report.message )

        # Update using shell-style results.
        aptask.routine.update( report, 0 )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, 1 )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, -1 )
        self.assertEqual( report.status, report.ERROR )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )

        # Update using incremental progress results.
        aptask.routine.update( report, 0.0 )
        self.assertEqual( report.status, report.INIT )
        self.assertEqual( report.progress, 0.0 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, 0.3 )
        self.assertEqual( report.status, report.RUNNING )
        self.assertEqual( report.progress, 0.3 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, 1.0 )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, 2.0 )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )
        aptask.routine.update( report, -1.0 )
        self.assertEqual( report.status, report.ERROR )
        self.assertEqual( report.progress, 1.0 )
        self.assertIsNone( report.message )

        # Update using string progress results.
        aptask.routine.update( report, '_message_' )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertEqual( report.message, '_message_' )

        # Update using another report.
        report2 = aptask.routine.Report(
            status   = aptask.routine.Report.RUNNING,
            progress = 0.5,
            message  = '_message_'
        )
        report.update( report2 )
        self.assertEqual( report.status, report.RUNNING )
        self.assertEqual( report.progress, 0.5 )
        self.assertEqual( report.message, '_message_' )

        # Update using a string-able object.
        stringable = [ 'alpha', 'baker', 'charlie' ]
        string     = str( stringable )
        report.update( stringable )
        self.assertEqual( report.status, report.DONE )
        self.assertEqual( report.progress, 1.0 )
        self.assertEqual( report.message, string )


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
    def test_update( self ):
        """
        Tests the bound update method.
        """
        report1 = aptask.routine.Report()
        report2 = aptask.routine.Report(
            status   = aptask.routine.Report.RUNNING,
            progress = 0.5,
            message  = '_message_'
        )

        # Make sure all important fields are not equal.
        self.assertNotEqual( report2.status,   report1.status   )
        self.assertNotEqual( report2.progress, report1.progress )
        self.assertNotEqual( report2.message,  report1.message  )

        # Update report 1 with report 2's information.
        report1.update( report2 )

        # Make sure all important fields were updated.
        self.assertEqual( report2.status,   report1.status   )
        self.assertEqual( report2.progress, report1.progress )
        self.assertEqual( report2.message,  report1.message  )


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
    def test_get_args( self ):
        """
        Tests the get_args() Routine method.
        """

        # Create a routine without arguments.
        routine = aptask.routine.Routine()
        self.assertListEqual( [], routine.get_args() )

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
        self.assertListEqual( expected, routine.get_args() )


    #=========================================================================
    def test_abort( self ):
        """
        Tests the abort() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()

        # Verify the base routine does not implement the abort method.
        self.assertRaises( NotImplementedError, routine.abort )

        # Create a routine subclass.
        routine = _SubRoutine()

        # Request abort.
        routine.abort()

        # Verify abort was called on subclass.
        self.assertEqual( 1, routine._abort_called )


    #=========================================================================
    def test_get_help( self ):
        """
        Tests the get_help() Routine method.
        """

        # Create a routine with a simple docstring.
        routine = _SubRoutine()
        self.assertEqual( '_test_sub_routine_class_', routine.get_help() )


    #=========================================================================
    def test_get_status( self ):
        """
        Tests the get_status() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()

        # Verify status is set to initial status.
        self.assertEqual( aptask.routine.Report.INIT, routine.get_status() )


    #=========================================================================
    def test_initialize( self ):
        """
        Tests the initialize() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()

        # Verify the base routine does not implement the initialize method.
        self.assertRaises( NotImplementedError, routine.initialize )

        # Create a routine subclass.
        routine = _SubRoutine()

        # Request initialization.
        routine.initialize()

        # Verify initialize was called on subclass.
        self.assertEqual( 1, routine._initialize_called )


    #=========================================================================
    def test_is_done( self ):
        """
        Tests the is_done() Routine method.
        """

        # Create a base routine.
        routine = aptask.routine.Routine()

        # Verify routine reports not done.
        self.assertFalse( routine.is_done() )

        # Manually set routine to done status.
        routine.report.status = routine.report.DONE

        # Verify routine reports done.
        self.assertTrue( routine.is_done() )


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

        # Request processing.
        routine.process()

        # Verify process was called on subclass.
        self.assertEqual( 1, routine._process_called )


#=============================================================================
_testcalls  = 0
_testyields = 0
def _testentry( loops = 10 ):
    '_test_entry_point_function_'
    global _testcalls, _testyields
    _testcalls += 1
    if loops <= 0:
        loops = 1
    divisor = float( loops )
    for loop in range( loops + 1 ):
        _testyields += 1
        progress = loop / divisor
        yield progress


#=============================================================================
class TestRoutineEntry( unittest.TestCase ):
    """
    Tests the RoutineEntry class in the routine module
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs test setup.
        """
        global _testcalls, _testyields
        _testcalls  = 0
        _testyields = 0


    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        # Make sure the arguments were properly populated.
        expected = [ ( 'loops', 10 ) ]
        self.assertListEqual( expected, routine._arguments )


    #=========================================================================
    def test_abort( self ):
        """
        Tests the RoutineEntry abort() method.
        """

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        # Check initial status.
        self.assertEqual( aptask.routine.Report.INIT, routine.report.status )
        self.assertEqual( 0.0, routine.report.progress )
        self.assertIsNone( routine.report.message )

        # Request abort.
        routine.abort()

        # Check done status.
        self.assertEqual( aptask.routine.Report.DONE, routine.report.status )
        self.assertEqual( 0.0, routine.report.progress )
        self.assertIsNone( routine.report.message )


    #=========================================================================
    def test_get_help( self ):
        """
        Tests the RoutineEntry get_help() method.
        """

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        # Check for proper help string.
        self.assertEqual( '_test_entry_point_function_', routine.get_help() )


    #=========================================================================
    def test_initialize( self ):
        """
        Tests the RoutineEntry initialize() method.
        """

        global _testcalls

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        # Verify routine has not been called, or yielded a result.
        self.assertEqual( 0, _testcalls )
        self.assertEqual( 0, _testyields )

        # Initialize the routine.
        routine.initialize()

        # Check report status, progress, and message.
        self.assertEqual( routine.report.INIT, routine.report.status )
        self.assertEqual( 0.0, routine.report.progress )
        self.assertIsNone( routine.report.message )

        # Verify routine has been called, and yielded a result.
        self.assertEqual( 1, _testcalls )
        self.assertEqual( 1, _testyields )


    #=========================================================================
    def test_process( self ):
        """
        Tests the RoutineEntry process() method.
        """

        # Create the RoutineEntry object.
        routine = aptask.routine.RoutineEntry( _testentry )

        # Verify routine has not been called, or yielded a result.
        self.assertEqual( 0, _testcalls )
        self.assertEqual( 0, _testyields )

        # Initialize the routine.
        routine.initialize()

        # Check report status, progress, and message.
        self.assertEqual( routine.report.INIT, routine.report.status )
        self.assertEqual( 0.0, routine.report.progress )
        self.assertIsNone( routine.report.message )

        # Verify routine has been called, and yielded a result.
        self.assertEqual( 1, _testcalls )
        self.assertEqual( 1, _testyields )

        # Execute a step in the routine.
        routine.process()

        # Check report status, progress, and message.
        self.assertEqual( routine.report.RUNNING, routine.report.status )
        self.assertEqual( 0.1, routine.report.progress )
        self.assertIsNone( routine.report.message )

        # Verify the routine was not called again.
        self.assertEqual( 1, _testcalls )

        # Verify routine has yielded another result.
        self.assertEqual( 2, _testyields )

        # Execute a another step in the routine.
        routine.process()

        # Check report status, progress, and message.
        self.assertEqual( routine.report.RUNNING, routine.report.status )
        self.assertEqual( 0.2, routine.report.progress )
        self.assertIsNone( routine.report.message )

        # Verify routine has yielded another result.
        self.assertEqual( 3, _testyields )

        # Execute remaining steps.
        yields = 3
        while routine.is_done() == False:

            # Check the last known progress.
            self.assertAlmostEqual(
                ( yields - 1 ) * 0.1,
                routine.report.progress
            )

            # Execute a step in the routine.
            routine.process()

            # Check number of values yielded from generator.
            yields += 1
            self.assertEqual( yields, _testyields )

        # Check report status, progress, and message.
        self.assertEqual( routine.report.DONE, routine.report.status )
        self.assertEqual( 1.0, routine.report.progress )
        self.assertIsNone( routine.report.message )


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

