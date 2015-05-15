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
        @param **kwargs Anything or everything, but not nothing
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
        self._iter = 0


    #=========================================================================
    def __contains__( self, key ):
        """
        Object "contains" magic method for "in" queries.
        @param key      Member name to check
        @return         If this object has that member
        """

        return hasattr( self, key )


    #=========================================================================
    def __delitem__( self, key ):
        """
        Deletes a member from the object when using "del" operator.
        @param key      Member name to delete
        """

        delattr( self, key )


    #=========================================================================
    def __iter__( self ):
        """
        Iterator protocol support.
        @return         The iterable object
        """

        self._iter = 0
        return self


    #=========================================================================
    def __len__( self ):
        """
        Support "len" built-in function.
        @return         Number of members in object
        """

        return len( self._keys )


    #=========================================================================
    def __getitem__( self, key ):
        """
        Support array-notation retrieval.
        @param key      Member name to retrieve
        @return         The value of the requested member
        """

        return getattr( self, key )


    #=========================================================================
    def __getstate__( self ):
        """
        Support pickle protocol to store an instance.
        @return         A dictionary containing all member data
        """

        return dict( ( k, self.__dict__[ k ] ) for k in self._keys )


    #=========================================================================
    def __setitem__( self, key, value ):
        """
        Support array-notation mutation.
        @param key      Member name to mutate
        @param value    The value to store in the requested member
        """

        setattr( self, key, value )


    #=========================================================================
    def __str__( self ):
        """
        Convert object data to a string (JSON).
        @return         String representation of object data
        """

        return json.dumps( self.__getstate__(), separators = ( ', ', ':' ) )


    #=========================================================================
    def __setstate__( self, data ):
        """
        Support pickle protocol to restore an instance.
        @param data     A dictionary containing all member data
        """

        self.__dict__.update( data )
        self._keys = data.keys()


    #=========================================================================
    def keys( self ):
        """
        Support a dictionary-style request for a list of all members.
        @return         A list of object member names
        """

        return self._keys


    #=========================================================================
    def next( self ):
        """
        Iterator protocol support.
        @return         Next member in object
        """

        if self._iter >= len( self._keys ):
            raise StopIteration

        key = self._keys[ self._iter ]
        self._iter += 1
        return getattr( self, key )


    #=========================================================================
    def super_init( self, data ):
        """
        Magical superclass initializer alias.
        @param data     A dictionary of member data to load into the object
        """

        super( self.__class__, self ).__init__( _vars = data )


    #=========================================================================
    def super_pairs( self, pairs ):
        """
        Magical superclass initializer alias using pair-wise data.
        @param pairs    A list of key-value pairs of member data.
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
