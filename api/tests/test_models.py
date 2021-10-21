from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from ..models import Recipe, RecipeImage, WhySlowcooker


class recipeTestCase(TestCase):
    def setUp(self):
        Recipe.objects.create(
            recipe_id = '1',
            url = 'https://www.crockpot.pl/przepis?p=1',
            name = 'Chicken salad',
            slug = 'chicken-salad',
            serving_size = '10+',
            preparing_time = '30 mins',
            time_on_high = '6h',
            time_on_low = '',
            recipe_ingredients = 'Chicken, salad, peper, salt',
            recipe_how_to = 'Place chicken in slow cooker, serve with salad'
        )

        Recipe.objects.create(
            recipe_id = '2',
            url = 'https://www.crockpot.pl/przepis?p=2',
            name = 'Lamb salad',
            slug = 'lamb-salad',
            serving_size = '6+',
            preparing_time = '40 mins',
            time_on_high = '1h',
            time_on_low = '6h',
            recipe_ingredients = 'Lamb, salad, peper, salt',
            recipe_how_to = 'Place lamb in slow cooker, serve with salad'
        )

    def test_saving_and_retrieving_part(self):
        saved_recipes = Recipe.objects.all()
        self.assertEqual(saved_recipes.count(), 2)

        first_saved_recipe = saved_recipes[0]
        second_saved_recipe = saved_recipes[1]
        self.assertEqual(first_saved_recipe.name, 'Chicken salad')
        self.assertEqual(second_saved_recipe.name, 'Lamb salad')

    def test_string_representation(self):
        saved_recipe = Recipe.objects.all()[0]
        self.assertEqual(str(saved_recipe), '1 Chicken salad')

    def test_slug_generating(self):
        recipe = Recipe.objects.create(
            recipe_id = '3',
            url = 'https://www.crockpot.pl/przepis?p=3',
            name = 'Pork with 2 kg carrots',
            serving_size = '2+',
            preparing_time = '30 mins',
            time_on_high = '3h',
            time_on_low = '',
            recipe_ingredients = 'Pork, 2kg carrots, peper, salt',
            recipe_how_to = 'Place pork and carrots in slow cooker, wait and eat'
        )
        self.assertEqual(recipe.slug, 'pork-with-2-kg-carrots')    

    def test_cannot_save_empty_recipe(self):        
        with self.assertRaises(IntegrityError):
            recipe = Recipe.objects.create()
            recipe.full_clean()

    def test_default_values(self):
        saved_recipe = Recipe.objects.all()[0]
        self.assertEqual(saved_recipe.views, 1)
        self.assertEqual(saved_recipe.likes, 0)

    def test_unique_together(self):
        new_recipe = {
            'recipe_id': '5',
            'url': 'https://www.crockpot.pl/przepis?p=5',
            'name': 'Chicken salad',
            'slug': 'chicken-salad',
            'serving_size': '10+',
            'preparing_time': '30 mins',
            'time_on_high': '6h',
            'time_on_low': '',
            'recipe_ingredients': 'Chicken, salad, peper, salt',
            'recipe_how_to': 'Place chicken in slow cooker, serve with salad'
        }
        Recipe.objects.create(**new_recipe)
        with self.assertRaises(IntegrityError):
            another_recipe = Recipe.objects.create(**new_recipe)
            another_recipe.full_clean()


class recipeImageTestCase(TestCase):
    def setUp(self):
        Recipe.objects.create(
            recipe_id = '1',
            url = 'https://www.crockpot.pl/przepis?p=1',
            name = 'Chicken salad',
            slug = 'chicken-salad',
            serving_size = '10+',
            preparing_time = '30 mins',
            time_on_high = '6h',
            time_on_low = '',
            recipe_ingredients = 'Chicken, salad, peper, salt',
            recipe_how_to = 'Place chicken in slow cooker, serve with salad'
        )

    def test_gallery_is_related_to_recipe(self):
        saved_recipe = Recipe.objects.all()[0]
        gallery = RecipeImage.objects.create(recipe=saved_recipe, image='lorem.jpg')
        self.assertIn(gallery, saved_recipe.images.all())


class WhySlowcookerTestCase(TestCase):
    def setUp(self):
        WhySlowcooker.objects.create(
            heading = 'Delicate',
            paragraph = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            icon = 'delicate-icon'
        )

        WhySlowcooker.objects.create(
            heading = 'Full of Vitamins',
            paragraph = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            icon = 'vitamins-icon'
        )

    def test_saving_and_retrieving_part(self):
        saved_data = WhySlowcooker.objects.all()
        self.assertEqual(saved_data.count(), 2)

        first_saved_data = saved_data[0]
        second_saved_data = saved_data[1]
        self.assertEqual(first_saved_data.heading, 'Delicate')
        self.assertEqual(second_saved_data.heading, 'Full of Vitamins')

    def test_string_representation(self):
        saved_data = WhySlowcooker.objects.all()[0]
        self.assertEqual(str(saved_data), 'Delicate')  

    def test_cannot_save_empty_recipe(self):        
        with self.assertRaises(ValidationError):
            saved_data = WhySlowcooker.objects.create()
            saved_data.full_clean()
