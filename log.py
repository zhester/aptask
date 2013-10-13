#!/usr/bin/env python


"""
Event Log Interface
"""


import sqlite3


#=============================================================================
class Event( object ):
    """
    """


    #=========================================================================
    table_name = 'log'


    #=========================================================================
    def __init__( self, message ):
        """
        """

        self.message = message
        self.open()
        self._check_schema()
        self.close()


#=============================================================================
class Log( object ):
    """
    """


    #=========================================================================
    def __init__( self, db_file ):
        """
        """

        self.db_file = db_file


    #=========================================================================
    def __enter__( self ):
        """
        """

        self.open()


    #=========================================================================
    def __exit__( self, *args ):
        """
        """

        self.close()


    #=========================================================================
    def append( self, event ):
        """
        """

        cursor.execute(
            """
            insert into ? ( message ) values ( ? )
            """,
            ( self.table_name, event.message )
        )
        cursor.commit()


    #=========================================================================
    def close( self ):
        """
        """

        self.db.close()


    #=========================================================================
    def open( self ):
        """
        """

        self.db = sqlite3.connect( self.db_file )


    #=========================================================================
    def _check_schema( self ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """"
            select name from sqlite_master
            where
                type = 'table'
                and
                name like ?
            """,
            ( self.table_name, )
        )

        if cursor.rowcount == 0:
            cursor.execute(
                """
                create table ? (
                    id        integer primary key,
                    timestamp datetime default current_timestamp,
                    message   text not null
                )
                """,
                ( self.table_name, )
            )
            cursor.commit()


