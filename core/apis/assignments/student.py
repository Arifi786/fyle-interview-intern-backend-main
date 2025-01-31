from flask import Blueprint, make_response, jsonify, Response
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentSubmitSchema
from ...libs import assertions
from ...models import assignments
from ...models.teachers import Teacher

student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    assignment_data = AssignmentSchema().load(incoming_payload, partial=True)
    if not incoming_payload.get('content'):
        response = make_response(
            jsonify({'error': 'Content cannot be empty'}),
            400
        )
        return response
    print("here")
    # Check for existing assignment
    if 'id' in incoming_payload and incoming_payload['id'] is not None:
        existing_assignment = Assignment.get_by_id(incoming_payload['id'])
        assertions.assert_found(existing_assignment, 'No assignment with this id was found')
        assertions.assert_true(
            existing_assignment.student_id == p.student_id,
            'This assignment belongs to another student'
        )

    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id
    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)



@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    # Validate and load payload
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Validate teacher exists
    teacher = Teacher.query.get(submit_assignment_payload.teacher_id)
    print(teacher)
    assertions.assert_found(teacher, "No such teacher exists")


    # Proceed with submission
    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    if isinstance(submitted_assignment, Response):
        return submitted_assignment
    db.session.commit()

    # Return response
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)