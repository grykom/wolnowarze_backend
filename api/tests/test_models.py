from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from ..models import Receipe, ReceipeImage, WhySlowcooker


class ReceipeTestCase(TestCase):
    def setUp(self):
        Receipe.objects.create(
            receipe_id = '1',
            url = 'https://www.crockpot.pl/przepis?p=1',
            name = 'Chicken salad',
            slug = 'chicken-salad',
            serving_size = '10+',
            preparing_time = '30 mins',
            time_on_high = '6h',
            time_on_low = '',
            receipe_ingredients = 'Chicken, salad, peper, salt',
            receipe_how_to = 'Place chicken in slow cooker, serve with salad'
        )

        Receipe.objects.create(
            receipe_id = '2',
            url = 'https://www.crockpot.pl/przepis?p=2',
            name = 'Lamb salad',
            slug = 'lamb-salad',
            serving_size = '6+',
            preparing_time = '40 mins',
            time_on_high = '1h',
            time_on_low = '6h',
            receipe_ingredients = 'Lamb, salad, peper, salt',
            receipe_how_to = 'Place lamb in slow cooker, serve with salad'
        )

    def test_saving_and_retrieving_part(self):
        saved_receipes = Receipe.objects.all()
        self.assertEqual(saved_receipes.count(), 2)

        first_saved_receipe = saved_receipes[0]
        second_saved_receipe = saved_receipes[1]
        self.assertEqual(first_saved_receipe.name, 'Chicken salad')
        self.assertEqual(second_saved_receipe.name, 'Lamb salad')

    def test_string_representation(self):
        saved_receipe = Receipe.objects.all()[0]
        self.assertEqual(str(saved_receipe), '1 Chicken salad')

    def test_slug_generating(self):
        receipe = Receipe.objects.create(
            receipe_id = '3',
            url = 'https://www.crockpot.pl/przepis?p=3',
            name = 'Pork with 2 kg carrots',
            serving_size = '2+',
            preparing_time = '30 mins',
            time_on_high = '3h',
            time_on_low = '',
            receipe_ingredients = 'Pork, 2kg carrots, peper, salt',
            receipe_how_to = 'Place pork and carrots in slow cooker, wait and eat'
        )
        self.assertEqual(receipe.slug, 'pork-with-2-kg-carrots')    

    def test_cannot_save_empty_receipe(self):        
        with self.assertRaises(IntegrityError):
            receipe = Receipe.objects.create()
            receipe.full_clean()

    def test_default_values(self):
        saved_receipe = Receipe.objects.all()[0]
        self.assertEqual(saved_receipe.views, 1)
        self.assertEqual(saved_receipe.likes, 0)

    def test_unique_together(self):
        new_receipe = {
            'receipe_id': '5',
            'url': 'https://www.crockpot.pl/przepis?p=5',
            'name': 'Chicken salad',
            'slug': 'chicken-salad',
            'serving_size': '10+',
            'preparing_time': '30 mins',
            'time_on_high': '6h',
            'time_on_low': '',
            'receipe_ingredients': 'Chicken, salad, peper, salt',
            'receipe_how_to': 'Place chicken in slow cooker, serve with salad'
        }
        Receipe.objects.create(**new_receipe)
        with self.assertRaises(IntegrityError):
            another_receipe = Receipe.objects.create(**new_receipe)
            another_receipe.full_clean()


class ReceipeImageTestCase(TestCase):
    def setUp(self):
        Receipe.objects.create(
            receipe_id = '1',
            url = 'https://www.crockpot.pl/przepis?p=1',
            name = 'Chicken salad',
            slug = 'chicken-salad',
            serving_size = '10+',
            preparing_time = '30 mins',
            time_on_high = '6h',
            time_on_low = '',
            receipe_ingredients = 'Chicken, salad, peper, salt',
            receipe_how_to = 'Place chicken in slow cooker, serve with salad'
        )

    def test_gallery_is_related_to_receipe(self):
        saved_receipe = Receipe.objects.all()[0]
        gallery = ReceipeImage.objects.create(receipe=saved_receipe, image='lorem.jpg')
        self.assertIn(gallery, saved_receipe.images.all())


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

    def test_cannot_save_empty_receipe(self):        
        with self.assertRaises(ValidationError):
            saved_data = WhySlowcooker.objects.create()
            saved_data.full_clean()
