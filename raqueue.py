#!/usr/bin/env python

"""
Random Access Queue

Implements a random access queue on top of a dictionary.  The dictionary
foundation provides fast access to items through the hashing index.  It is
expected (but not required) that items are enqueued with the add() method and
dequeued with the remove() method.  Any item can be non-destructively
inspected through normal dictionary access methods.
"""


import time


#=============================================================================
class RandomAccessQueue( dict ):
    """
    Simplifies the process of generating hash indexes (compared to a normal
    dictionary) by generating them internally.
    """


    #=========================================================================
    def __init__( self, *args, **kwargs ):
        """
        Constructor.
        """

        super( RandomAccessQueue, self ).__init__( *args, **kwargs )

        self._next_id = 1


    #=========================================================================
    def __getitem__( self, key ):
        """
        Override index read access to prevent application aborts due an
        exception caused by attempting to reference an invalid key.
        @param key      The key of the item to retrieve
        @return         The item for the given key or None if key is invalid
        """

        # make sure the key is valid
        if key in self:

            # use the parent class' method to prevent recursion
            return super( RandomAccessQueue, self ).__getitem__( key )

        # invalid key, return None
        return None


    #=========================================================================
    def add( self, item ):
        """
        Adds a new item to the queue.
        @param item     The item (value, string, instance, etc) to enqueue
        @return         The assigned access key
        """

        # determine a suitable item key string
        key = str( self._next_id )
        self._next_id += 1

        # store the session item for hash-based (random) dequeuing later
        self[ key ] = item

        # return the new key
        return key


    #=========================================================================
    def remove( self, key ):
        """
        Removes and returns an item given its key.
        @param key      The key of the item to remove
        @return         The corresponding item
        """

        # fetch the item
        item = self[ key ]

        # remove it from the hash table
        del self[ key ]

        # return the item
        return item
