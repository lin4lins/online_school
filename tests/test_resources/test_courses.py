def test_courses_post(api, client):
    response = client.post("/courses/1/students/1")
    assert response.status_code == 201


def test_courses_delete(api, client):
    response = client.delete("/courses/1/students/1")
    assert response.status_code == 204