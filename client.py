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


    #=========================================================================
    def __del__( self ):
        """
        Destructor.
        """

        pass


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

        # create a TCP socket object
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.settimeout( 60.0 )
        sock.connect( self.address )

        sock.sendall( request )

        try:
            response = sock.recv( 4096 )
        except socket.timeout:
            sock.close()
            print 'receive timed out'
            return None

        sock.close()

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

    # example of fetching the task index
    #index = client.get_task_index()
    #print json.dumps( index, **pp )
    #devtask = index[ 'index' ][ 0 ][ 'name' ]

    devtask = 'DevTask'

    if len( argv ) > 1:
        start = int( argv[ 1 ] )
        for devarg in range( start ):
            result = client.start_task( devtask, ( devarg, ) )

    active = client.get_active_tasks()
    print json.dumps( active, **pp )

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
