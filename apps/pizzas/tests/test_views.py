from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model

from apps.pizzas.models import Pizza, PizzaComment

User = get_user_model()


class TestPizzaAPI(APITestCase):
    def setUp(self):
        self.pizza = Pizza.objects.create(name='test pizza', price=100, price_discount=10)
        self.user = User.objects.create_user(username='test', password='test')
        self.test_client = APIClient()

    def test_api_pizzas(self):
        pizzas_url = api_reverse('pizzas-list')
        pizzas_r = self.test_client.get(path=pizzas_url)

        self.assertEqual(pizzas_r.status_code, status.HTTP_200_OK)
        self.assertContains(pizzas_r, 'test pizza', status_code=status.HTTP_200_OK)
        self.assertEqual(pizzas_r.json().get('count'), 1)

    def test_api_order_pizza(self):
        token_url = api_reverse('token-obtain')
        obtain_r = self.test_client.post(
            path=token_url,
            data={'username': 'test', 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        order_url = api_reverse('pizzas-order', kwargs={'pk': self.pizza.id})
        order_r = self.test_client.post(path=order_url)

        self.assertEqual(order_r.status_code, status.HTTP_201_CREATED)

    def test_api_comment(self):
        token_url = api_reverse('token-obtain')
        obtain_r = self.test_client.post(
            path=token_url,
            data={'username': 'test', 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        add_comment_url = api_reverse('pizzas-add-comment', kwargs={'pk': self.pizza.id})
        add_comment_r = self.test_client.post(path=add_comment_url, data={'content': 'test-comment'})

        self.assertEqual(add_comment_r.status_code, status.HTTP_201_CREATED)

        comments_url = api_reverse('pizzas-comments', kwargs={'pk': self.pizza.id})
        comments_r = self.test_client.get(path=comments_url)

        self.assertNotContains(comments_r, 'test-comment', status_code=status.HTTP_200_OK)

        # Approving comments
        PizzaComment.objects.filter(
            approved_user__isnull=True
        ).update(
            approved_user=self.user,
            approved_time=timezone.now()
        )
        comments_r = self.test_client.get(path=comments_url)

        self.assertContains(comments_r, 'test-comment', status_code=status.HTTP_200_OK)
        self.assertEqual(comments_r.json().get('count'), 1)

    def test_api_rate(self):
        token_url = api_reverse('token-obtain')
        obtain_r = self.test_client.post(
            path=token_url,
            data={'username': 'test', 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        rate_url = api_reverse('pizzas-rate', kwargs={'pk': self.pizza.id})
        rate_r = self.test_client.post(path=rate_url, data={'rate': 3})

        self.assertEqual(rate_r.status_code, status.HTTP_201_CREATED)
