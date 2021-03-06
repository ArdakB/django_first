from lxml import html
from django.urls import reverse
from django_first.models import Order, Product


def test_hello_200(db, client, data):
    client.login(username='alice', password='alice')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, world!' in response
    assert 'alice' in response
    response = html.fromstring(response)
    orders = Order.objects.filter(
        customer__user__username='alice'
    )
    items = response.cssselect('.list-group-item > a')
    assert len(items) == orders.count()
    assert items[0].text == '1'


def test_order_view(db, client, data):
    url = reverse('orders', args=[1])
    response = client.get(url)
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'
    assert response.cssselect('#product') != []
    assert response.cssselect('#quantity') != []


def test_order_add(db, client, data):
    client.login(username='alice', password='alice')
    response = client.post('/', {'city': 1})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    orders = response.cssselect('.list-group-item > a')
    assert len(orders) == 2
    assert orders[0].text == '1'
    assert orders[1].text == '2'


def test_order_add_item_same(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 10})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 20'


def test_order_add_item_new(db, client, data):
    banana = Product.objects.create(name='banana', price=20)
    response = client.post(
        '/orders/1/',
        {'product': banana.id, 'quantity': 30}
    )
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'
    assert items[1].text == 'banana 30'


def test_order_add_item_product_doesnt_exist(db, client, data):
    response = client.post('/orders/1/', {'product': 100, 'quantity': ''})
    assert response.status_code == 404
    response = response.content.decode('utf-8')
    assert response == 'Product not found'


def test_order_add_item_invalid_product_id(db, client, data):
    response = client.post('/orders/1/', {'product': 'asd', 'quantity': ''})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Invalid product id'


def test_order_add_item_empty_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': ''})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_item_zero_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 0})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_item_negative_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': -10})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_item_nonint_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 'asd'})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_django_404(client):
    response = client.get('/test/')
    assert response.status_code == 404


def test_bye_200(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'


def test_third_200(client):
    response = client.get('/third/')
    assert response.status_code == 200
    assert response.content == b'Third'
