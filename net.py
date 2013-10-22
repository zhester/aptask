#!/usr/bin/env python

"""
Network Interface Process

This implements a network daemon that communicates with its parent process
through a duplex pipe.  This daemon uses select polling to handle multiple
simultaneous clients.
"""


import select
import socket


#=============================================================================
class Message( object ):
    DATA = 1
    QUIT = 86
    def __init__( self, id = DATA, data = None ):
        self.id   = id
        self.data = data


#=============================================================================
QUIT = Message( Message.QUIT )      # message to send to shut down the process


#=============================================================================
def net( pipe, address ):
    """
    Network daemon process function.
    @param
    @param
    """

    # set the maximum backlog for new connections (5 is often max)
    backlog = 5

    # set the maximum request payload size
    max_request_size = 2048

    # create and configure the server socket
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.bind( address )
    sock.listen( backlog )

    # list of input connections to poll
    input = [ sock, pipe ]

    # loop execution flag
    is_running = True

    # daemon loop
    while( is_running == True ):

        # select next connection with available data
        inputs, outputs, excepts = select.select( input, [], [] )

        # loop through all new inputs
        for ready in inputs:

            # handle parent process messages
            if ready == pipe:
                message = pipe.recv()
                if message.id == Message.QUIT:
                    is_running = False

            # handle a new connection with a network client
            elif ready == sock:
                connection, address = ready.accept()
                input.append( connection )

            # handle data from all other connections
            else:

                # load the request data from the socket
                payload, address = ready.recvfrom( max_request_size )

                # ZIH - not sure what i'm testing yet (none? empty string?)
                if payload:

                    print ' #>', payload

                    # send request to parent
                    request = Message( data = payload )
                    pipe.send( request )

                    # get response and send data to client
                    response = pipe.recv()

                    print ' #<', response.data

                    ready.send( response.data )
                    input.remove( ready )

                    # ZIH - this could be improved by not blocking on the
                    # pipe receive... would need to manage a list of sockets
                    # waiting for a response, and sending to the socket after
                    # the pipe has data from select

                # no data in payload, drop the connection
                else:
                    ready.close()
                    input.remove( ready )

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



    # return success
    return 0

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

