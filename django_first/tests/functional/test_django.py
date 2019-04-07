def test_hello_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.content == b'Hello, world!'

#def test_django(client):
#    response = client.get("/")
#    assert response.status_code == 404