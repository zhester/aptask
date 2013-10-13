#!/usr/bin/env python
##############################################################################
#
# worker.py
#
##############################################################################


"""
This module contains the interface to running a worker process.
"""


import Queue


import task


#=============================================================================
class Command( object ):
    """
    Worker control command.
    """


    #=========================================================================
    CONTINUE = 0
    ABORT    = 1


    #=========================================================================
    def __init__( self, command_id = Command.CONTINUE ):
        """
        Constructor.
        @param command_id
                        Command identifier
        """

        self.id = command_id



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

    command = None
    report  = None

    # create the task object according to the descriptor
    tsk = _create_task( task_descriptor )

    # initialize task
    #   some tasks will initialize here and start processing later
    #   some tasks will block here until complete
    #   some tasks won't implement this
    try:
        report = tsk.initialize()
    except task.NotSupported:
        pass

    # loop until the task reports completion
    while report.is_done() == False:

        # check for any pending messages
        try:
            command = command_queue.get_nowait()
        except Queue.Empty:
            # if the queue is empty, continue processing/updating
            pass
        else:
            if command is not None:
                if command.id == Command.ABORT:
                    try:
                        report = tsk.abort()
                    except task.NotSupported:
                        pass
                    # ZIH - we're putting too much trust in the driver to
                    #  set the done status here... we should keep some local
                    # state and time out if we keep processing

        # spend time executing task
        try:
            report = tsk.process()
        except task.NotSupported:
            pass

        # send status and progress to manager
        try:
            status_queue.put_nowait( report )
            # ZIH - i don't like the manager having to know anything about the
            #   task module... might want to repackage the data
        except Queue.Full:
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
    return task.Task()


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

