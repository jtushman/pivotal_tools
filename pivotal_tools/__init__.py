#!/usr/bin/env python
"""Pivotal Readme

Usage:
  pivotal_tools.py generate_readme [--project=<project_name>]

Options:
  -h --help     Show this screen.
  --project=<project_name>  Name of specific project

"""
from docopt import docopt

import urllib2
from urllib import quote
import xml.etree.ElementTree as ET
import os

PROJECT_ID = '737117'
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


def print_stories(root):
    for child in root:
        story_id = child.find('id').text
        name = child.find('name').text
        formatted_title = "[{}] {}".format(story_id, name)[:140]

        print formatted_title
        print '-' * len(formatted_title)
        print child.find('description').text or 'No Description'
        print
        print


def get_project(project_id):
    url = "http://www.pivotaltracker.com/services/v3/projects/%s" % project_id
    response = perform_pivotal_request(url)

    root = ET.fromstring(response.read())

    project = {
        'name': root.find('name').text
    }
    return project


def generate_readme(project_id):
    project = get_project(project_id)

    readme_string = 'README {}'.format(project['name'])

    print
    print readme_string
    print '=' * len(readme_string)
    print

    print 'New Features'
    print '============'
    print

    feature_root = get_story_tree(project_id, 'state:delivered,finished type:feature')
    print_stories(feature_root)


    print 'Bugs Fixed'
    print '=========='
    print

    bug_root = get_story_tree(project_id, 'state:delivered,finished type:bug')
    print_stories(bug_root)


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


def prompt_project():
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


def main():
    check_api_token()
    arguments = docopt(__doc__)
    if 'generate_readme' in arguments:
        project_id = prompt_project()
        generate_readme(project_id)
    else:
        print arguments


if __name__ == '__main__':
    main()
