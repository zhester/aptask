#!/usr/bin/env python

"""
Development Testing Task
"""


import time

import task


class DevTask( task.Task ):

    def abort( self ):
        self.report.status = task.Report.DONE
        return self.report

    def getargs( self ):
        return [
            {
                "name" : "devarg",
                "default" : 42
            }
        ]

    def initialize( self ):
        self.report.progress = 0.0
        self.report.status = task.Report.INIT
        return self.report

    def process( self ):
        if self.report.progress >= 1.0:
            self.report.status = task.Report.DONE
        else:
            time.sleep( 0.25 )
            self.report.progress += 0.1
            self.report.status = task.Report.RUNNING
        return self.report
