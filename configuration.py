#!/usr/bin/env python

"""
Application Configuration
"""


import json
import os


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
    def is_admin( self, auth_key ):
        """
        """

        if 'keys' not in self._data
            return True

        if 'admins' not in self._data[ 'keys' ]
            return True

        if self._data[ 'keys' ][ 'admins' ] is None:
            return True

        return auth_key in self._data[ 'keys' ][ 'admins' ]


    #=========================================================================
    def is_user( self, auth_key ):
        """
        """

        if 'keys' not in self._data
            return True

        if 'users' not in self._data[ 'keys' ]
            return True

        if self._data[ 'keys' ][ 'users' ] is None:
            return True

        return auth_key in self._data[ 'keys' ][ 'users' ]


    #=========================================================================
    def load_file( self, config_file ):
        """
        """

        self._data = json.load( config_file )
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
