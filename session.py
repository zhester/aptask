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

import raqueue


#=============================================================================
class SessionQueue( raqueue.RandomAccessQueue ):
    """
    Simplifies the process of adding network-specific information to a queue.
    """


    #=========================================================================
    def add( self, address, sock ):
        """
        Adds a new session entry to the queue.
        @param address  The standard network address value (tuple)
        @param sock     The connection's socket instance/descriptor/handle
        @return         The assigned session ID
        """

        # get parameters as a dictionary
        data = vars()

        # store the start time of the session
        data[ 'time' ] = time.time()

        # add the session data to the queue, and return the session ID
        return super( SessionQueue, self ).add( data )
