#!/usr/bin/env python

"""
Network Session Queue

Provides a means of building a queue of network "sessions."  While the
fundamental protocol of the aptask system is session-less, the server uses
this term internally to refer to unserviced network requests.  This allows
better concurrency by not having to block the network process while the task
manager handles a particular request.  A "session" should last on the order of
a few miliseconds to less than one second.
"""


import time


class SessionQueue( object ):

    def __init__( self ):
        self.next_id  = 1
        self.sessions = {}

    def __getitem__( self, key ):
        return self.sessions[ key ]

    def __len__( self ):
        return len( self.sessions )

    def add( self, address, sock ):
        data = vars()
        data[ 'time' ] = time.time()
        sid = str( self.next_id )
        self.next_id += 1
        self.sessions[ sid ] = data
        return sid

    def remove( self, sid ):
        data = self.sessions[ sid ]
        del self.sessions[ sid ]
        return data
