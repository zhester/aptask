#=============================================================================
#
# Task Execution Group Management
#
#=============================================================================

"""
Task Execution Group Management
===============================

Task groups provide isolation between different applications/teams/users
within the same aptask service.  All conforming clients should specify a
request key string.  This key string is used to identify the group for which
to manage task execution/monitoring.
"""


#=============================================================================
class Group( object ):
    """
    Group data object
    """


    #=========================================================================
    def __init__( self, name ):
        """
        Initializes a Group object.

        @param name The name of the group as a string
        """

        # The name of the group.
        self.name = name

        # List of job IDs that belong to this group.
        self._jobs = list()

        # List of task IDs that belong to this group.
        self._tasks = list()


    #=========================================================================
    def __contains__( self, jobid ):
        """
        Supports `in` queries for jobs in the group.

        @param jobid The ID of the job to test for existence
        @return      True if this group has the given job ID
        """
        return jobid in self._jobs


    #=========================================================================
    def __str__( self ):
        """
        Returns a string representing the group.

        @return A string representing the group
        """
        return '"{}" : {{ "tasks" : [{}], "jobs" : [{}] }}'.format(
            self.name,
            ','.join( str( t ) for t in self._tasks ),
            ','.join( '"{}"'.format( g ) for g in self._jobs )
        )


    #=========================================================================
    def addjob( self, jobid ):
        """
        Adds a job to the group.

        @param jobid The job ID to add to the group
        @throws      ValueError if the job ID is already present
        """
        if jobid in self._jobs:
            raise ValueError(
                'Unable to add duplicate job ID: {}'.format( jobid )
            )
        self._jobs.append( jobid )


    #=========================================================================
    def addtask( self, taskid ):
        """
        Adds a task to the group.

        @param taskid The task ID to add to the group
        @throws       ValueError if the task ID is already present
        """
        if taskid in self._tasks:
            raise ValueError(
                'Unable to add duplicate task ID: {}'.format( taskid )
            )
        self._tasks.append( taskid )


    #=========================================================================
    def clear( self ):
        """
        Removes all tracked information from the group.
        """
        self._jobs  = list()
        self._tasks = list()


    #=========================================================================
    def removejob( self, jobid ):
        """
        Removes a job from the group.

        @param jobid The job ID to remove from the group
        @throws      ValueError if the job ID does not exist
        """
        if jobid not in self._jobs:
            raise ValueError(
                'Unable to remove unknown job ID: {}'.format( jobid )
            )
        self._jobs.remove( jobid )


    #=========================================================================
    def removetask( self, taskid ):
        """
        Removes a task from the group.

        @param taskid The task ID to add to the group
        @throws       ValueError if the task ID does not exist
        """
        if taskid not in self._tasks:
            raise ValueError(
                'Unable to remove unknown task ID: {}'.format( taskid )
            )
        self._tasks.remove( taskid )


#=============================================================================
class Manager( object ):
    """
    Group management system
    """


    #=========================================================================
    NONEKEY = '__nonekey__'
    SYSKEY  = '__syskey__'


    #=========================================================================
    def __init__( self ):
        """
        Initializes a Manager object.
        """

        # Initialize the groups management dictionary.
        self._groups = dict(
            ( self.NONEKEY, Group() ),
            ( self.SYSKEY,  Group() )
        )


    #=========================================================================
    def __delitem__( self, name ):
        """
        Provides subscript notation to remove individual groups.

        @param name The name of the group to remove
        @throws     KeyError if the group is unknown or protected
        """

        # Catch attempts to remove one of the internal groups.
        if name.startswith( '__' ) and name.endswidth( '__' ):
            raise KeyError(
                'Unable to remove protected group: {}'.format( name )
            )

        # Remove the group from the dictionary.
        del self._groups[ name ]


    #=========================================================================
    def __getitem__( self, name ):
        """
        Provides subscript notation to access individual groups.

        @param name The name of the group to retrieve
        @return     The requested Group instance
        @throws     KeyError if the group is unknown
        """

        # Catch unknown group names to give a better exception message.
        if name not in self._groups:
            raise KeyError( 'Unknown group name: {}'.format( name ) )

        # Return the group's data object.
        return self._groups[ name ]


    #=========================================================================
    def __iter__( self ):
        """
        Produces an iterator for each group in the manager.  The group manager
        quacks like a dictionary, and iterates through all group names (keys)
        rather than the group objects.

        @return The iterable object for all (user) groups
        """

        # Generate all group names.
        for name in self.keys():
            yield name


    #=========================================================================
    def __len__( self ):
        """
        Returns the number of (user) groups in the manager.

        @return The number of (user) groups in the manager
        """

        # Do not include the internal groups in the total.
        return len( self._groups ) - 2


    #=========================================================================
    def __setitem__( self, name, group ):
        """
        Provides subscript notation to add/update individual groups.

        @param name  The name of the group to add/update
        @param group The group instance to set for this group
        @throws      ValueError if the group is not a Group instance
        @throws      KeyError if the group is protected
        """

        # Check for invalid group object.
        if isinstance( group, Group ) == False:
            raise ValueError(
                'Group must be an instance of Group, {} given.'.format(
                    type( group )
                )
            )

        # Invalid group name.
        if name.startswith( '__' ) and name.endswidth( '__' ):
            raise KeyError(
                'Unable to replace protected group: {}'.format( name )
            )

        # Check group instance integrity.
        if group.name != name:
            raise ValueError(
                "Group name mismatch: '{}' != '{}'".format( group.name, name )
            )

        # Replace the group object in the manager.
        self._groups[ name ] = group


    #=========================================================================
    def __str__( self ):
        """
        Converts the group manager content to a string.

        @return A string representing all (user) groups in the manager.
        """

        # Set the group format string.
        fmt = '"{0}" : {{ {1} }}'

        # List of name, list group pairs.
        pairs = []

        # Iterate through normal groups.
        for name, group in self.items():

            # Format the pair string, append to list of pairs.
            pairs.append(
                fmt.format( name, ','.join( str( g ) for g in group ) )
            )

        # Return a string describing all groups.
        return ', '.join( pairs )


    #=========================================================================
    def clear( self ):
        """
        Removes all (user) groups from the manager.
        """
        for name in self.iterkeys():
            del self._groups[ name ]


    #=========================================================================
    def items( self ):
        """
        Returns a list of (user) group name-object pairs.

        @return A list of (user) group name-object pairs
        """
        items = []
        for name in self.iterkeys():
            items.append( ( name, self._groups[ name ] ) )
        return items


    #=========================================================================
    def iteritems( self ):
        """
        Returns an iterable object for the name-object pairs.

        @return An iterable object for the name-object pairs
        """
        for name in self.iterkeys():
            yield ( name, self._groups[ name ] )


    #=========================================================================
    def iterkeys( self ):
        """
        Returns an iterable object for all (user) group names

        @return An iterable object for all (user) group names
        """

        # Tuple of all keys to skip.
        skip = ( self.NONEKEY, self.SYSKEY )

        # Iterate through the group dictionary keys.
        for name in self._groups.iterkeys():

            # Do not yield internal group names.
            if name in skip:
                continue

            # Yield all user group names.
            yield name


    #=========================================================================
    def keys( self ):
        """
        Returns a list of all (user) groups in the manager.

        @return A list of all (user) groups in the manager
        """

        # Return list of user group names.
        return list( self.iterkeys() )

