#!/usr/bin/env python
#=============================================================================
#
# group Module Unit Tests
#
#=============================================================================

"""
group Module Unit Tests
=======================
"""


import unittest


import aptask.group


__version__ = '0.0.0'


#=============================================================================
class GroupTests( unittest.TestCase ):
    """
    Tests the group.Group class
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs test setup.
        """
        self.group = aptask.group.Group( 'testgroup' )


    #=========================================================================
    def test_init( self ):
        """
        Tests Group object initialization.
        """
        self.assertEqual( 'testgroup', self.group.name )
        self.assertListEqual( [], self.group._jobs )
        self.assertListEqual( [], self.group._tasks )


    #=========================================================================
    def test_contains( self ):
        """
        Tests the Group.__contains__ method.
        """
        self.group.clear()
        self.group.addjob( 'testjob' )
        self.group.addjob( 1 )
        self.group.addjob( None )
        self.assertIn( 'testjob', self.group )
        self.assertIn( 1, self.group )
        self.assertIn( None, self.group )


    #=========================================================================
    def test_str( self ):
        """
        Tests the Group.__str__ method.
        """
        self.group.clear()
        expected = '"testgroup" : { "tasks" : [], "jobs" : [] }'
        self.assertEqual( expected, str( self.group ) )


    #=========================================================================
    def test_addjob( self ):
        """
        Tests the Group.addjob method.
        """
        self.group.clear()
        self.group.addjob( 42 )
        self.assertIn( 42, self.group )
        self.assertListEqual( [ 42 ], self.group._jobs )
        self.group.addjob( 26 )
        self.assertIn( 26, self.group )
        self.assertListEqual( [ 42, 26 ], self.group._jobs )
        with self.assertRaises( ValueError ):
            self.group.addjob( 42 )


    #=========================================================================
    def test_addtask( self ):
        """
        Tests the Group.addtask method.
        """
        self.group.clear()
        self.group.addtask( 42 )
        self.assertListEqual( [ 42 ], self.group._tasks )
        self.group.addtask( 26 )
        self.assertListEqual( [ 42, 26 ], self.group._tasks )
        with self.assertRaises( ValueError ):
            self.group.addtask( 42 )


    #=========================================================================
    def test_clear( self ):
        """
        Tests the Group.clear method.
        """
        self.group.clear()
        self.assertEqual( 'testgroup', self.group.name )
        self.assertListEqual( [], self.group._jobs )
        self.assertListEqual( [], self.group._tasks )
        self.group.addjob( 1 )
        self.group.addtask( 2 )
        self.assertListEqual( [ 1 ], self.group._jobs )
        self.assertListEqual( [ 2 ], self.group._tasks )
        self.group.clear()
        self.assertListEqual( [], self.group._jobs )
        self.assertListEqual( [], self.group._tasks )


    #=========================================================================
    def test_removejob( self ):
        """
        Tests the Group.removejob method.
        """
        self.group.clear()
        self.assertListEqual( [], self.group._jobs )
        self.group.addjob( 42 )
        self.assertListEqual( [ 42 ], self.group._jobs )
        self.group.removejob( 42 )
        self.assertListEqual( [], self.group._jobs )
        with self.assertRaises( ValueError ):
            self.group.removejob( 42 )


    #=========================================================================
    def test_removetask( self ):
        """
        Tests the Group.removetask method.
        """
        self.group.clear()
        self.assertListEqual( [], self.group._tasks )
        self.group.addtask( 42 )
        self.assertListEqual( [ 42 ], self.group._tasks )
        self.group.removetask( 42 )
        self.assertListEqual( [], self.group._tasks )
        with self.assertRaises( ValueError ):
            self.group.removetask( 42 )



#=============================================================================
class TestManager( object ):
    """
    Tests the group.Manager class
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs test setup.
        """
        self.mgr = aptask.group.Manager()


    #=========================================================================
    def test_init( self ):
        """
        Tests the Manager.__init__ method.
        """
        self.assertIsInstance( self.mgr._groups, dict )
        self.assertIn( self.mgr.NONEKEY, self.mgr._groups )
        self.assertIn( self.mgr.SYSKEY, self.mgr._groups )
        self.assertEqual( 2, len( self.mgr._groups ) )


    #=========================================================================
    def test_delitem( self ):
        """
        Tests the Manager.__delitem__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_getitem( self ):
        """
        Tests the Manager.__getitem__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_iter( self ):
        """
        Tests the Manager.__iter__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_len( self ):
        """
        Tests the Manager.__len__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_setitem( self ):
        """
        Tests the Manager.__setitem__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_str( self ):
        """
        Tests the Manager.__str__ method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_clear( self ):
        """
        Tests the Manager.clear method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_items( self ):
        """
        Tests the Manager.items method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_iteritems( self ):
        """
        Tests the Manager.iteritems method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_iterkeys( self ):
        """
        Tests the Manager.iterkeys method.
        """
        self.mgr.clear()
        ### ZIH
        pass


    #=========================================================================
    def test_keys( self ):
        """
        Tests the Manager.keys method.
        """
        self.mgr.clear()
        ### ZIH
        pass


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

