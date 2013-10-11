#!/usr/bin/env python
##############################################################################
#
# worker.py
#
##############################################################################


import Queue


import manager
import task


#=============================================================================
STATUS_INIT    = 0                  # worker is initializing task
STATUS_RUNNING = 1                  # task is executing as normal
STATUS_DONE    = 2                  # task is done executing
STATUS_ERROR   = 99                 # worker encountered an error


#=============================================================================
def create_task_descriptor( name, arguments ):
    """
    Decouples the structure of a task descriptor from code outside this
    module.  Don't count on the returned object having a consistent type or
    format.
    @param name         Task identifier
    @param arguments    Arguments to pass to the task
    """

    # for now, just use a dict
    return { 'name' : name, 'args' : arguments }


#=============================================================================
def worker( command_queue, status_queue, task_descriptor ):
    """
    Function to execute as a worker process.
    @param
    @param
    @param
    """

    command  = None
    message  = None
    progress = 0.0
    status   = INIT

    try:
        tsk = _create_task( task_descriptor )
    except ValueErrer:
        status = ERROR


    # ZIH - not sure this is the best pattern
    #  init, proc
    # some things are run with no control or monitoring
    # some things have no control, but can be monitored
    #
    # some things are run in steps with control and monitoring

    # incremental   monitorable   abortable
    # -----------   -----------   ---------
    #


    tsk.start()

    while progress < 1.0:

        try:
            command = command_queue.get_nowait()
            if command is not None:
                command_id, = command
                if command_id == manager.CMD_ABORT:
                    tsk.abort()
        except Queue.Empty:
            # if the queue is empty, continue processing/updating
            pass

        # update task execution progress
        progress = tsk.get_progress()

        try:
            # send status and progress to manager
            status_queue.put_nowait( ( status, progress, message ) )
        except Queue.Full:
            # if the queue is full, try again next time
            pass


#=============================================================================
def _create_task( descriptor ):
    """
    Creates a task object from a descriptor.
    @param descriptor   Task descriptor
    @return             Task instance
    @throws ValueError  When the descriptor can not be resolved
    """

    # ZIH - implement me!
    return task.task()


#=============================================================================
def main( argv ):
    """
    Script execution entry point
    @param argv         Arguments passed to the script
    @return             Exit code (0 = success)
    """



    # return success
    return 0

#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

