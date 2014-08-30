__author__ = 'heddevanderheide'

# Django specific
from django import test

# App specific
from takeaway.models import Pizza, Topping


class TestNetworthModel(test.TestCase):
    def setUp(self):
        self.obj_1 = Pizza.objects.create(name='Margherita')
        self.obj_2 = Pizza.objects.create(name='Funghi')
        self.obj_3 = Pizza.objects.create(name='Double Dutch')

        self.topping_1 = Topping.objects.create(name='Mushrooms')
        self.topping_2 = Topping.objects.create(name='Cheese')
        self.topping_3 = Topping.objects.create(name='Onions')

        self.obj_2.toppings.add(self.topping_1)
        self.obj_3.toppings.add(self.topping_2, self.topping_3)

    def test_obj_1(self):
        # no commit
        self.assertEqual(self.obj_1.networth(), 1)
        self.assertEqual(self.obj_1._networth, 1)

        # commit
        self.assertEqual(self.obj_1.networth(commit=True), 1)
        self.assertEqual(self.obj_1._networth, 1)

        # relative
        self.assertEqual(self.obj_1.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_1._relative_networth, 100)

    def test_obj_2(self):
        self.assertEqual(self.obj_2.networth(realtime=True), 2)
        self.assertEqual(self.obj_2._networth, 1)

        # commit
        self.assertEqual(self.obj_2.networth(realtime=True, commit=True), 2)
        self.assertEqual(self.obj_2._networth, 2)

        # relative
        self.assertEqual(self.obj_2.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_2._relative_networth, 100)

    def test_obj_3(self):
        self.assertEqual(self.obj_3.networth(realtime=True), 3)
        self.assertEqual(self.obj_3._networth, 1)

        # commit
        self.assertEqual(self.obj_3.networth(realtime=True, commit=True), 3)
        self.assertEqual(self.obj_3._networth, 3)

        # relative
        self.assertEqual(self.obj_3.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_3._relative_networth, 100)

    def test_relative_networth_multiple_objects(self):
        # no commit
        self.assertEqual(self.obj_1.networth(realtime=True), 1)
        self.assertEqual(self.obj_2.networth(realtime=True), 2)
        self.assertEqual(self.obj_3.networth(realtime=True), 3)

        # OBJ 1

        # commit
        self.assertEqual(self.obj_1.networth(commit=True), 1)
        self.assertEqual(self.obj_1._networth, 1)

        # relative
        self.assertEqual(self.obj_1.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_1._relative_networth, 100)

        # OBJ 2

        # commit
        self.assertEqual(self.obj_2.networth(realtime=True, commit=True), 2)
        self.assertEqual(self.obj_2._networth, 2)

        # relative
        self.assertEqual(self.obj_2.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_2._relative_networth, 100)

        # re-test previous object(s)
        self.assertEqual(self.obj_1.relative_networth(realtime=False, commit=True), 100)
        self.assertEqual(self.obj_1._relative_networth, 50)

        # OBJ 3

        # commit
        self.assertEqual(self.obj_3.networth(realtime=True, commit=True), 3)
        self.assertEqual(self.obj_3._networth, 3)

        # relative
        self.assertEqual(self.obj_3.relative_networth(realtime=True, commit=True), 100)
        self.assertEqual(self.obj_3._relative_networth, 100)

        # re-test previous object(s)
        self.assertEqual(self.obj_1.relative_networth(realtime=False, commit=True), 50)
        self.assertEqual(self.obj_1._relative_networth, 33)

        self.assertEqual(self.obj_2.relative_networth(realtime=False, commit=True), 100)
        self.assertEqual(self.obj_2._relative_networth, 66)