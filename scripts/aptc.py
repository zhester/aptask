#!/usr/bin/env python
#=============================================================================
#
# aptask Client Interface Script
#
#=============================================================================

"""
aptask Client Interface Script
==============================
"""


import json
import os
import socket
import sys


__version__ = '0.0.0'


#=============================================================================
class Client( object ):
    """
    Development Client Class
    """


    #=========================================================================
    def __init__( self, address, key ):
        """
        Initializes a Client object.

        @param address The network address two-tuple: ( host, port )
        @param key     The client's identification key string
        """

        # Set object state.
        self.address = address
        self.key     = key


    #=========================================================================
    def get_active_tasks( self ):
        """
        Retrieves a list of all active tasks.

        @return A list of all active tasks represented by dictionaries
        """

        # Perform the "active" request.
        return self.request( { 'key' : self.key, 'request' : 'active' } )


    #=========================================================================
    def get_task_index( self ):
        """
        Retrieves a list of all available tasks.

        @return A list of all tasks represented by dictionaries
        """

        # Perform the "index" request.
        return self.request( { 'key' : self.key, 'request' : 'index' } )


    #=========================================================================
    def request( self, request ):
        """
        Performs a generic request and returns the response.

        @param request The aptask request message as a dictionary
        @return        The aptask server response message object
        """

        # Convert dictionary messages to JSON strings.
        if type( request ) is dict:
            request = json.dumps( request )

        # Create a TCP socket object.
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.settimeout( 60.0 )
        sock.connect( self.address )

        # Send the request message.
        sock.sendall( request )

        # Wait for response.
        try:
            response = sock.recv( 4096 )
        except socket.timeout:
            sock.close()
            print( 'Request timed out waiting for host.' )
            return None

        # Close our side of the socket.
        sock.close()

        # Attempt to parse and return the response.
        try:
            result = json.loads( response )
        except ValueError:
            return None
        return result


    #=========================================================================
    def start_task( self, name, arguments ):
        """
        Requests the start of a task.

        @param name      The string name of the task to start
        @param arguments The list of arguments to send to the task
        @return          The response of the request from the host
        """

        # Perform the start task request.
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

        @param taskid The task's ID number
        @return       The response of the request from the host
        """

        # Perform the stop task request.
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

    @param argv List of arguments passed to the script
    @return     Shell exit code (0 = success)
    """

    # Development configuration file path.
    config_file = os.path.sep.join(
        (
            os.path.dirname(
                os.path.dirname( os.path.realpath( __file__ ) )
            ),
            'conf',
            'aptaskd.json'
        )
    )

    # Imports when using this as a script
    import argparse

    # Create and configure an argument parser.
    parser = argparse.ArgumentParser(
        description = 'aptask Client Interface',
        add_help    = False
    )
    parser.add_argument(
        '-c',
        '--command',
        default = 'index',
        help    = 'Client command [active|index|start|stop]'
    )
    parser.add_argument(
        '-d',
        '--taskid',
        default = 0,
        help    = 'Specify a task ID for the request (stop).'
    )
    parser.add_argument(
        '-i',
        '--config',
        default = config_file,
        help    = 'Path to the daemon configuration.'
    )
    parser.add_argument(
        '-h',
        '--help',
        default = False,
        help    = 'Display this help message and exit.',
        action  = 'help'
    )
    parser.add_argument(
        '-t',
        '--taskname',
        default = 'DevTask',
        help    = 'Set the name of the task to start.'
    )
    parser.add_argument(
        '-v',
        '--version',
        default = False,
        help    = 'Display script version and exit.',
        action  = 'version',
        version = __version__
    )
    parser.add_argument(
        'args',
        nargs = '*',
        help  = 'Arguments to pass to new task.'
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Try to open configuration file.
    try:
        with open( args.config ) as cfh:
            config = json.load( cfh )
    except EnvironmentError:
        config = {}

    # Create a client object.
    client = Client(
        ( 'localhost', config.get( 'port', 2142 ) ),
        config.get( 'keys', {} ).get( 'users', [ 'userkey' ] )[ 0 ]
    )

    # Check for request to start a new task.
    if args.command == 'start':
        result = client.start_task( args.taskname, args.args )

    # Check for request to stop a running task.
    elif args.command == 'stop':
        result = client.stop_task( args.taskid )

    # Check for request to list active tasks.
    elif args.command == 'active':
        result = client.get_active_tasks()

    # Assume the request is to list all tasks in queue.
    else:
        result = client.get_task_index()

    # kwargs for pretty-printing JSON
    pp = {
        'indent'     : 4,
        'separators' : ( ',', ' : ' )
    }

    # Display results on console.
    print( json.dumps( result, **pp ) )

    # Return success.
    return 0


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

