#=============================================================================
#
# data Module Unit Tests
#
#=============================================================================

"""
data Module Unit Tests
======================
"""


import json
import pickle
import unittest


import aptask.data


__version__ = '0.0.0'



#=============================================================================
class _SubData( aptask.data.Data ):
    """
    Subclass of the Data class used for testing.
    """

    _fields = [
        ( 'field_1', 1 ),
        ( 'field_2', 2.22 ),
        ( 'field_3', 'hello' ),
        ( 'field_4', None )
    ]


#=============================================================================
class DataTests( unittest.TestCase ):
    """
    Tests the Data class in the data module
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

        obj = aptask.data.Data()
        self.assertEqual( 0, len( obj ) )

        sobj = _SubData()
        self.assertEqual( len( _SubData._fields ), len( sobj ) )


    #=========================================================================
    def test_init_fields( self ):
        """
        Tests initialization of subclass-specified fields.
        """

        sobj = _SubData()

        self.assertIn( 'field_1', sobj )
        self.assertIn( 'field_2', sobj )
        self.assertIn( 'field_3', sobj )
        self.assertIn( 'field_4', sobj )
        self.assertEqual( sobj.field_1, 1 )
        self.assertEqual( sobj.field_2, 2.22 )
        self.assertEqual( sobj.field_3, 'hello' )
        self.assertIsNone( sobj.field_4 )


    #=========================================================================
    def test_init_dynamic( self ):
        """
        Tests dynamic field initialization.
        """

        dobj = aptask.data.DynamicData( a = 1, b = '2', c = None )

        self.assertIn( 'a', dobj )
        self.assertIn( 'b', dobj )
        self.assertIn( 'c', dobj )
        self.assertEqual( dobj.a, 1 )
        self.assertEqual( dobj.b, '2' )
        self.assertIsNone( dobj.c )


    #=========================================================================
    def test_contains( self ):
        """
        Tests operation of the `in` query.
        """

        sobj = _SubData()

        # Normal range
        self.assertIn( 'field_1', sobj )
        self.assertIn( 'field_2', sobj )
        self.assertIn( 'field_3', sobj )
        self.assertIn( 'field_4', sobj )

        # Robustness
        self.assertNotIn( 'fake_field', sobj )


    #=========================================================================
    def test_delitem( self ):
        """
        Tests operation of the `del` operation.
        """

        sobj = _SubData()

        # Normal range
        expected_length = len( _SubData._fields )
        self.assertIn( 'field_1', sobj )
        self.assertEqual( expected_length, len( sobj ) )
        del sobj[ 'field_1' ]
        self.assertNotIn( 'field_1', sobj )
        self.assertEqual( expected_length - 1, len( sobj ) )

        # Robustness
        with self.assertRaises( KeyError ):
            del sobj[ 'fake_field' ]


    #=========================================================================
    def test_iter( self ):
        """
        Tests object iteration interface.
        """

        sobj = _SubData()

        expected_fields = [ f[ 0 ] for f in _SubData._fields ]

        actual_fields = []
        for name in sobj:
            actual_fields.append( name )

        self.assertListEqual( expected_fields, actual_fields )


    #=========================================================================
    def test_len( self ):
        """
        Tests object length determination.
        """

        sobj = _SubData()

        expected_length = len( _SubData._fields )

        self.assertEqual( expected_length, len( sobj ) )


    #=========================================================================
    def test_getitem( self ):
        """
        Tests subscript notation for value retrieval.
        """

        sobj = _SubData()

        # Normal range
        self.assertEqual( _SubData._fields[ 0 ][ 1 ], sobj[ 'field_1' ] )
        self.assertEqual( _SubData._fields[ 1 ][ 1 ], sobj[ 'field_2' ] )
        self.assertEqual( _SubData._fields[ 2 ][ 1 ], sobj[ 'field_3' ] )
        self.assertEqual( _SubData._fields[ 3 ][ 1 ], sobj[ 'field_4' ] )

        # Robustness
        with self.assertRaises( KeyError ):
            value = sobj[ 'fake_field' ]


    #=========================================================================
    def test_pickle( self ):
        """
        Tests object state serialization/unserialization.
        """

        sobj = _SubData()
        expected_data = dict( _SubData._fields )

        # Normal range
        state_data = sobj.__getstate__()
        serial_data = pickle.dumps( sobj )
        self.assertDictEqual( expected_data, state_data )
        uobj = pickle.loads( serial_data )
        self.assertEqual( uobj.field_1, sobj.field_1 )
        self.assertEqual( uobj.field_2, sobj.field_2 )
        self.assertEqual( uobj.field_3, sobj.field_3 )
        self.assertEqual( uobj.field_4, sobj.field_4 )
        self.assertDictEqual( state_data, uobj.__getstate__() )


    #=========================================================================
    def test_setitem( self ):
        """
        Tests subscript notation for value updating.
        """

        sobj = _SubData()

        # Normal range
        sobj[ 'field_1' ] = 99
        sobj[ 'field_2' ] = 12.34
        sobj[ 'field_3' ] = 'bye'
        sobj[ 'field_4' ] = False
        self.assertEqual( 99, sobj[ 'field_1' ] )
        self.assertEqual( 12.34, sobj[ 'field_2' ] )
        self.assertEqual( 'bye', sobj[ 'field_3' ] )
        self.assertEqual( False, sobj[ 'field_4' ] )

        # Robustness
        with self.assertRaises( KeyError ):
            sobj[ 'fake_field' ] = 'value'


    #=========================================================================
    def test_str( self ):
        """
        Tests object conversion to a JSON string.
        """

        def jsoneq( a, b ):
            adict = json.loads( a )
            bdict = json.loads( b )
            return adict == bdict

        sobj = _SubData()

        expected_json = json.dumps( dict( _SubData._fields ) )

        actual_json = str( sobj )

        self.assertTrue( jsoneq( expected_json, actual_json ) )


    #=========================================================================
    def test_keys( self ):
        """
        Tests retrieval of object field names.
        """

        sobj = _SubData()

        expected_keys = [ f[ 0 ] for f in _SubData._fields ]

        self.assertListEqual( expected_keys, sobj.keys() )


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

