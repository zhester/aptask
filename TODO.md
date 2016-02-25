aptask Development TODO
=======================

Documentation
-------------

- Clean up `README.md`, fill out examples.
- Add/complete docstrings throughout project.

Refactoring
-----------

- Add back the ability to set logging output to the configured log file.
- Re-evaluate all one-off modules for a more Python-ic way of doing business.
  - aptask/raqueue.py module seems to re-implement built-in functionality
    - remove() should be replaced with dict.pop()
    - __getitem__() shouldn't be used to protect (users should use .get())
    - keys should be integers
    - fifo and session subclass raqueue
      - fifo can be cleaned up/simplified
        - see if fifo is ever accessed randomly (toss it if not)
        - could be refactored into separate pending/active queues
      - session might be easier if it's just a plain dict
      - if the above two modules are unnecessary, so is raqueue
        - the biggest value is generating IDs in the add() method
        - HAHAHA: new_id = max( q.keys() ) + 1
          - more sophistication might be to avoid re-using old IDs
    - net and manager use those queues
- Re-evaluate application configuration (file format, abstraction, validity).

Features and New Development
----------------------------

### Installation, Configuration, Integration

- Create FreeBSD `rc.d` script.
- Create Linux `init.d` script.
- Create local service installation script.

### Testing

- Remove all informal test code from library modules.
- Move informal test code into unit test framework.
- Add to unit tests.
- Create a set of complete integration and regression tests.
- Check test coverage.

### New Stuff

- Implement a forceful shutdown of all workers.
- Implement parallel queue scheduling.
  - Queue is currently sequential.
  - May require notion of task dependencies (to force sequential execution).
- Build a few general-purpose task classes.
  - Run any `subprocess`-able command that is on a whitelist of commands.
  - Run any python function from a whitelist.
  - Import and run any module function (similar to `-m` for the interpreter).
- Write a stand-alone client driver for Python/WSGI applications.
- Write a PHP client driver.
- Write a JavaScript class to simplify client implementations with the
  host-side drivers.
- Make the client a more complete client (rather than a testing tool).
  - Add an interactive query/response interface.
- Allow worker tasks to post "results" of processing when complete.
  - These persist after the task has finished up until requested by a client.
- Implement remote workers.
  - Abstract communication pipes to work over network.

New Scheduling Design Notes
---------------------------

raqueue/fifo/WorkerFifo needs help.  Might be easier to implement a better
scheduling system.  Also, it's time to bring in execution dependencies (only
allowing a task to be processed if another one has completed) and priorities.

A task is now a bundle of information:

- routine: requested by the user (formerly "tasks" in the tasks directory)
- job identifier: given by the user (uniqueness for the user only)
- job dependencies: list of jobids that must finish first
- job priority: given by the user
- task identifier: assigned by the scheduler (same as task ID right now)

The scheduler then implements a single pending/inactive task queue.  The
scheduler maintains a separate active task object for each worker.  When
queried for all tasks, the scheduler reports all pending and active tasks.

The scheduler attempts to prioritize jobs if their ID ever appears in another
job's depenency list.  Otherwise, it selects jobs based on the user's
requested priorities, then by age in pending queue.

This effort will require refactoring the task module to the new routine
module.  Then, a new task module will better reflect the metaphore of a unique
execution of a routine.  The task module will implement the Queue/Scheduler
and the new Task class.  This should also simplify the manager module.

