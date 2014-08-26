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
        self.assertEqual(self.obj_1.networth(), 1)

    def test_obj_2(self):
        self.assertEqual(self.obj_2.networth(), 6)