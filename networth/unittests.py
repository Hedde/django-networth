__author__ = 'heddevanderheide'

import unittest

# App specific
from networth.mixins import NetworthMixin


class TestObject(NetworthMixin):
    first_name = ''
    last_name = ''

    tags = None

    class Networth:
        fields = (
            ('first_name', (True, 1)),
            ('last_name', (lambda f: f.startswith('P'), 5)),
            ('tags', (lambda f: len(f), 'result')),
        )

    def __init__(self, **kwargs):
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.tags = filter(None, kwargs.get('tags', '').split(','))

    def add_tag(self, tag):
        if self.tags:
            self.tags.append(tag)
        else:
            self.tags = [tag]


class TestNetworthMixin(unittest.TestCase):
    def setUp(self):
        self.obj_1 = TestObject(
            first_name='Pete'
        )
        self.obj_2 = TestObject(
            first_name='Pete',
            last_name='Philly'
        )
        self.obj_3 = TestObject(
            first_name='Pete',
            last_name='Philly',
            tags='foo'
        )

    def test_obj_1(self):
        self.assertEqual(self.obj_1.networth(), 1)

    def test_obj_2(self):
        self.assertEqual(self.obj_2.networth(), 6)

    def test_obj_3(self):
        self.assertEqual(self.obj_3.networth(), 7)

        self.obj_3.add_tag('bar')

        self.assertEqual(self.obj_3.networth(), 8)