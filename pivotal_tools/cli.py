#!/usr/bin/env python
"""Pivotal Tools

A collection of tools to help with your pivotal workflow


changelog
---------------
List out projects stories that are delivered or finished (not accepted)

show stories
---------------
Lists all stories for a given project (will prompt you if not specified)
Can filter by user with the `for` option
By default show the top 20 stories, can specify more (or less) with the _number_ option

show story
---------------
Show the details for a given story.  passing the project-index parameter will make it faster

open
---------------
Will open the given story in a browser.  passing the project-index parameter will make it faster

scrum
---------------
Will list stories and bugs that team members are working on.  Grouped by team member

poker (aka planning)
---------------
Help to facilitate a planning poker session

create (feature|bug|chore)
---------------
Create a story


Usage:
  pivotal_tools create (feature|bug|chore) <title> [<description>] [--project-index=<pi>]
  pivotal_tools (start|finish|deliver|accept|reject) story <story_id> [--project-index=<pi>]
  pivotal_tools show stories [--project-index=<pi>] [--for=<user_name>] [--number=<number_of_stories>]
  pivotal_tools show story <story_id> [--project-index=<pi>]
  pivotal_tools open <story_id> [--project-index=<pi>]
  pivotal_tools changelog [--project-index=<pi>]
  pivotal_tools scrum [--project-index=<pi>]
  pivotal_tools (planning|poker) [--project-index=<pi>]

Options:
  -h --help             Show this screen.
  --for=<user_name>     Username, or initials
  --project-index=<pi>  If you have multiple projects, this is the index that the project shows up in my prompt
                        This is useful if you do not want to be prompted, and then you can pipe the output

"""

#Core Imports
import os
import webbrowser
from itertools import islice


#3rd Party Imports
from docopt import docopt
from termcolor import colored

from pivotal import Project, Story, InvalidStateException


## Main Methods



def generate_changelog(project):
    """Generate a Changelog for the current project.  It is grouped into 3 sections:
    * New Features
    * Bugs Fixed
    * Known Issues

    The new features section is grouped by label for easy comprehension
    """

    title_string = 'Change Log {}'.format(project.name)

    print
    print bold(title_string)
    print bold('=' * len(title_string))
    print

    print bold('New Features')
    print bold('============')

    finished_features = project.finished_features()
    features_by_label = group_stories_by_label(finished_features)

    for label in features_by_label:
        if len(label) == 0:
            display_label = 'Other'
        else:
            display_label = label
        print bold(display_label.title())
        for story in features_by_label[label]:
            print '    * {:14s} {}'.format('[{}]'.format(story.story_id), story.name)


    def print_stories(stories):
        if len(stories) > 0:
            for story in stories:
                story_string = ""
                if story.labels is not None and len(story.labels) > 0:
                    story_string += "[{}] ".format(story.labels)

                story_string += story.name
                print '* {:14s} {}'.format('[{}]'.format(story.story_id), story_string)
        else:
            print 'None'
            print


    print
    print bold('Bugs Fixed')
    print bold('==========')
    print_stories(project.finished_bugs())

    print
    print bold('Known Issues')
    print bold('==========')
    print_stories(project.known_issues())

    print


def show_stories(project, arguments):
    """Shows the top stories
    By default it will show the top 20.  But that change be changed by the --number arguement
    You can further filter the list by passing the --for argument and pass the initials of the user
    """

    search_string = 'state:unscheduled,unstarted,rejected,started'
    if arguments['--for'] is not None:
        search_string += " owner:{}".format(arguments['--for'])

    stories = project.get_stories(search_string)

    number_of_stories = 20
    if arguments['--number'] is not None:
        number_of_stories = int(arguments['--number'])
    else:
        print
        print "Showing the top 20 stories, if you want to show more, specify number with the --number option"
        print


    if len(stories) == 0:
        print "None"
    else:
        for story in islice(stories, number_of_stories):
            print '{:14s}{:4s}{:9s}{:13s}{:10s} {}'.format('#{}'.format(story.story_id),
                                                           initials(story.owned_by),
                                                           story.story_type,
                                                           story.state,
                                                           estimate_visual(story.estimate),
                                                           story.name)


def show_story(story_id, arguments):
    """Shows the Details for a single story

    Will find the associate project, then look up the story and print of the details
    """

    story = load_story(story_id, arguments)


    print
    print colored('{:12s}{:4s}{:9s}{:10s} {}'.format('#{}'.format(story.story_id),
                                                     initials(story.owned_by),
                                                     story.story_type,
                                                     estimate_visual(story.estimate),
                                                     story.name), 'white', attrs=['bold'])
    print
    print colored("Story Url: ", 'white', attrs=['bold']) + colored(story.url, 'blue', attrs=['underline'])
    print colored("Description: ", 'white', attrs=['bold']) + story.description

    if len(story.notes) > 0:
        print
        print bold("Notes:")
        for note in story.notes:
            print "[{}] {}".format(initials(note.author), note.text)


    if len(story.tasks) > 0:
        print
        print bold("Tasks:")
        for task in story.tasks:
            print "[{}] {}".format(x_or_space(task.complete), task.description)

    if len(story.attachments) > 0:
        print
        print bold("Attachments:")
        for attachment in story.attachments:
            print "{} {}".format(attachment.description, colored(attachment.url,'blue',attrs=['underline']))

    print


def scrum(project):
    """ CLI Visual Aid for running the daily SCRUM meeting.
        Prints an list of stories that people are working on grouped by user
    """

    stories = project.in_progress_stories()
    stories_by_owner = group_stories_by_owner(stories)

    print bold("{} SCRUM -- {}".format(project.name, pretty_date()))
    print

    for owner in stories_by_owner:
        print bold(owner)
        for story in stories_by_owner[owner]:
            print "   #{:12s}{:9s} {:7s} {}".format(story.story_id,
                                                    estimate_visual(story.estimate),
                                                    story.story_type,
                                                    story.name)

        print

    print bold("Bugs")
    bugs = project.open_bugs()
    if len(bugs) == 0:
        print 'Not sure that I believe it, but there are no bugs'
    for bug in bugs:
        print "   #{:12s} {:4s} {}".format(bug.story_id,
                                     initials(bug.owned_by),
                                     bug.name)


def poker(project):
    """CLI driven tool to help facilitate the periodic poker planning session

    Will loop through and display unestimated stories, and prompt the team for an estimate.
    You can also open the current story in a browser for additional editing
    """
    total_stories = len(project.unestimated_stories())
    for idx, story in enumerate(project.unestimated_stories()):
        clear()
        rows, cols = _get_column_dimensions()
        print "{} PLANNING POKER SESSION [{}]".format(project.name.upper(), bold("{}/{} Stories Estimated".format(idx+1, total_stories)))
        print "-" * cols
        pretty_print_story(story)
        prompt_estimation(project, story)
    else:
        print "KaBoom!!! Nice Work Team"


def load_story(story_id, arguments):
    story = None
    if arguments['--project-index'] is not None and arguments['--project-index'].isdigit():
        idx = int(arguments['--project-index']) - 1
        story = Story.find(story_id, project_index=idx)
    else:

        story = Story.find(story_id)
    return story


def browser_open(story_id, arguments):
    """Open the given story in a browser"""

    story = load_story(story_id, arguments)

    webbrowser.open(story.url)

def create_story(project, arguments):

    story = dict()
    story['name'] = arguments['<title>']
    if '<description>' in arguments:
        story['description'] = arguments['<description>']

    if arguments['bug']:
        story['story_type'] = 'bug'
    elif arguments['feature']:
        story['story_type'] = 'feature'
    elif arguments['chore']:
        story['story_type'] = 'chore'

    stories = {'story': story}

    project.create_story(stories)


def update_status(arguments):

    story = None
    if '<story_id>' in arguments:
        story_id = arguments['<story_id>']
        story = load_story(story_id, arguments)

    if story is not None:
        try:

            if arguments['start']:
                story.start()
                print "Story: [{}] {} is STARTED".format(story.story_id, story.name)
            elif arguments['finish']:
                story.finish()
                print "Story: [{}] {} is FINISHED".format(story.story_id, story.name)
            elif arguments['deliver']:
                story.deliver()
                print "Story: [{}] {} is DELIVERED".format(story.story_id, story.name)
            elif arguments['accept']:
                story.accept()
                print "Story: [{}] {} is ACCEPTED".format(story.story_id, story.name)
            elif arguments['reject']:
                story.reject()
                print "Story: [{}] {} is REJECTED".format(story.story_id, story.name)

        except InvalidStateException, e:
            print e.message
    else:
        print "hmmm could not find story"



## Helper Methods



def bold(string):
    return colored(string, 'white', attrs=['bold'])


def prompt_project(arguments):
    """prompts the user for a project, if not passed in as a argument"""
    projects = Project.all()

    # Do not prompt -- and auto select the one project if a account only has one project
    if len(projects) == 1:
        return projects[0]

    if arguments['--project-index'] is not None:
        try:
            idx = int(arguments['--project-index']) - 1
            project = projects[idx]
            return project
        except:
            print 'Yikes, that did not work -- try again?'
            exit()

    while True:
        print "Select a Project:"
        for idx, project in enumerate(projects):
            print "[{}] {}".format(idx+1, project.name)
        s = raw_input('>> ')

        try:
            project = projects[int(s) - 1]
        except:
            print 'Hmmm, that did not work -- try again?'
            continue

        break

    return project


def check_api_token():
    """Check to see if the API Token is set, else give instructions"""

    token = os.getenv('PIVOTAL_TOKEN', None)
    if token is None:
        print """
        You need to have your pivotal developer token set to the 'PIVOTAL_TOKEN' env variable.

        I keep mine in ~/.zshenv
        export PIVOTAL_TOKEN='your token'

        If you do not have one, login to pivotal, and go to your profile page, and scroll to the bottom.
        You'll find it there.
        """
        exit()


def initials(full_name):
    """Return the initials of a passed in name"""

    if full_name is not None and len(full_name) > 0:
        return ''.join([s[0] for s in full_name.split(' ')]).upper()
    else:
        return ''


def estimate_visual(estimate):
    if estimate is not None:
        return '[{:8s}]'.format('*' * estimate)
    else:
        return '[        ]'


def group_stories_by_owner(stories):
    stories_by_owner = {}
    for story in stories:
        if story.owned_by is not None:
            if story.owned_by in stories_by_owner:
                stories_by_owner[story.owned_by].append(story)
            else:
                stories_by_owner[story.owned_by] = [story]
        else:
            continue
    return stories_by_owner


def group_stories_by_label(stories):
    stories_by_label = {}
    for story in stories:
        if story.first_label in stories_by_label:
            stories_by_label[story.first_label].append(story)
        else:
            stories_by_label[story.first_label] = [story]

    return stories_by_label


def pretty_date():
    from datetime import datetime
    return datetime.now().strftime('%b %d, %Y')


def clear():
    """Clears the terminal buffer"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pretty_print_story(story):
    print
    print bold(story.name)
    if len(story.description) > 0:
        print
        print story.description
        print

    if len(story.notes) > 0:
        print
        print bold('Notes:')
        for note in story.notes:
            print "[{}] {}".format(initials(note.author), note.text)

    if len(story.attachments) > 0:
        print
        print bold('Attachments:')
        for attachment in story.attachments:
            if len(attachment.description) > 0:
                print "Description: {}".format(attachment.description)
            print "Url: {}".format(colored(attachment.url, 'blue'))


    if len(story.tasks) > 0:
        print
        print bold("Tasks:")
        for task in story.tasks:
            print "[{}] {}".format(x_or_space(task.complete), task.description)

    if len(story.labels) > 0:
        print
        print "{} {}".format(bold('Labels:'), story.labels)


def prompt_estimation(project, story):
    print
    print bold("Estimate: [{}, (s)kip, (o)pen, (q)uit]".format(','.join(project.point_scale)))
    input_value = raw_input(bold('>> '))

    if input_value in ['s', 'S']:
        #skip move to the next
        return
    elif input_value in ['o', 'O']:
        webbrowser.open(story.url)
        prompt_estimation(project, story)
    elif input_value in ['q','Q']:
        exit()
    elif input_value in project.point_scale:
        value = int(input_value)
        story.assign_estimate(value)
    else:
        print "Invalid Input, Try again"
        prompt_estimation(project, story)


def _get_column_dimensions():
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(rows), int(cols)


def x_or_space(complete):
    if complete:
        return 'X'
    else:
        return ' '


def main():

    arguments = docopt(__doc__)

    check_api_token()

    if arguments['changelog']:
        project = prompt_project(arguments)
        generate_changelog(project)
    elif arguments['show'] and arguments['stories']:
        project = prompt_project(arguments)
        show_stories(project, arguments)
    elif arguments['show'] and arguments['story']:
        show_story(arguments['<story_id>'], arguments)
    elif arguments['open']:
        browser_open(arguments['<story_id>'], arguments)
    elif arguments['scrum']:
        project = prompt_project(arguments)
        scrum(project)
    elif arguments['poker'] or arguments['planning']:
        project = prompt_project(arguments)
        poker(project)
    elif arguments['create']:
        project = prompt_project(arguments)
        create_story(project, arguments)
    elif arguments['story']:
        update_status(arguments)
    else:
        print arguments


if __name__ == '__main__':
    main()
