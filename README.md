pivotal_tools
=============

Set of helper tools to rock your pivotal process.  On the Command Line of course


install
-------

```bash
pip install git+ssh://git@github.com/jtushman/pivotal_tools.git
```


setup
-----
Add PIVOTAL_TOKEN to your environment

I put mine in ~/.zshenv, like so ...

`export PIVOTAL_TOKEN='your token'`

usage
-----

```bash
A collection of tools to help with your pivotal workflow

generate_readme
---------------
List out projects stories that are delivered or finished (not accepted), including description


generate_changelog
---------------
List out projects stories that are delivered or finished (not accepted), titles only

show_stories
---------------
Lists all stories for a given project (will prompt you if not specified)
Can filter by user with the `for` option
By default show the top 20 stories, can specify more (or less) with the number option

show_story
---------------
Show the details for a given story.  passing the project-index parameter will make it faster

browser_open
---------------
Will open the given story in a browser.  passing the project-index parameter will make it faster

scrum
---------------
Will list stories and bugs that team members are working on.  Grouped by team member

poker
---------------
Help to facilitate a planning poker session


Usage:
  pivotal_tools generate_readme [--project-index=<pi>]
  pivotal_tools generate_changelog [--project-index=<pi>]
  pivotal_tools show_stories [--project-index=<pi>] [--for=<user_name>] [--number=<number_of_stories>]
  pivotal_tools show_story <story_id> [--project-index=<pi>]
  pivotal_tools browser_open <story_id> [--project-index=<pi>]
  pivotal_tools scrum [--project-index=<pi>]
  pivotal_tools poker [--project-index=<pi>]

Options:
  -h --help             Show this screen.
  --for=<user_name>     Username, or initials
  --project-index=<pi>  If you have multiple projects, this is the index that the project shows up in my prompt
                        This is useful if you do not want to be prompted, and then you can pipe the output
```
