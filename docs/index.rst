pivotal_tools v0.14
===================

pivotal_tools is a geeky command-line interface with additional scrum, planning
poker, and changelog generation features.

`Blog post on its usage`_

.. _Blog post on its usage: http://jtushman.github.io/blog/2013/08/15/introducing-pivotal-tools/


Installation
------------

::

    pip install pivotal_tools

Add :envvar:`PIVOTAL_TOKEN` to your environment.

If you use zsh, you could put it in :file:`~/.zshenv`, like so::

    export PIVOTAL_TOKEN='your token'

Also make sure in your pivotal project settings that you have "Allow API
Access" checked (currently the default behavior).

Usage
-----

Options accepted by all commands
""""""""""""""""""""""""""""""""

All commands take the following options:

:option:`--project-index`
    If you have multiple projects, this is the index that the project shows up
    in my prompt. This is useful if you do not want to be prompted, and then
    you can pipe the output. Passing this parameter will make everything
    faster.

Commands
""""""""

changelog
^^^^^^^^^

List out projects stories that are delivered or finished (not accepted)

show stories
^^^^^^^^^^^^

Lists all stories for a given project (will prompt you if not specified).

:option:`--for`
    Filter by the given user name.

:option:`--number`
    Number of stories to show. Defaults to 20.

show story <story_id>
^^^^^^^^^^^^^^^^^^^^^

::

    pivotal_tools show story <story_id>

Show the details for a given story.

open <story_id>
^^^^^^^^^^^^^^^

::

    pivotal_tools open <story_id>

Will open the given story in a browser.

scrum
^^^^^

::

    pivotal_tools scrum

Will list stories and bugs that team members are working on. Grouped by team
member.

poker or planning
^^^^^^^^^^^^^^^^^

::

    pivotal_tools poker
    pivotal_tools planning  # equivalent

Help to facilitate a planning poker session.

create
^^^^^^

::

    pivotal_tools create feature
    pivotal_tools create bug
    pivotal_tools create chore

Create a story.

<verb> story <story_id>
^^^^^^^^^^^^^^^^^^^^^^^

::

    pivotal_tools start story <story_id>
    pivotal_tools finish story <story_id>
    pivotal_tools deliver story <story_id>
    pivotal_tools accept story <story_id>
    pivotal_tools reject story <story_id>

Change the state of a story.

::

    Usage:
    pivotal_tools changelog [--project-index=<pi>]
    pivotal_tools show stories [--project-index=<pi>] [--for=<user_name>] [--number=<number_of_stories>]
    pivotal_tools show story <story_id> [--project-index=<pi>]
    pivotal_tools open <story_id> [--project-index=<pi>]
    pivotal_tools scrum [--project-index=<pi>]
    pivotal_tools poker [--project-index=<pi>]
    pivotal_tools planning [--project-index=<pi>]
    pivotal_tools create (feature|bug|chore) <title> [<description>] [--project-index=<pi>]
    pivotal_tools (start|finish|deliver|accept|reject) story <story_id> [--project-index=<pi>]

    Options:
    -h --help             Show this screen.
    --for=<user_name>     Username, or initials
    --project-index=<pi>  If you have multiple projects, this is the index that the project shows up in my prompt
                            This is useful if you do not want to be prompted, and then you can pipe the output
