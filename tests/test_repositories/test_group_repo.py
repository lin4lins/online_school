import pytest

from src.repositories import GroupRepository
from tests.test_data import GROUP_NAMES


@pytest.fixture
def group_repo(_db):
    return GroupRepository(_db)


@pytest.mark.parametrize("id, test_group_name", enumerate(GROUP_NAMES, start=1))
def test_get_by_name(app, group_repo, id, test_group_name):
    with app.app_context():
        assert group_repo.get_by_name(test_group_name).id == id


@pytest.mark.parametrize("student_count, group_count",
                         [[1, 1], [5, 3], [4, 2], [10, 3]])
def test_get_by_student_count(app, group_repo, student_count, group_count):
    with app.app_context():
        assert len(group_repo.get_by_student_count(student_count)) == group_count
