from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model

from apps.pizzas.models import Pizza

User = get_user_model()


class TestOrderAPI(APITestCase):
    def setUp(self):
        self.pizza = Pizza.objects.create(name='test pizza', price=100, price_discount=20)
        self.user = User.objects.create_user(username='test', password='test')
        self.test_client = APIClient()

    def test_api_orders(self):
        token_url = api_reverse('token-obtain')
        obtain_r = self.test_client.post(
            path=token_url,
            data={'username': 'test', 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        order_url = api_reverse('pizzas-order', kwargs={'pk': self.pizza.id})
        self.test_client.post(path=order_url)

        orders_url = api_reverse('orders-list')
        orders_r = self.test_client.get(path=orders_url)

        self.assertEqual(orders_r.status_code, status.HTTP_200_OK)
        self.assertEqual(orders_r.json()['results'][0].get('price'), 80)
        self.assertEqual(orders_r.json()['count'], 1)

    def test_api_order_detail(self):
        token_url = api_reverse('token-obtain')
        obtain_r = self.test_client.post(
            path=token_url,
            data={'username': 'test', 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        order_url = api_reverse('pizzas-order', kwargs={'pk': self.pizza.id})
        order_r = self.test_client.post(path=order_url)
        detail_url = api_reverse('orders-detail', kwargs={'pk': order_r.json()['id']})
        detail_r = self.test_client.get(path=detail_url)

        self.assertContains(detail_r, 'id', status_code=status.HTTP_200_OK)

        delete_r = self.test_client.delete(path=detail_url)

        self.assertEqual(delete_r.status_code, status.HTTP_204_NO_CONTENT)
