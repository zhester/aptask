#!/usr/bin/env python

"""
Worker/Task FIFO Queue
"""


#=============================================================================
class WorkerFIFO( object ):
    """
    """


    #=========================================================================
    def __init__( self, num_procs = 1 ):
        """
        Constructor.
        @param num_procs
        """

        self._iter_i   = 0
        self.next_id   = 1
        self.num_procs = num_procs
        self.queue     = []
        self.workers   = {}


    #=========================================================================
    def __iter__( self ):
        """
        Get iterator instance.
        @return
        """

        self._iter_i = 0
        return self


    #=========================================================================
    def add( self, wrkr ):
        """
        Add a worker to the queue.
        @param wrkr
        @return
        """

        # determine a suitable task ID
        task_id = str( self.next_id )
        self.next_id += 1

        # append the ID to the end of the queue
        self.queue.append( task_id )

        # add the worker object to the dictionary
        self.workers[ task_id ] = wrkr

        # return the task ID for this worker object
        return task_id


    #=========================================================================
    def get( self, task_id ):
        """
        Get a worker object by task ID.
        @param task_id
        @return
        """

        # attempt to get object from dictionary
        try:
            wrkr = self.workers[ task_id ]
        except KeyError:
            return None

        # return worker object
        return wrkr


    #=========================================================================
    def get_task_ids( self, active = False ):
        """
        Get list of task IDs in the queue.
        @param active
        @return
        """

        if active == True:
            return self.queue[ : self.num_procs ]

        return list( self.queue )


    #=========================================================================
    def next( self ):
        """
        Support for iterator protocol.
        @return
        """

        if self._iter_i >= len( self.workers ):
            raise StopIteration

        index = self._iter_i
        self._iter_i += 1
        return self.workers[ self.queue[ index ] ]


    #=========================================================================
    def remove( self, task_id = None ):
        """
        Remove a worker from the queue.
        @param task_id
        @return
        """

        # the default assumption is to remove the oldest worker (index = 0)
        if task_id is None:
            index = 0

        # if the ID is specified, we have to search the queue for the index
        else:
            try:
                index = self.queue.index( task_id )
            except ValueError:
                return None

        # remove the worker from the queue
        try:
            task_id = self.queue.pop( index )
        except IndexError:
            return None

        # retrieve the worker instance and delete it from the dictionary
        wrkr = self.workers[ task_id ]
        del self.workers[ task_id ]

        # return the worker instance that was removed
        return wrkr


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """

    queue = WorkerFIFO( 4 )

    print 'initial queue:', queue.queue
    queue.add( object() )
    print 'adding one:', queue.queue
    queue.add( object() )
    queue.add( object() )
    print 'adding two:', queue.queue
    queue.remove( '2' )
    print 'removing second:', queue.queue
    queue.add( object() )
    queue.add( object() )
    queue.add( object() )
    queue.add( object() )
    queue.add( object() )
    queue.add( object() )
    print 'adding six:', queue.queue
    print 'active only:', queue.get_task_ids( active = True )

    # return success
    return 0


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )
