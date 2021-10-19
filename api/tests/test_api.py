from django.db.models import query
from django.urls import  reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Receipe, ReceipeImage, WhySlowcooker


class MethodsAPITests(APITestCase):
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
        WhySlowcooker.objects.create(
            heading = 'Delicate',
            paragraph = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            icon = 'delicate-icon'
        )


    """
    Ensure we can 
        list/GET (receipes, no_idea_receipes, why_slowcooker, gallery), 
        retrieve/GET (single receipe) data only,
        change likes/POST (single receipe) only
    """    
    def test_list_receipes_only(self):            
        url = reverse('api:receipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'receipe_id': '10'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_receipe_only(self):
        url = reverse('api:receipe', kwargs={'receipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'name': 'Chicken with salad'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response_put = self.client.put(url, data, format='json')
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response_patch = self.client.patch(url, data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_no_idea_receipes_only(self):     
        url = reverse('api:no_idea_receipes')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        data = {'receipe_id': '10'}
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

    def test_post_likes_receipe_method(self):
        url = reverse('api:receipe_likes', kwargs={'receipe_id':1, 'up_down': 'up'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_200_OK)

        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 


class ReceipeAPITests(APITestCase):
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

    def test_retrieving_receipes_list(self):
        url = reverse('api:receipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['count'], 2)

    """
    Receipes list - query params - {search}, {page_size}, {page}
    """
    def test_receipes_search_filter(self):
        url = reverse('api:receipes_list') + "?search=Lamb"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['count'], 1)
        self.assertEqual(response_get.data['results'][0]['name'], "Lamb salad")

    def test_receipes_list_page_size_change(self):
        url = reverse('api:receipes_list')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['next'], None)

        url = reverse('api:receipes_list') + "?page_size=1"
        response_get = self.client.get(url, format='json')
        self.assertNotEqual(response_get.data['next'], None)

    def test_receipes_list_page_number_change(self):
        url = reverse('api:receipes_list') + "?page_size=1"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['results'][0]['name'], "Chicken salad")

        url = reverse('api:receipes_list') + "?page_size=1&page=2"
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['results'][0]['name'], "Lamb salad")

    """
    Single receipe tests
    """
    def test_retrieving_single_receipe(self):
        url = reverse('api:receipe', kwargs={'receipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['name'], "Chicken salad")

    """
    Single receipe tests - POST likes / GET views
    """
    def test_post_likes_up_receipe(self):
        url = reverse('api:receipe_likes', kwargs={'receipe_id':1, 'up_down': 'up'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], 1)
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], 2)

    def test_post_likes_down_receipe(self):
        url = reverse('api:receipe_likes', kwargs={'receipe_id':1, 'up_down': 'down'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], -1)
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.data['likes'], -2)

    def test_post_likes_error_receipe(self):
        url = reverse('api:receipe_likes', kwargs={'receipe_id':1, 'up_down': 'two_down'})
        response_post = self.client.post(url, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieving_single_receipe_adds_views(self):
        url = reverse('api:receipe', kwargs={'receipe_id':1})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['views'], 2)
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data['views'], 3)


class NoIdeaReceipesAPITests(APITestCase):
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

    def test_retrieving_no_idea_receipes_list(self):
        url = reverse('api:no_idea_receipes')
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 1)

    def test_changing_no_idea_receipes_num(self):
        url = reverse('api:no_idea_receipes') + "?num=2"
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


class ReceipeImageAPITests(APITestCase):
    def setUp(self):
        saved_receipe = Receipe.objects.create(
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
        ReceipeImage.objects.create(
            receipe=saved_receipe,
            image='lorem.jpg'
        )

    def test_retrieving_gallery_list(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')
        self.assertEqual(len(response_get.data), 1)

    def test_gallery_related_to_receipe(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.data[0]['name'], "Chicken salad") 

    def test_gallery_images_count(self):
        url = reverse('api:gallery')
        response_get = self.client.get(url, format='json')        
        self.assertEqual(len(response_get.data[0]['images']), 1) 

        saved_receipe = Receipe.objects.get(receipe_id=1)
        ReceipeImage.objects.create(
            receipe=saved_receipe,
            image='lorem_ipsum.jpg'
        )
        response_get = self.client.get(url, format='json')        
        self.assertEqual(len(response_get.data[0]['images']), 2)

