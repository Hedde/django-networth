__author__ = 'heddevanderheide'

# Django specific
from django import test

# App specific
from app.models import TestModel


class TestNetworthModel(test.TestCase):
    def setUp(self):
        self.obj_1 = TestModel.objects.create(
            first_name='Pete',
        )
        self.obj_2 = TestModel.objects.create(
            first_name='Pete',
            last_name='Philly'
        )

    def test_obj_1(self):
        # no commit
        self.assertEqual(self.obj_1.networth(commit=False), 1)
        self.assertEqual(self.obj_1._networth, 0)

        # commit
        self.assertEqual(self.obj_1.networth(commit=True), 1)
        self.assertEqual(self.obj_1._networth, 1)

        # relative
        self.assertEqual(self.obj_1.relative_networth(), 100)

    def test_obj_2(self):
        self.assertEqual(self.obj_2.networth(commit=False), 6)
        self.assertEqual(self.obj_2._networth, 0)

        # commit
        self.assertEqual(self.obj_2.networth(commit=True), 6)
        self.assertEqual(self.obj_2._networth, 6)

        # relative
        self.assertEqual(self.obj_2.relative_networth(), 100)

    def test_relative_networth_multiple_objects(self):
        # no commit
        self.assertEqual(self.obj_1.networth(commit=False), 1)
        self.assertEqual(self.obj_2.networth(commit=False), 6)

        # commit
        self.assertEqual(self.obj_1.networth(commit=True), 1)
        self.assertEqual(self.obj_2.networth(commit=True), 6)

        # relative
        self.assertEqual(self.obj_1.relative_networth(), 16)
        self.assertEqual(self.obj_2.relative_networth(), 100)