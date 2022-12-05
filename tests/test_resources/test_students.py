import json

import dicttoxml2
import pytest

from tests.test_data import NUMBER_OF_STUDENTS_ON_COURSE


@pytest.mark.parametrize("course_name, students_in_course_count",
                         NUMBER_OF_STUDENTS_ON_COURSE.items())
def test_students_search_get(api, client, course_name, students_in_course_count):
    response = client.get(f"/students/search?course={course_name}")
    assert response.status_code == 200
    students = json.loads(response.data).get("students")
    assert len(students) == students_in_course_count


def test_students_post(api, client):
    request_body = {"group_name": "CD-34", "first_name": "Jeffree", "last_name": "Star"}
    response = client.post("/students", json=request_body)
    assert response.status_code == 201


def test_students_invalid_content_type(api, client):
    request_body = {"group_name": "CD-34", "first_name": "Jeffree", "last_name": "Star"}
    response = client.post("/students", data=request_body,
                           headers={"Content-Type": "application/xml"})
    assert response.status_code == 404


def test_student_delete(api, client):
    response = client.delete("/students/1")
    assert response.status_code == 204
