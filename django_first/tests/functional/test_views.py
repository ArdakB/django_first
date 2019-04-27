from lxml import html
from django_first.models import Order


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
    assert len(response.cssselect('li')) == orders.count()


def test_order_view(db, client, data):
    response = client.get('/orders/1/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'


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
