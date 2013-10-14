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
    def __init__( self, message, timestamp = None ):
        """
        """

        self.message   = message
        self.timestamp = timestamp


#=============================================================================
class Log( object ):
    """
    """


    #=========================================================================
    table_name = 'log'


    #=========================================================================
    def __init__( self, db_file ):
        """
        """

        self.db_file = db_file
        self.open()
        self._check_schema()
        self.close()


    #=========================================================================
    def __enter__( self ):
        """
        """

        self.open()
        return self


    #=========================================================================
    def __exit__( self, *args ):
        """
        """

        self.close()


    #=========================================================================
    def append( self, event ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            insert into %s ( message ) values ( ? )
            """ % self.table_name,
            ( event.message, )
        )
        self.db.commit()


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
    def purge( self ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            delete from %s
            """  % self.table_name
        )


    #=========================================================================
    def tail( self, num_events = 10 ):
        """
        """

        cursor = self.db.cursor()
        cursor.execute(
            """
            select
                message,
                timestamp
            from (
                select
                    id,
                    message,
                    timestamp
                from %s
                order by
                    timestamp desc,
                    id desc
                limit ?
            ) as dummy_alias
            order by
                timestamp asc,
                id asc
            """ % self.table_name,
            ( num_events, )
        )

        events = []
        for event in cursor.fetchall():
            events.append( Event( *event ) )

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
                    timestamp datetime default current_timestamp,
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

    messages = [ 'hello log', 'event 2', 'event 3' ]

    with Log( 'test.sqlite' ) as log:
        log.purge()
        for message in messages:
            log.append( Event( message ) )

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
