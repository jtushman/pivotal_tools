from __future__ import unicode_literals
from datetime import datetime

import factory

from pivotal_tools import cli


class StoryFactory(factory.StubFactory):
    story_id = '42'
    project_id = '43'
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


def test_scrum(monkeypatch):
    monkeypatch.setattr(cli, 'pretty_date', lambda: 'Oct 27, 2013')
    assert (
        cli.scrum('Test', [StoryFactory()], [StoryFactory()])
        == ['\x1b[1m\x1b[37mTest SCRUM -- Oct 27, 2013\x1b[0m',
            '',
            '\x1b[1m\x1b[37mSome P\xf8rson\x1b[0m',
            '   #42          [*       ] bug     F\xf8\xf8',
            '',
            '\x1b[1m\x1b[37mBugs\x1b[0m',
            '   #42           SP   F\xf8\xf8']
    )


def test_decode_dict():
    assert cli.decode_dict(dict(a=b'\xc3\xb8'), 'utf-8') == dict(a='\xf8')
