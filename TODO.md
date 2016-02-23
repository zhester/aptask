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
- Implement remote workers.
  - Abstract communication pipes to work over network.
- Make the client a more complete client (rather than a testing tool).
  - Add an interactive query/response interface.
- Allow worker tasks to post "results" of processing when complete.
  - These persist after the task has finished up until requested by a client.
- Build a few general-purpose task classes.
  - Run any `subprocess`-able command that is on a whitelist of commands.
  - Run any python function from a whitelist.
  - Import and run any module function (similar to `-m` for the interpreter).

