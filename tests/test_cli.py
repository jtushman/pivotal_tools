from __future__ import unicode_literals

import factory

from pivotal_tools import cli


class TestProject(object):
    def __init__(self, stories):
        self.stories = stories

    def get_stories(self, pattern):
        return self.stories


class StoryFactory(factory.StubFactory):
    story_id = 42
    project_id = 43
    name = 'F\xf8\xf8'
    description = 'F\xf8\xf8 is a thing'
    owned_by = 'Some P\xf8rson'
    story_type = 'bug'
    estimate = 1
    state = 'started'
    url = 'http://example.com'
    labels = None


def test_stories():
    cli.show_stories(TestProject([StoryFactory()]),
                     {'--for': None, '--number': 2})


def test_decode_dict():
    assert cli.decode_dict(dict(a=b'\xc3\xb8'), 'utf-8') == dict(a='\xf8')
