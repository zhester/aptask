#!/usr/bin/env python

"""
Network Interface Process

This implements a network daemon that communicates with its parent process
through a duplex pipe.  This daemon uses select polling to handle multiple
simultaneous clients.
"""


import errno
import select
import socket

import data
import session


#=============================================================================
class Message( data.Data ):
    """
    IPC Message Definition
    """

    #=========================================================================
    DATA = 1                        # message contains data
    QUIT = 86                       # message indicates process shutdown


    #=========================================================================
    def __init__( self, mid = DATA, sid = None, data = None ):
        """
        Constructor.
        @param mid      Message ID (default is for a data message)
        @param sid      Request session ID (required for data messages)
        @param data     Message data payload (as a string)
        """

        # load arguments into object state
        self.super_init( vars() )


#=============================================================================
QUIT = Message( Message.QUIT )      # message to send to shut down the process


#=============================================================================
def net( pipe, address ):
    """
    Network daemon process function.
    @param pipe         IPC duplex communication pipe connection object
    @param address      Address of the listen port (tuple)
    @return             Process exit code (0 = normal)
    """

    # create a session queue
    queue = session.SessionQueue()

    # set the maximum backlog for new connections (5 is often max)
    backlog = 5

    # set the maximum request payload size
    max_request_size = 2048

    # create and configure the server socket
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.bind( address )
    sock.listen( backlog )

    # list of input connections to poll
    poll = [ sock, pipe ]

    # loop execution flag
    is_running = True

    # daemon loop
    while( is_running == True ):

        # select next connection with available data
        try:
            inputs, outputs, excepts = select.select( poll, [], [] )

        # select errors
        except select.error as e:

            # select was interrupted by system call (SIGINT)
            if e.args[ 0 ] == errno.EINTR:
                for s in poll:
                    if ( s != sock ) and ( s != pipe ):
                        s.close()
                is_running = False
                break

        # process shut down by interactive input or application exit
        except ( KeyboardInterrupt, SystemExit ):
            for s in poll:
                if ( s != sock ) and ( s != pipe ):
                    s.close()
            is_running = False
            break

        # loop through all new inputs
        for ready in inputs:

            # handle parent process messages
            if ready == pipe:

                # fetch the message from the pipe
                message = pipe.recv()

                # check for daemon shutdown message
                if message.mid == Message.QUIT:
                    is_running = False

                # check for response data message
                elif message.mid == Message.DATA:

                    # remove the session from the queue
                    sess = queue.remove( message.sid )

                    # send the response data to the socket
                    sess[ 'sock' ].send( message.data )

                    # close the socket
                    sess[ 'sock' ].close()

            # handle a new connection with a network client
            elif ready == sock:

                # accept the new connection
                connection, address = ready.accept()

                # add the connection to the input polling list
                poll.append( connection )

            # handle data from all other connections
            else:

                # load the request data from the socket
                payload, address = ready.recvfrom( max_request_size )

                # data is available if the payload is not an empty string
                if len( payload ) > 0:

                    # add request to session queue
                    sid = queue.add( address = address, sock = ready )

                    # send request to parent
                    pipe.send( Message( sid = sid, data = payload ) )

                    # remove the socket from select polling
                    poll.remove( ready )

                # no data in payload (empty string)
                else:

                    # close the socket
                    ready.close()

                    # remove the socket from select polling
                    poll.remove( ready )

    # shut down the listen socket
    sock.close()

    # return exit code
    return 0


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    address = ( '', 9999 )

    # test client accepts a string to send and prints the response
    if len( argv ) > 1:
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( ( 'localhost', address[ 1 ] ) )
        sock.sendall( argv[ 1 ] )
        print sock.recv( 128 )
        sock.close()
        return 0

    # test server echos messages in all caps... real mature, server

    import multiprocessing

    ( p_pipe, c_pipe ) = multiprocessing.Pipe( True )
    netd = multiprocessing.Process(
        target = net,
        args   = ( c_pipe, address ),
        name   = 'netd'
    )
    netd.start()

    print 'server started, listening on port %d' % address[ 1 ]

    while True:
        try:
            message = p_pipe.recv()
            message.data = message.data.upper()
            p_pipe.send( message )
        except:
            break

    p_pipe.send( QUIT )

    print 'server shutting down'

    netd.join()

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
