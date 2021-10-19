from django.test import TestCase
from ..utils import CrockPotRecipe, get_last_crockpot_receipe_id

'''
class CrockpotUtilsTestCase(TestCase):
    def test_last_crockpot_receipe_id_is_number(self):
        last_id = get_last_crockpot_receipe_id()
        self.assertTrue(int(last_id))

    def test_crockpot_class_retreive_data(self):
        last_id = get_last_crockpot_receipe_id()
        crockpot_receipe = CrockPotRecipe(last_id)
        crockpot_receipe_data = crockpot_receipe.get_receipe_data()
        self.assertEqual(crockpot_receipe_data['url'], f'https://www.crockpot.pl/przepis?p={last_id}')
        self.assertEqual(crockpot_receipe_data['receipe_id'], last_id)
'''