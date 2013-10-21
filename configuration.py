#!/usr/bin/env python

"""
Application Configuration
"""


import glob
import importlib
import json
import os
import sys


#=============================================================================
def load_configuration( filename ):
    """
    Load configuration from a file.
    """

    try:
        config = Configuration( filename )
    except VerificationError:
        return None
    return config


#=============================================================================
class Error( Exception ):
    """
    """

    pass


#=============================================================================
class VerificationError( Error ):
    """
    """

    pass


#=============================================================================
class KeyError( Error ):
    """
    """

    pass


#=============================================================================
class Configuration( object ):
    """
    """


    #=========================================================================
    commands_admins = ()
    commands_users  = ( 'index', 'start', 'stop', 'active' )


    #=========================================================================
    def __init__( self, config_file = None ):
        """
        """

        self._data = {}

        self.config_file = config_file

        if self.config_file is not None:
            self.load_file( self.config_file )


    #=========================================================================
    def __getattr__( self, key ):
        """
        """

        return self.get( key )


    #=========================================================================
    def get( self, key ):
        """
        """

        if key == 'tasks':
            return self._data[ 'directories' ][ 'tasks' ]

        if key == 'data':
            return self._data[ 'directories' ][ 'data' ]

        if key in self._data:
            return self._data[ key ]

        raise KeyError()


    #=========================================================================
    def get_address( self ):
        """
        """

        return ( self._data[ 'host' ], self._data[ 'port' ] )


    #=========================================================================
    def get_log_file( self ):
        """
        """

        return self.get_path( 'data' ) + os.sep + 'log.sqlite'


    #=========================================================================
    def get_path( self, key ):
        """
        """

        if key not in self._data[ 'directories' ]:
            raise KeyError()

        base = self._data[ 'directories' ][ key ]

        if base.startswith( '/' ) == True:
            return base

        script_path = os.path.realpath( __file__ )
        script_dir  = os.path.dirname( script_path )
        return script_dir + os.sep + base


    #=========================================================================
    def get_task_index( self ):
        """
        """

        path = self.get_path( 'tasks' )

        if path not in sys.path:
            sys.path.append( path )

        index = []

        modules = glob.glob( path + '/*.py' )
        for modfile in modules:
            modname = os.path.basename( modfile )[ : -3 ]
            module  = importlib.import_module( modname )
            for symname in dir( module ):
                if symname.lower() == modname:
                    ref = getattr( module, symname )
                    index.append(
                        {
                            'name'      : symname,
                            'arguments' : ref.getargs(),
                            'help'      : ref.gethelp()
                        }
                    )

        return index


    #=========================================================================
    def is_admin( self, auth_key ):
        """
        """

        if 'keys' not in self._data:
            return True

        if 'admins' not in self._data[ 'keys' ]:
            return True

        if self._data[ 'keys' ][ 'admins' ] is None:
            return True

        return auth_key in self._data[ 'keys' ][ 'admins' ]


    #=========================================================================
    def is_authorized( self, auth_key, request ):
        """
        """

        auth = False

        if request in Configuration.commands_users:
            if self.is_user( auth_key ) == True:
                auth = True
        elif request in Configuration.commands_admins:
            if self.is_admin( auth_key ) == True:
                auth = True

        return auth

    #=========================================================================
    def is_user( self, auth_key ):
        """
        """

        if 'keys' not in self._data:
            return True

        if 'users' not in self._data[ 'keys' ]:
            return True

        if self._data[ 'keys' ][ 'users' ] is None:
            return True

        return auth_key in self._data[ 'keys' ][ 'users' ]


    #=========================================================================
    def load_file( self, config_file ):
        """
        """

        with open( config_file, 'rb' ) as cf:
            self._data = json.load( cf )
        self.verify()


    #=========================================================================
    def verify( self ):
        """
        Checks the current configuration against reality.
        """

        if 'host' not in self._data:
            raise VerificationError()

        if 'port' not in self._data:
            raise VerificationError()

        if 'directories' not in self._data:
            raise VerificationError()

        dirs = self._data[ 'directories' ]

        if 'data' not in dirs:
            raise VerificationError()

        if 'tasks' not in dirs:
            raise VerificationError()

        if os.access( dirs[ 'data' ], ( os.R_OK | os.W_OK | os.X_OK ) ) == False:
            raise VerificationError()

        if os.access( dirs[ 'tasks' ], ( os.R_OK | os.X_OK ) ) == False:
            raise VerificationError()

        if 'loglevel' not in self._data:
            self._data[ 'loglevel' ] = 1


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    conf = load_configuration( 'aptaskd.json' )

    pp = {
        'sort_keys'  : True,
        'indent'     : 4,
        'separators' : ( ',', ' : ' )
    }

    print json.dumps( conf.get_address(), **pp )

    print json.dumps( conf.get_task_index(), **pp )

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )
