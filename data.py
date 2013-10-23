#!/usr/bin/env python

"""
Data Object

A very generic object intended to be used to store and transmit simple data.
This is similar to using a dict.  Hoever, fields are accessed using
attributes, and this is intended to be extended as future needs warrant.
The key to using this module correctly is defining the fields necessary for
your object in your subclass' constructor.  Once defined there, this class
eliminates dual-maintenance issues.
"""


import json


#=============================================================================
class Data( object ):
    """
    Data Object Base Class
    """


    #=========================================================================
    def __init__( self, **kwargs ):
        """
        Constructor.
        @param *args    Anything, everything, or nothing
        @param **kwargs Anything, everything, or nothing
        """

        # check for secret handshake
        if '_vars' in kwargs:
            if 'self' in kwargs[ '_vars' ]:
                del kwargs[ '_vars' ][ 'self' ]
            self.__dict__.update( **kwargs[ '_vars' ] )
            del kwargs[ '_vars' ]

        # load keyword arguments into object state
        self.__dict__.update( **kwargs )

        # record a separate list of keys in case the subclass adds more later
        self._keys = self.__dict__.keys()


    #=========================================================================
    def __contains__( self, key ):
        """
        """

        return hasattr( self, key )


    #=========================================================================
    def __delitem__( self, key ):
        """
        """

        delattr( self, key )


    #=========================================================================
    def __iter__( self ):
        """
        """

        return self.__dict__


    #=========================================================================
    def __len__( self ):
        """
        """

        return len( self.__dict__ )


    #=========================================================================
    def __getitem__( self, key ):
        """
        """

        return getattr( self, key )


    #=========================================================================
    def __str__( self ):
        """
        """

        return json.dumps( self.__getstate__(), separators = ( ', ', ':' ) )


    #=========================================================================
    def __setitem__( self, key, value ):
        """
        """

        setattr( self, key, value )


    #=========================================================================
    def __getstate__( self ):
        """
        """

        return dict( ( k, self.__dict__[ k ] ) for k in self._keys )


    #=========================================================================
    def __setstate__( self, data ):
        """
        """

        self.__dict__.update( data )


    #=========================================================================
    def keys( self ):
        """
        """

        return self._keys


    #=========================================================================
    def super_init( self, data ):
        """
        """

        super( self.__class__, self ).__init__( _vars = data )


    #=========================================================================
    def super_pairs( self, pairs ):
        """
        """

        super( self.__class__, self ).__init__( _vars = dict( pairs ) )


#=============================================================================
class _Test( Data ):

    #=========================================================================
    def __init__( self, a, b = 1, c = '2', d = None ):
        self.super_init( vars() )


#=============================================================================
class _Test2( Data ):

    #=========================================================================
    def __init__( self, a, b = 1, c = '2', d = None ):
        d = vars()
        self.super_pairs( zip( d.keys(), d.values() ) )


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    t = _Test( a = 8 )
    print t

    t = _Test2( a = 9 )
    print t

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
