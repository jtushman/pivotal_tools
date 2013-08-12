#!/usr/bin/env python
"""Pivotal Tools

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


Usage:
  pivotal_tools generate_readme [--project-index=<pi>]
  pivotal_tools generate_changelog [--project-index=<pi>]
  pivotal_tools show_stories [--project-index=<pi>] [--for=<user_name>] [--number=<number_of_stories>]
  pivotal_tools show_story <story_id> [--project-index=<pi>]
  pivotal_tools browser_open <story_id> [--project-index=<pi>]
  pivotal_tools scrum [--project-index=<pi>]

Options:
  -h --help             Show this screen.
  --for=<user_name>     Username, or initials
  --project-index=<pi>  If you have multiple projects, this is the index that the project shows up in my prompt
                        This is useful if you do not want to be prompted, and then you can pipe the output

"""

#Core Imports
import urllib2
from urllib import quote
import xml.etree.ElementTree as ET
import os
import webbrowser
from itertools import islice


#3rd Party Imports
from docopt import docopt
from termcolor import colored

TOKEN = os.getenv('PIVOTAL_TOKEN', None)


def perform_pivotal_request(url):
    req = urllib2.Request(url, None, {'X-TrackerToken': TOKEN})
    response = urllib2.urlopen(req)
    return response


def get_story_tree(project_id, filter_string):
    story_filter = quote(filter_string, safe='')
    stories_url = "http://www.pivotaltracker.com/services/v3/projects/{}/stories?filter={}".format(project_id, story_filter)

    response = perform_pivotal_request(stories_url)
    root = ET.fromstring(response.read())
    return root


class Story(object):

    story_id = None
    name = None
    description = None
    owned_by = None
    story_type = None
    estimate = None
    state = None
    labels = ""

    @property
    def first_label(self):
        return self.labels.split(',')[0]

    @classmethod
    def from_node(cls, node):
        def parse_text(node, key):
            element = node.find(key)
            if element is not None:
                text = element.text
                if text is not None:
                    return text.strip()
                else:
                    return ''
            else:
                return ''

        def parse_int(node, key):
            element = node.find(key)
            if element is not None:
                return int(element.text)
            else:
                return None

        story = Story()
        story.story_id = parse_text(node, 'id')
        story.name = parse_text(node, 'name')
        story.owned_by = parse_text(node, 'owned_by')
        story.story_type = parse_text(node, 'story_type')
        story.state = parse_text(node, 'current_state')
        story.description = parse_text(node, 'description')
        story.estimate = parse_int(node, 'estimate')
        story.labels = parse_text(node, 'labels')
        return story


def print_stories(root):
    if len(root) > 0:
        for child in root:
            story = Story.from_node(child)
            formatted_title = "[{}] {}".format(story.story_id, story.name)[:140]

            print formatted_title
            print '-' * len(formatted_title)
            print story.description or 'No Description'
            print
            print
    else:
        print 'None'
        print


def print_stories_for_changelog(root):
    if len(root) > 0:
        for child in root:
            story = Story.from_node(child)
            story_string = ""
            if story.labels is not None and len(story.labels) > 0:
                story_string += "[{}] ".format(story.labels)

            story_string += story.name
            print '* {:14s} {}'.format('[{}]'.format(story.story_id), story_string)
    else:
        print 'None'
        print


def get_project(project_id):
    url = "http://www.pivotaltracker.com/services/v3/projects/%s" % project_id
    response = perform_pivotal_request(url)

    root = ET.fromstring(response.read())

    project = {
        'name': root.find('name').text
    }
    return project


def bold(string):
    return colored(string, 'white', attrs=['bold'])


def generate_readme(project_id):
    project = get_project(project_id)

    readme_string = 'README {}'.format(project['name'])

    print
    print readme_string
    print '=' * len(readme_string)
    print

    print bold('New Features')
    print bold('============')
    print

    feature_root = get_story_tree(project_id, 'state:delivered,finished type:feature')
    print_stories(feature_root)


    print 'Bugs Fixed'
    print '=========='
    print

    bug_root = get_story_tree(project_id, 'state:delivered,finished type:bug')
    print_stories(bug_root)

    print 'Known Issues'
    print '=========='
    bug_root = get_story_tree(project_id, 'state:unscheduled,unstarted,started,rejected type:bug')
    print_stories_for_changelog(bug_root)


def generate_changelog(project_id):
    project = get_project(project_id)

    title_string = 'Changes {}'.format(project['name'])

    print
    print bold(title_string)
    print bold('=' * len(title_string))
    print

    print bold('New Features')
    print bold('============')
    feature_root = get_story_tree(project_id, 'state:delivered,finished type:feature')
    features_by_tag = get_stories_by_label(feature_root)

    for label in features_by_tag:
        print bold(label.title())
        for story in features_by_tag[label]:
            print '    * {:14s} {}'.format('[{}]'.format(story.story_id), story.name)

    #print_stories_for_changelog(feature_root)


    print
    print bold('Bugs Fixed')
    print bold('==========')
    bug_root = get_story_tree(project_id, 'state:delivered,finished type:bug')
    print_stories_for_changelog(bug_root)

    print
    print bold('Known Issues')
    print bold('==========')
    issues_root = get_story_tree(project_id, 'state:unscheduled,unstarted,started,rejected type:bug')
    print_stories_for_changelog(issues_root)


def list_projects():
    projects_url = 'http://www.pivotaltracker.com/services/v3/projects'
    response = perform_pivotal_request(projects_url)
    root = ET.fromstring(response.read())

    i = 0
    for child in root:
        i += 1
        project_name = child.find('name').text
        project_id = child.find('id').text
        print "[{}] {}".format(i, project_name)


def get_project_by_index(index):
    projects_url = 'http://www.pivotaltracker.com/services/v3/projects'
    response = perform_pivotal_request(projects_url)
    root = ET.fromstring(response.read())
    return root[index].find('id').text


def prompt_project(arguments):

    if arguments['--project-index'] is not None:
        try:
            project = get_project_by_index(int(arguments['--project-index']) - 1)
            return project
        except:
            print 'Yikes, that did not work -- try again?'
            exit()

    while True:
        print "Select a Project:"
        list_projects()
        s = raw_input('>> ')

        try:
           project = get_project_by_index(int(s) - 1)
        except:
            print 'Hmmm, that did not work -- try again?'
            continue

        break

    return project


def check_api_token():
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
    if full_name is not None and len(full_name) > 0:
        return ''.join([s[0] for s in full_name.split(' ')]).upper()
    else:
        return ''


def estimate_visual(estimate):
    if estimate is not None:
        return '[{:8s}]'.format('*' * estimate)
    else:
        return '[        ]'


def list_stories(project_id, arguments):
    search_string = 'state:unscheduled,unstarted,rejected,started'
    if arguments['--for'] is not None:
        search_string += " owner:{}".format(arguments['--for'])

    stories_root = get_story_tree(project_id, search_string)


    number_of_stories = 20
    if arguments['--number'] is not None:
        number_of_stories = int(arguments['--number'])
    else:
        print
        print "Showing the top 20 stories, if you want to show more, specify number with the --number option"
        print


    if len(stories_root) == 0:
        print "None"
    else:
        for child in islice(stories_root, number_of_stories):
            story = Story.from_node(child)
            print '{:14s}{:4s}{:9s}{:13s}{:10s} {}'.format('#{}'.format(story.story_id),
                                                       initials(story.owned_by),
                                                       story.story_type,
                                                       story.state,
                                                       estimate_visual(story.estimate),
                                                       story.name)


def find_project_for_story(story_id, arguments):
    project_id = None
    if arguments['--project-index'] is not None:
        try:
            project_id = get_project_by_index(int(arguments['--project-index']) - 1)
        except:
            pass

    if project_id is not None:
        return project_id
    else:
        # Loop thorugh your projects to try to find the project where the story is:
        projects_url = 'http://www.pivotaltracker.com/services/v3/projects'
        response = perform_pivotal_request(projects_url)
        root = ET.fromstring(response.read())
        for project_node in root:
            project_id = project_node.find('id').text

            try:
                story_url = "http://www.pivotaltracker.com/services/v3/projects/{}/stories/{}".format(project_id, story_id)
                response = perform_pivotal_request(story_url)
            except urllib2.HTTPError, e:
                if e.code == 404:
                    continue
                else:
                    raise e

            if response is not None:
                return project_id
        else:
            print "Could not find story"
            exit()


def browser_open(story_id, arguments):

    project_id = find_project_for_story(story_id, arguments)
    story_url = "https://www.pivotaltracker.com/s/projects/{}/stories/{}".format(project_id, story_id)
    webbrowser.open(story_url)


def show_story(story_id, arguments):
    project_id = find_project_for_story(story_id, arguments)
    story_url = "http://www.pivotaltracker.com/services/v3/projects/{}/stories/{}".format(project_id,story_id)
    resposne = perform_pivotal_request(story_url)
    #print resposne.read()
    root = ET.fromstring(resposne.read())
    story = Story.from_node(root)

    print
    print colored('{:12s}{:4s}{:9s}{:10s} {}'.format('#{}'.format(story.story_id),
                                                     initials(story.owned_by),
                                                     story.story_type,
                                                     estimate_visual(story.estimate),
                                                     story.name), 'white', attrs=['bold'])
    print
    print colored("Story Url: ", 'white', attrs=['bold']) + colored(story_url, 'blue', attrs=['underline'])
    print colored("Description: ", 'white', attrs=['bold']) + story.description


    notes = root.find('notes')
    if notes is not None:
        print
        print colored("Notes:",'white', attrs=['bold'])
        for note in notes:
            text = note.find('text').text
            author = note.find('author').text
            print "[{}] {}".format(initials(author), text)

    attachments = root.find('attachments')
    if attachments is not None:
        print
        print colored("Attachments:",'white', attrs=['bold'])
        for attachment in attachments:
            description = attachment.find('description').text
            location = attachment.find('url').text
            print "{} {}".format(description, colored(location,'blue',attrs=['underline']))

    print


def get_stories_by_owner(stories_root):
    stories_by_owner = {}
    for story_node in stories_root:
        story = Story.from_node(story_node)
        owner_node = story_node.find('owned_by')
        if owner_node is not None:
            owner_full_name = owner_node.text
            if owner_full_name in stories_by_owner:
                stories_by_owner[owner_full_name].append(story)
            else:
                stories_by_owner[owner_full_name] = [story]
        else:
            continue
    return stories_by_owner


def get_stories_by_label(stories_root):
    stories = {}
    for story_node in stories_root:
        story = Story.from_node(story_node)
        label = story.first_label or 'Other'
        if label in stories:
            stories[label].append(story)
        else:
            stories[label] = [story]

    return stories

def pretty_date():
    from datetime import datetime
    return datetime.now().strftime('%b %d, %Y')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def scrum(project_id):
    search_string = 'state:started,rejected'
    project = get_project(project_id)
    stories_root = get_story_tree(project_id, search_string)
    stories_by_owner = get_stories_by_owner(stories_root)

    print bold("{} SCRUM -- {}".format(project['name'], pretty_date()))
    print

    for owner in stories_by_owner:
        print colored(owner, 'white', attrs=['bold'])
        for story in stories_by_owner[owner]:
            print "   #{:12s}{:9s} {:7s} {}".format(story.story_id,
                                              estimate_visual(story.estimate),
                                              story.story_type,
                                              story.name)

def main():
    clear()
    check_api_token()
    arguments = docopt(__doc__)
    if arguments['generate_readme']:
        project_id = prompt_project(arguments)
        generate_readme(project_id)
    elif arguments['generate_changelog']:
        project_id = prompt_project(arguments)
        generate_changelog(project_id)
    elif arguments['show_stories']:
        project_id = prompt_project(arguments)
        list_stories(project_id, arguments)
    elif arguments['show_story']:
        show_story(arguments['<story_id>'], arguments)
    elif arguments['browser_open']:
        browser_open(arguments['<story_id>'], arguments)
    elif arguments['scrum']:
        project_id = prompt_project(arguments)
        scrum(project_id)
    else:
        print arguments


if __name__ == '__main__':
    main()
