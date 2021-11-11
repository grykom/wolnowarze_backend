from django.urls import  reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Recipe, RecipeImage, WhySlowcooker


class MethodsAPITests(APITestCase):
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
        WhySlowcooker.objects.create(
            heading = 'Delicate',
            paragraph = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            icon = 'delicate-icon'
        )


    """
    Ensure we can 
        list/GET (recipes, no_idea_recipes, why_slowcooker, gallery), 
        retrieve/GET (single recipe) data only,
        change likes/POST (single recipe) only
    """    
    def test_list_recipes_only(self):            
        url = reverse('api:recipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'recipe_id': '10'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_recipe_only(self):
        url = reverse('api:recipe', kwargs={'recipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'name': 'Chicken with salad'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response_put = self.client.put(url, data, format='json')
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response_patch = self.client.patch(url, data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_no_idea_recipes_only(self):     
        url = reverse('api:no_idea_recipes')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'recipe_id': '10'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_why_slowcooker_only(self):
        url = reverse('api:why_slowcooker')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'heading': 'Health'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)   

    def test_list_gallery_only(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'name': 'Pork with salad'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 

    def test_post_likes_recipe_method(self):
        url = reverse('api:recipe_likes', kwargs={'recipe_id':1, 'up_down': 'up'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_200_OK)

        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 


class recipeAPITests(APITestCase):
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

    def test_retrieving_recipes_list(self):
        url = reverse('api:recipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['count'], 2)

    """
    recipes list - query params - {search}, {page_size}, {page}
    """
    def test_recipes_search_filter(self):
        url = reverse('api:recipes_list') + "?search=Lamb"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['count'], 1)
        self.assertEqual(response_get.data['results'][0]['name'], "Lamb salad")

    def test_recipes_list_page_size_change(self):
        url = reverse('api:recipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['next'], None)

        url = reverse('api:recipes_list') + "?page_size=1"
        response_get = self.client.get(url, format='json')
        self.assertNotEqual(response_get.data['next'], None)

    def test_recipes_list_page_number_change(self):
        url = reverse('api:recipes_list') + "?page_size=1"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['results'][0]['name'], "Chicken salad")

        url = reverse('api:recipes_list') + "?page_size=1&page=2"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['results'][0]['name'], "Lamb salad")

    """
    Single recipe tests
    """
    def test_retrieving_single_recipe(self):
        url = reverse('api:recipe', kwargs={'recipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['name'], "Chicken salad")

    """
    Single recipe tests - POST likes / GET views
    """
    def test_post_likes_up_recipe(self):
        url = reverse('api:recipe_likes', kwargs={'recipe_id':1, 'up_down': 'up'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], 1)
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], 2)

    def test_post_likes_down_recipe(self):
        url = reverse('api:recipe_likes', kwargs={'recipe_id':1, 'up_down': 'down'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], -1)
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], -2)

    def test_post_likes_error_recipe(self):
        url = reverse('api:recipe_likes', kwargs={'recipe_id':1, 'up_down': 'two_down'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieving_single_recipe_adds_views(self):
        url = reverse('api:recipe', kwargs={'recipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['views'], 2)
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['views'], 3)


class NoIdearecipesAPITests(APITestCase):
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

    def test_retrieving_no_idea_recipes_list(self):
        url = reverse('api:no_idea_recipes')
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 1)

    def test_changing_no_idea_recipes_num(self):
        url = reverse('api:no_idea_recipes') + "?num=2"
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 2)


class WhySlowcookerAPITests(APITestCase):
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

    def test_retrieving_why_slowcooker_list(self):
        url = reverse('api:why_slowcooker')
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 2)


class recipeImageAPITests(APITestCase):
    def setUp(self):
        saved_recipe = Recipe.objects.create(
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
        RecipeImage.objects.create(
            recipe=saved_recipe,
            image='lorem.jpg'
        )

    def test_retrieving_gallery_list(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 1)

    def test_gallery_related_to_recipe(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data[0]['name'], "Chicken salad") 

    def test_gallery_images_count(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')        
        self.assertEqual(len(response_get.data[0]['images']), 1) 

        saved_recipe = Recipe.objects.get(recipe_id=1)
        RecipeImage.objects.create(
            recipe=saved_recipe,
            image='lorem_ipsum.jpg'
        )
        response_get = self.client.get(url, format='json')        
        self.assertEqual(len(response_get.data[0]['images']), 2)

