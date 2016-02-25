#=============================================================================
#
# Data Object
#
#=============================================================================


"""
Data Object
===========

A very generic object intended to be used to store and transmit simple data.
In practice, this is similar to a mutable version of a
`collections.namedtuple` that is meant to be extended.

The key to using this module correctly is defining the fields necessary for
your object in your subclass.  Once defined there, this class minimizes
dual-maintenance.

Example Usage
-------------

    class MyData( Data ):
        _fields = [
            ( 'field_1', 42 ),
            ( 'field_2', 3.1 ),
            ( 'field_3', 'green' )
        ]

    data = MyData( field_2 = 1.23 )

    print( data.field_1, data.field_2, data.field_3 )

    serial_data = str( data )

See: [tests/test_data.py](tests/test_data.py) for usage testing.
"""


import json


#=============================================================================
class Data( object ):
    """
    Data Object Base Class
    """


    #=========================================================================
    # Inheriting classes can provide a list of fields they wish to formally
    # define along with their default values.  This is specified as a list of
    # two-tuples: `[ ( 'name', 'default' ), ... ]`
    _fields = None


    #=========================================================================
    def __init__( self, *args, **kwargs ):
        """
        Initializes a basic Data object.

        When specifying positional arguments, these values are loaded into the
        object in the order of the specified `_fields` list.

        When specifying keyword arguments, only arguments that match the names
        given in the subclass' `_fields` attribute are loaded.

        @param *args    The initial field values for the data object.
        @param **kwargs The initial fields and values for the data object.
        """

        # Initialize list of serializable object fields.
        self._keys     = []
        self._defaults = {}

        # Look for fields in the subclass.
        if self._fields is not None:

            # Establish each field in this object.
            for key, default in self._fields:

                # Set up the field.
                self._keys.append( key )
                self._defaults[ key ] = default
                setattr( self, key, default )

            # Attempt to set attributes from positional arguments.
            for index, arg in enumerate( args ):
                setattr( self, self._keys[ index ], args )

            # Attempt to set attributes from keyword arguments.
            self.__dict__.update( kwargs )


    #=========================================================================
    def __contains__( self, key ):
        """
        Implements the method for `in` queries.

        @param key Field name to check
        @return    If this object has that field
        """

        # Check the list of serializable fields.
        return key in self._keys


    #=========================================================================
    def __delitem__( self, key ):
        """
        Deletes a field from the object when using `del` operator on
        subscripted fields.

        @param key Field name to delete
        """

        # Check presence of field.
        if key not in self._keys:
            raise KeyError( key )

        # Remove the field.
        self._keys.remove( key )
        del self._defaults[ key ]
        delattr( self, key )


    #=========================================================================
    def __iter__( self ):
        """
        Implements iterator protocol support.  Iteration is in the style of
        dictionaries (each item is the name of a field in the object).

        @return A generator producing the names of each field in the object
        """

        # Yield each key.
        for key in self._keys:
            yield key


    #=========================================================================
    def __len__( self ):
        """
        Supports the `len()` built-in function.

        @return Number of fields in the object
        """

        return len( self._keys )


    #=========================================================================
    def __getitem__( self, key ):
        """
        Supports subscript notation of field values.

        @param key Field name from which to retrieve a value
        @return    The value of the requested field
        """

        # Raise the expected exception if this field doesn't exist.
        if key not in self._keys:
            raise KeyError( key )

        # Attempt to retrieve the value from the attribute.
        return getattr( self, key )


    #=========================================================================
    def __getstate__( self ):
        """
        Supports the pickle protocol to serialize an instance.

        @return A dictionary containing all serializable fields
        """

        # Scan the object for required fields.
        return dict( ( k, self.__dict__[ k ] ) for k in self._keys )


    #=========================================================================
    def __setitem__( self, key, value ):
        """
        Supports subscript notation of field values.

        @param key   Field name of which to update
        @param value The value to store in the requested field
        """

        # Raise an exception if this field doesn't exist.
        if key not in self._keys:
            raise KeyError( key )

        # Set the value for this field in the object's state.
        setattr( self, key, value )


    #=========================================================================
    def __str__( self ):
        """
        Serializes object data into a JSON string.

        @return String representation of object state
        """

        # Use JSON to serialize object state.
        return json.dumps( self.__getstate__() )


    #=========================================================================
    def __setstate__( self, data ):
        """
        Supports pickle protocol to un-serialize an instance.

        @param data A dictionary containing all member data
        """

        # Reset field list.
        self._keys = data.keys()

        # Reset default values.
        self._defaults = dict( data )

        # Update all attribute values.
        self.__dict__.update( data )


    #=========================================================================
    def keys( self ):
        """
        Supports dictionary-style request for a list of all field names.

        @return A list of names of fields in this object
        """

        # Return a list of field names.
        return list( self._keys )


#=============================================================================
class DynamicData( Data ):
    """
    Extends the Data class to provide dynamic object creation without requring
    a subclass.
    """


    #=========================================================================
    def __init__( self, **kwargs ):
        """
        Initializes a DynamicData object.

        Unlike the generic Data container, this object can only be initialized
        using keyword arguments.  These arguments are used to create the
        object's serializable fields and initial values.

        @param **kwargs The initial fields and values for the data object.
        """

        # Construct the _fields list before we initialize the object.
        self._fields = kwargs.items()

        # Initialize the object with the given values.
        super( DynamicData, self ).__init__( **kwargs )

