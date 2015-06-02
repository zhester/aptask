#!/usr/bin/env python

"""
Development Testing Task
"""


import time

import task


class DevTask( task.Task ):
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
        self.report.status = task.Report.DONE
        return self.report

    def initialize( self ):
        self.report.progress = 0.0
        self.report.status = task.Report.INIT
        self.report.message = 'devtask with devarg: %d' \
            % self.arguments[ 'devarg' ]
        return self.report

    def process( self ):
        if self.report.progress >= 1.0:
            self.report.status = task.Report.DONE
        else:
            time.sleep( 5.0 )
            self.report.progress += 0.1
            self.report.status = task.Report.RUNNING
        return self.report

