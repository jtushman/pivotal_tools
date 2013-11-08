from __future__ import unicode_literals

import factory

from pivotal_tools import cli


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
    assert (
        cli.show_stories([StoryFactory()],
                         {'--for': None, '--number': 2})
        == ['#42           SP  bug      started      [*       ] F\xf8\xf8'])


def test_decode_dict():
    assert cli.decode_dict(dict(a=b'\xc3\xb8'), 'utf-8') == dict(a='\xf8')
