#!/usr/bin/env python

"""
Worker/Task FIFO Queue
"""


import raqueue


#=============================================================================
class WorkerFIFO( raqueue.RandomAccessQueue ):
    """
    Implements a FIFO queue to ensure first-come, first-served task execution.
    Additionally, this allows random access to all items in the queue to allow
    a user to check on status, and execute multiple simultaneous tasks without
    removing them from the queue.
    """


    #=========================================================================
    def __init__( self, num_procs = 1 ):
        """
        Constructor.
        @param num_procs
                        Maximum number of concurrent worker processes
        """

        super( WorkerFIFO, self ).__init__()

        self._iter     = 0
        self.num_procs = num_procs
        self.fifo      = []


    #=========================================================================
    def __iter__( self ):
        """
        Iterator protocol support.
        @return         Iterable object
        """

        self._iter = 0
        return self


    #=========================================================================
    def add( self, wrkr ):
        """
        Add a worker to the queue.
        @param wrkr     Worker object to enqueue
        @return         Assigned task ID
        """

        # enqueue the worker object
        task_id = super( WorkerFIFO, self ).add( wrkr )

        # append the ID to the end of the queue
        self.fifo.append( task_id )

        # return the task ID for this worker object
        return task_id


    #=========================================================================
    def get_task_ids( self, active = False ):
        """
        Get list of task IDs in the queue.
        @param active   Set this option to only retrieve active task IDs
        @return         A list of task IDs in the queue
        """

        if active == True:
            return self.fifo[ : self.num_procs ]

        return list( self.fifo )


    #=========================================================================
    def next( self ):
        """
        Iterator protocol support.
        @return         Next worker in queue
        """

        if self._iter >= len( self.fifo ):
            raise StopIteration

        task_id = self.fifo[ self._iter ]
        self._iter += 1
        return self[ task_id ]


    #=========================================================================
    def remove( self, task_id = None ):
        """
        Remove a worker from the queue.
        @param task_id  The task ID to remove
        @return         The worker object that was removed
        """

        # the default assumption is to remove the oldest worker (index = 0)
        if task_id is None:
            index = 0

        # if the ID is specified, we have to search the queue for the index
        else:
            try:
                index = self.fifo.index( task_id )
            except ValueError:
                return None

        # remove the worker from the queue
        try:
            task_id = self.fifo.pop( index )
        except IndexError:
            return None

        # dequeue the worker object
        return super( WorkerFIFO, self ).remove( task_id )


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
