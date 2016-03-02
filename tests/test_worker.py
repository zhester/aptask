#=============================================================================
#
# worker Module Unit Tests
#
#=============================================================================

"""
worker Module Unit Tests
======================
"""


import time
import unittest


import aptask.routine
import aptask.worker


__version__ = '0.0.0'



#=============================================================================
class CommandTests( unittest.TestCase ):
    """
    Tests the Command class in the worker module
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """

        cmd = aptask.worker.Command()
        self.assertEqual( aptask.worker.Command.CONTINUE, cmd.command_id )


    #=========================================================================
    def test_eq( self ):
        """
        Tests the equality operator for command objects.
        """

        cmd_def  = aptask.worker.Command()
        cmd_cont = aptask.worker.Command(
            command_id = aptask.worker.Command.CONTINUE
        )
        cmd_abort = aptask.worker.Command(
            command_id = aptask.worker.Command.ABORT
        )
        self.assertEqual( cmd_def, cmd_cont )
        self.assertNotEqual( cmd_def, cmd_abort )


#=============================================================================
class TestWorker( unittest.TestCase ):
    """
    Tests the Worker class in the worker module.
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs regular test setup procedures.
        """

        # Test variables.
        self._switch_time = 0.05 # Seconds to allow for task switching.

        # Create a known worker control instance.
        self.descr = { 'name' : 'deventry', 'arguments' : [ 0.0 ] }
        self.group = 'test'
        self.worker = aptask.worker.Worker( self.descr, self.group )


    #=========================================================================
    def test_init( self ):
        """
        Tests object initialization.
        """

        # Test each of the important attributes.
        self.assertIsNotNone( self.worker._command_queue )
        self.assertIsNotNone( self.worker._status_queue )
        self.assertEqual( 'aptask_worker_deventry', self.worker.name )
        self.assertEqual( self.group, self.worker.group )
        self.assertEqual( aptask.worker.Worker.INIT, self.worker._state )
        self.assertIsNone( self.worker._status )


    #=========================================================================
    def test_get_status( self ):
        """
        Tests the Worker.get_status() method.
        """

        # No status to report yet.
        self.assertIsNone( self.worker.get_status() )

        # Start the worker process.
        self.worker.start()

        # Let some context switching happen.
        time.sleep( self._switch_time )

        # Test that the status dequeues a report.
        report = self.worker.get_status()
        self.assertIsInstance( report, aptask.routine.Report )
        self.assertEqual( 1.0, report.progress )
        self.assertEqual( report.DONE, report.status )
        self.assertEqual( None, report.message )

        # Stop the worker process, and wait to unfork ourselves.
        self.worker.stop()
        self.worker.join()


    #=========================================================================
    def is_active( self ):
        """
        Tests the Worker.is_active() method.
        """

        # Test that the worker is not currently active.
        self.assertFalse( self.worker.is_active() )

        # Start the worker.
        self.worker.start()

        # Test that the worker is currently active.
        self.assertTrue( self.worker.is_active() )

        # Let some context switching happen.
        time.sleep( self._switch_time )

        # Test that the worker is not currently active.
        self.assertFalse( self.worker.is_active() )

        # Stop the worker process, and wait to unfork ourselves.
        self.worker.stop()
        self.worker.join()


    #=========================================================================
    def test_start( self ):
        """
        Tests the Worker.start() method.
        """
        ### ZIH
        pass


    #=========================================================================
    def test_stop( self ):
        """
        Tests the Worker.stop() method.
        """
        ### ZIH
        pass


#=============================================================================
class Test_worker( object ):
    """
    Tests the worker process function in the worker module.
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs regular test setup procedures.
        """

        # Test variables.
        self._switch_time = 0.05 # Seconds to allow for task switching.

        # Create a known worker control instance.
        self.descr = { 'name' : 'deventry', 'arguments' : [ 0.01 ] }
        self.group = 'test'
        self.worker = aptask.worker.Worker( self.descr, self.group )

        # Start the worker.
        self.worker.start()


    #=========================================================================
    def tearDown( self ):
        """
        Performs regular test teardown procedures.
        """

        # Stop the worker process, and wait to unfork ourselves.
        self.worker.stop()
        self.worker.join()


    #=========================================================================
    def test_abort( self ):
        """
        Tests worker termination.
        """
        ### ZIH
        pass


    #=========================================================================
    def test_initialize( self ):
        """
        Tests worker initialization.
        """
        ### ZIH
        pass


    #=========================================================================
    def test_process( self ):
        """
        Tests worker processing.
        """
        ### ZIH
        pass


    #=========================================================================
    def test_watchdog( self ):
        """
        Tests worker watchdog timeouts.
        """
        ### ZIH
        pass


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

