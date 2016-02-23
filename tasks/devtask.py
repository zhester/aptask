#=============================================================================
#
# Development Testing Task
#
#=============================================================================


"""
Development Testing Task
========================
"""


import time

import aptask.task


class DevTask( aptask.task.Task ):
    """
    This is a task used for developmental purposes only.
    """

    @classmethod
    def getargs( cls ):
        return [
            {
                "name" : "devarg",
                "default" : 42
            }
        ]

    def abort( self ):
        self.report.status = aptask.task.Report.DONE
        return self.report

    def initialize( self ):
        self.report.progress = 0.0
        self.report.status = aptask.task.Report.INIT
        self.report.message = 'devtask with devarg: %d' \
            % self.arguments[ 'devarg' ]
        return self.report

    def process( self ):
        if self.report.progress >= 1.0:
            self.report.status = aptask.task.Report.DONE
        else:
            time.sleep( 1.0 )
            self.report.progress += 0.1
            self.report.status = aptask.task.Report.RUNNING
        return self.report

