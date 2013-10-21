#!/usr/bin/env python

"""
aptask Development Client
"""


import json
import socket

import configuration


#=============================================================================
class Client( object ):
    """
    Development Client Class
    """


    #=========================================================================
    def __init__( self, address, key ):
        """
        Constructor.
        @param address
        @param key
        """

        self.address = address
        self.key     = key

        # create a TCP socket object
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.sock.settimeout( 5.0 )
        self.sock.connect( self.address )


    #=========================================================================
    def __del__( self ):
        """
        Destructor.
        """

        self.sock.close()


    #=========================================================================
    def get_active_tasks( self ):
        """
        Retrieves a list of all active tasks.
        @return
        """

        return self.request( { 'key' : self.key, 'request' : 'active' } )


    #=========================================================================
    def get_task_index( self ):
        """
        Retrieves a list of all available tasks.
        @return
        """

        return self.request( { 'key' : self.key, 'request' : 'index' } )


    #=========================================================================
    def request( self, request ):
        """
        Performs a generic request and returns the response.
        @param request
        @return
        """

        if type( request ) is dict:
            request = json.dumps( request )

        self.sock.sendall( request )

        try:
            response = self.sock.recv( 4096 )
        except socket.timeout:
            print 'receive timed out'
            return None

        try:
            res = json.loads( response )
        except ValueError:
            return None
        else:
            return res


    #=========================================================================
    def start_task( self, name, arguments ):
        """
        Requests the start of a task.
        @param name
        @param arguments
        @return
        """

        return self.request(
            {
                'key'       : self.key,
                'request'   : 'start',
                'name'      : name,
                'arguments' : arguments
            }
        )


    #=========================================================================
    def stop_task( self, taskid ):
        """
        Requests an abort of a task.
        @param taskid
        @return
        """

        return self.request(
            {
                'key'     : self.key,
                'request' : 'stop',
                'taskid'  : taskid
            }
        )


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    config = configuration.load_configuration( 'aptaskd.json' )

    address = ( 'localhost', config.get_address()[ 1 ] )

    client = Client( address, config.keys[ 'users' ][ 0 ] )

    pp = {
        'indent'     : 4,
        'separators' : ( ',', ' : ' )
    }

    index = client.get_task_index()
    #print json.dumps( index, **pp )

    devtask = index[ 'index' ][ 0 ][ 'name' ]

    for devarg in range( 4 ):
        result = client.start_task( devtask, ( devarg, ) )
        #print json.dumps( result, **pp )

    active = client.get_active_tasks()
    print json.dumps( active, **pp )

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )