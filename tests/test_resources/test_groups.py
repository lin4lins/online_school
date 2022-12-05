import json

import pytest


@pytest.mark.parametrize("student_count, group_count",
                         [[1, 1], [5, 3], [4, 2], [10, 3]])
def test_groups_search_get(api, client, student_count, group_count):
    response = client.get(f"/groups/search?student_count={student_count}")
    assert response.status_code == 200
    groups = json.loads(response.data).get("groups")
    assert len(groups) == group_count
