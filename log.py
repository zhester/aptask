#!/usr/bin/env python

"""
Event Log Interface
"""


import sqlite3

import data


#=============================================================================
UNSPECIFIED  = 0
SERVER_ERROR = 1
CLIENT_ERROR = 2
REQUEST      = 3
RESPONSE     = 4
TASKING      = 5
STATISTICS   = 6
ALL          = 6


#=============================================================================
level_strings = (
    'unspecified',
    'server error',
    'client error',
    'request',
    'response',
    'tasking',
    'statistics'
)


#=============================================================================
class Event( data.Data ):
    """
    """


    #=========================================================================
    def __init__(
        self,
        message,
        level     = 0,
        authkey   = None,
        timestamp = None
    ):
        """
        """

        # load constructor parameters into object state
        self.super_init( vars() )


    #=========================================================================
    def __str__( self ):
        """
        """

        return '%s,%d,%s,"%s"' % (
            self.timestamp,
            self.level,
            self.authkey,
            self.message.replace( '"', '""' )
        )


#=============================================================================
class Log( object ):
    """
    """


    #=========================================================================
    table_name = 'log'


    #=========================================================================
    def __init__( self, db_file, max_level = 1 ):
        """
        """

        self.db_file        = db_file
        self.db             = sqlite3.connect( self.db_file )
        self.db.row_factory = sqlite3.Row
        self.is_open        = True
        self.max_level      = max_level
        self._check_schema()


    #=========================================================================
    def __enter__( self ):
        """
        """

        if self.is_open == False:
            self.db = sqlite3.connect( self.db_file )
            self.is_open = True
        return self


    #=========================================================================
    def __exit__( self, *args ):
        """
        """

        if self.is_open == True:
            self.close()


    #=========================================================================
    def append( self, event ):
        """
        """

        if event.level > self.max_level:
            return

        cursor = self.db.cursor()
        cursor.execute(
            """
            insert into %s ( message, level, authkey ) values ( ?, ?, ? )
            """ % self.table_name,
            ( event.message, event.level, event.authkey )
        )
        self.db.commit()


    #=========================================================================
    def append_message( self, message ):
        """
        """

        self.append( Event( message ) )


    #=========================================================================
    def log( self, level, message, authkey = None ):
        """
        """

        self.append( Event( message, level, authkey ) )


    #=========================================================================
    def close( self ):
        """
        """

        self.db.close()


    #=========================================================================
    def purge( self ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            delete from %s
            """  % self.table_name
        )
        self.db.commit()


    #=========================================================================
    def tail( self, num_events = 10, max_level = ALL ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            select
                message,
                timestamp,
                level,
                authkey
            from (
                select
                    id,
                    message,
                    timestamp,
                    level,
                    authkey
                from %s
                where
                    level <= ?
                order by
                    timestamp desc,
                    id desc
                limit ?
            ) as dummy_alias
            order by
                timestamp asc,
                id asc
            """ % self.table_name,
            ( max_level, num_events )
        )

        events = []
        for row in cursor.fetchall():
            events.append( Event( **dict( zip( row.keys(), row ) ) ) )

        return events


    #=========================================================================
    def _check_schema( self ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            select name
            from sqlite_master
            where
                type = 'table'
                and
                name like ?
            """,
            ( self.table_name, )
        )

        record = cursor.fetchone()

        if record is None:
            cursor.execute(
                """
                create table %s (
                    id        integer primary key,
                    level     integer default 0,
                    timestamp datetime default current_timestamp,
                    authkey   text,
                    message   text not null
                )
                """ % self.table_name
            )


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    import configuration
    config = configuration.load_configuration( 'aptaskd.json' )

    if len( argv ) > 1:
        if argv[ 1 ] == 'purge':
            with Log( config.get_log_file() ) as log:
                log.purge()
        else:
            num_events = int( argv[ 1 ] )
            if len( argv ) > 2:
                max_level = int( argv[ 2 ] )
            else:
                max_level = ALL
            tail = []
            with Log( config.get_log_file() ) as log:
                tail = log.tail( num_events, max_level )
            for event in tail:
                print event

    else:
        messages = [ 'hello log', 'event 2', 'event 3' ]
        with Log( 'test.sqlite' ) as log:
            log.purge()
            for message in messages:
                log.append_message( message )
            tail = log.tail()
            index = 0
            for event in tail:
                if event.message != messages[ index ]:
                    print 'error: logged message mismatch'
                    print '  ', event.message, '!=', messages[ index ]
                    return 1
                index += 1
            print 'success: all logged messages recorded'

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
