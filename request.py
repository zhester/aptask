#!/usr/bin/env python

"""
Request Parsing and Abstraction
"""


import json


#=============================================================================
class Request( object ):
    """
    Request Format Abstraction
    """


    #=========================================================================
    def __init__( self, string ):
        """
        Constructor.
        @param string   Request data as a string
        """

        # default attributes
        self.key     = None
        self.request = None

        # attempt to parse request data
        try:
            req = json.loads( request )
        except ValueError:
            self.valid_syntax = False
        else:
            self.valid_syntax = True

            # load request data into object
            for k, v in req.items():
                setattr( self, k, v )


    #=========================================================================
    def __getattr__( self, key ):
        """
        Silently handle missing attributes.
        @param key
        @return
        """

        return None


    #=========================================================================
    def is_valid( self ):
        """
        Checks if the request is valid for processing.
        """

        if ( self.valid_syntax == True ) and ( self.request is not None ):
            return True
        return False
