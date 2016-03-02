#=============================================================================
#
# Application Configuration
#
#=============================================================================


"""
Application Configuration
=========================
"""


import glob
import importlib
import json
import logging
import os
import sys


#=============================================================================
def load_configuration( filename ):
    """
    Loads configuration from a file.

    @param filename     The name of the file where the configuration is stored
    @return             A populated Configuration object
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

        return self.get_path( 'data' ) + os.sep + 'aptask.log'


    #=========================================================================
    def get_path( self, key ):
        """
        """

        if key not in self._data[ 'directories' ]:
            raise KeyError()

        base = self._data[ 'directories' ][ key ]

        if base.startswith( '/' ) == True:
            return base

        script_dir = os.path.realpath( os.getcwd() )
        return script_dir + os.sep + base


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

        # Host is required.
        if 'host' not in self._data:
            raise VerificationError()

        # Port is required.
        if 'port' not in self._data:
            raise VerificationError()

        # Directories are required.
        if 'directories' not in self._data:
            raise VerificationError()

        dirs = self._data[ 'directories' ]

        # Routines directory is required.
        if 'routines' not in dirs:
            raise VerificationError()

        # Make sure script has access to routines directory.
        if os.access( dirs[ 'routines' ], ( os.R_OK | os.X_OK ) ) == False:
            raise VerificationError()

        # Check/default the logging level.
        ll = self._data.get( 'loglevel', logging.WARNING )
        if isinstance( ll, basestring ):
            if hasattr( logging, ll ):
                self._data[ 'loglevel' ] = getattr( logging, ll )
            else:
                self._data[ 'loglevel' ] = logging.WARNING

