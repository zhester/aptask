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
QUIT = 86                           # value to send to shut down the process


#=============================================================================
def net( pipe, address, handler ):
    """
    Network daemon process function.
    @param
    @param
    """

    # ZIH - may change pipe to queue if i don't need to send anything back

    # set the maximum backlog for new connections (5 is often max)
    backlog = 5

    # set the maximum request payload size
    max_request_size = 1024

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
                if message == QUIT:
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

                    # pass the request to the handler which should send the
                    #   response using the supplied socket
                    close = handler( ready, address, payload )
                    if close = True:
                        ready.close()
                        input.remove( ready )

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

