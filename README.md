aptask
======

Asynchronous parallel task scheduling, execution, and monitoring.

Problem
-------

User interfaces require low latency and a lack of indeterminate blocking.
Many problems in large-scale software involve executing tasks asynchronous to
the user's workflow.  This allows the user to continue their work while they
receive updates on how the task is executing, and when it has completed.  This
problem becomes even more important when distributing long-running execution
across networks.

Proposed Solution
-----------------

This project aims to provide a solution through a network daemon that can
schedule many arbitrarty tasks without blocking the client.  This is done
through a session-less (request/response) protocol.

By implementing the "user" interface as a general-purpose network daemon,
many types of applications can take advantage of this system without any
custom library support.  Reference client implementations in Python will be
provided.

If more parallel processing is needed, more processors can be made available
(either locally, or over the network).

The types of processing that can be scheduled include external programs,
scripts, and any code that can be interpreted by Python.  For the best
possible integration, these systems should provide some sort of execution
feedback.  Native Python code and drivers for external applications can be
built on top of an existing Python class that greatly simplifies adding new
processing capabilities to the system.

Protocol
--------

Clients send and receive data using JSON messages.  Messages sent from a
client are requests.  Messages sent from a server are responses.

### User Requests ###

#### `index`: Request Supported Task List ####

    {
        "key" : "<userkey>",
        "request" : "index"
    }

#### `start`: Request New Task ####

    {
        "key" : "<userkey>",
        "request" : "start",
        "name" : "<taskname>",
        "arguments" : [ "<argument1>", "<argument2>" ]
    }

#### `stop`: Request Task Abort ####

    {
        "key" : "<userkey>",
        "request" : "stop",
        "taskid" : "<taskid>"
    }

#### `active`: Request My Active Tasks' Status ####

    {
        "key" : "<userkey>",
        "request" : "active"
    }

### Responses to User Requests ###

#### Task Index ####

    {
        "status" : "ok",
        "response" : "index",
        "index" : [
            "<taskname>" : {
                "arguments" : [
                    [ "<argument1>", "string" ],
                    [ "<argument2>", "string" ]
                ]
            }
        ]
    }

#### Start Task ####

    {
        "status" : "ok",
        "response" : "start",
        "taskid" : "<taskid>"
    }

#### Stop Task ####

    {
        "status" : "ok",
        "response" : "stop",
        "taskid" : "<taskid>"
    }

#### Show Active Tasks ####

    {
        "status" : "ok",
        "response" : "active",
        "active" : [
            {
                "taskid" : "<taskid>",
                "status" : "<status>",
                "progress" : "<progress>",
                "message" : "<message>"
            }
        ]
    }

### Admin Requests ###

### Responses to Admin Requests ###
