from django.test import TestCase
from ..utils import CrockPotRecipe, get_last_crockpot_recipe_id


class CrockpotUtilsTestCase(TestCase):
    def test_last_crockpot_recipe_id_is_number(self):
        last_id = get_last_crockpot_recipe_id()
        self.assertTrue(int(last_id))

    def test_crockpot_class_retreive_data(self):
        last_id = get_last_crockpot_recipe_id()
        crockpot_recipe = CrockPotRecipe(last_id)
        crockpot_recipe_data = crockpot_recipe.get_recipe_data()
        self.assertEqual(crockpot_recipe_data['url'], f'https://www.crockpot.pl/przepis?p={last_id}')
        self.assertEqual(crockpot_recipe_data['recipe_id'], last_id)
