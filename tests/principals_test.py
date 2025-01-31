import pytest

from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals import Principal
from core.models.teachers import TeacherSchema



def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_principal_repr(client):
    # Assuming a principal object exists with an id
    principal = Principal(id=1)
    repr_str = repr(principal)
    assert repr_str == '<Principal 1>'

# def test_teacher_list(client,h_principal):
#     response = client.get(
#         '/principal/assignments',
#         headers=h_principal
#     )
#     assert response.status_code == 200
#     assert response.json['data']['teacher_id'] == 1

def test_list_teachers(client, h_principal):
    # Send a GET request to the /teachers endpoint
    response = client.get('/principal/teachers', headers=h_principal)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON contains the 'data' key and it is a list
    data = response.json
    assert 'data' in data, "'data' key is missing from the response"
    assert isinstance(data['data'], list), "'data' should be a list"

    # You can add more assertions depending on the expected contents of the list
    # For example, checking that the list is not empty (if you have teachers in the DB)
    assert len(data['data']) > 0, "'data' should not be empty"