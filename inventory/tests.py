import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item
from django.contrib.auth import get_user_model


# Get the test logger
test_logger = logging.getLogger('inventory.tests')


class ItemTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Creating a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
    
    def setUp(self):
        # Logging the user and retrieving the token
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    # testcases for creating items 
    def test_create_item_success(self):
        url = reverse('create_item')
        data = {'name': 'Item1', 'description': 'A test item'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Item1')
        test_logger.info(f'Successfully created item: {data["name"]}')  

    def test_create_item_failure(self):
        # Create first item details
        Item.objects.create(name='Item1', description='A test item')
        url = reverse('create_item')
        data = {'name': 'Item1', 'description': 'Duplicate test item'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_logger.error(f'Failed to create duplicate item: {data["name"]}')  

    # testcases for fetching item details
    def test_get_item_success(self):
        item = Item.objects.create(name='Item1', description='A test item')
        url = reverse('item_detail', kwargs={'item_id': item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)
        test_logger.info(f'Successfully fetched item with id: {item.id}') 

    def test_get_item_failure(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_logger.error(f'Failed to fetch item with non-existent id: 999')  

    # testcases for updating item details
    def test_update_item_success(self):
        item = Item.objects.create(name='Item1', description='A test item')
        url = reverse('item_detail', kwargs={'item_id': item.id})
        data = {'name': 'Updated Item', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Item')
        test_logger.info(f'Successfully updated item with id: {item.id}')

    def test_update_item_failure(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        data = {'name': 'Non-existent Item', 'description': 'Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_logger.error(f'Failed to update non-existent item with id: 999')  

    # testcases for deleting item details
    def test_delete_item_success(self):
        item = Item.objects.create(name='Item1', description='A test item')
        url = reverse('item_detail', kwargs={'item_id': item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
        test_logger.info(f'Successfully deleted item with id: {item.id}')  

    def test_delete_item_failure(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_logger.error(f'Failed to delete non-existent item with id: 999')  

    # testcases for fetching all item details
    def test_get_all_items_success(self):
        Item.objects.create(name='Item1', description='A test item')
        Item.objects.create(name='Item2', description='Another test item')
        url = reverse('get_item_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        test_logger.info('Successfully fetched all items.')  

    def test_get_all_items_empty(self):
        url = reverse('get_item_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_logger.warning('No items found when fetching the item list.')  
