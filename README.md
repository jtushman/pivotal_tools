pivotal_tools
=============

Set of helper tools to rock your pivotal process.  On the Command Line of course


install
-------

```bash
pip install pivotal_tools
```


setup
-----
Add PIVOTAL_TOKEN to your environment

I put mine in ~/.zshenv, like so ...

`export PIVOTAL_TOKEN='your token'`

usage
-----

A collection of tools to help with your pivotal workflow

```
changelog
---------------
List out projects stories that are delivered or finished (not accepted)

show_stories
---------------
Lists all stories for a given project (will prompt you if not specified)
Can filter by user with the `for` option
By default show the top 20 stories, can specify more (or less) with the _number_ option

show_story
---------------
Show the details for a given story.  passing the project-index parameter will make it faster

browser_open
---------------
Will open the given story in a browser.  passing the project-index parameter will make it faster

scrum
---------------
Will list stories and bugs that team members are working on.  Grouped by team member

poker || planning
---------------
Help to facilitate a planning poker session


Usage:
  pivotal_tools changelog [--project-index=<pi>]
  pivotal_tools show_stories [--project-index=<pi>] [--for=<user_name>] [--number=<number_of_stories>]
  pivotal_tools show_story <story_id> [--project-index=<pi>]
  pivotal_tools browser_open <story_id> [--project-index=<pi>]
  pivotal_tools scrum [--project-index=<pi>]
  pivotal_tools poker [--project-index=<pi>]
  pivotal_tools planning [--project-index=<pi>]

Options:
  -h --help             Show this screen.
  --for=<user_name>     Username, or initials
  --project-index=<pi>  If you have multiple projects, this is the index that the project shows up in my prompt
                        This is useful if you do not want to be prompted, and then you can pipe the output
```