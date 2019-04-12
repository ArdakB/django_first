def test_hello_200(client):
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, world!' in response


def test_django_404(client):
    response = client.get("/test/")
    assert response.status_code == 404


def test_bye_200(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'


def test_third_200(client):
    response = client.get('/third/')
    assert response.status_code == 200
    assert response.content == b'Third'
