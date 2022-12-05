from flask import request, Response
from flask_restful import Resource, abort, reqparse, fields, marshal_with

from src import db
from src.models import Student
from src.repositories import GroupRepository, StudentRepository

course_fields = {"id": fields.Integer, "name": fields.String, "description": fields.String}
student_fields = {"id": fields.Integer, "first_name": fields.String, "last_name": fields.String,
                  "courses": fields.Nested(course_fields)}


class StudentsResource(Resource):
    def __init__(self):
        super().__init__()
        self.group_repo = GroupRepository(db)
        self.student_repo = StudentRepository(db)

    def post(self):
        """Creates student
           ---
           parameters:
           - name: Student
             in: body
             required: true
             schema:
              id: Student
              required:
                - group_name
                - first_name
                - last_name
              properties:
                group_name:
                  type: string
                first_name:
                  type: string
                last_name:
                  type: string
           responses:
             201:
               description: Created
             404:
               description: Not found
             500:
               description: Internal server error
                   """
        request_type = request.headers.get("Content-Type")
        if request_type != "application/json":
            abort(404)

        student_to_create = Student(group_id=self.group_repo.
                                    get_by_name(request.json['group_name']).id,
                                    first_name=request.json['first_name'],
                                    last_name=request.json['last_name'])
        self.student_repo.create(student_to_create)
        return Response(status=201)


class StudentResource(Resource):
    def __init__(self):
        super().__init__()
        self.student_repo = StudentRepository(db)

    def delete(self, id: int):
        """Deletes student
           ---
           parameters:
           - name: id
             in: path
             required: true
           responses:
             204:
               description: No data
             404:
               description: Not found
             500:
               description: Internal server error
        """
        self.student_repo.delete(student_id=id)
        return Response(status=204)


class StudentsSearch(Resource):
    def __init__(self):
        super().__init__()
        self.student_repo = StudentRepository(db)

    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('course', type=str, required=True, location="args")
        return parser.parse_args()

    @marshal_with(student_fields, envelope="students")
    def get(self):
        """Returns all students related to the course with a given name
           ---
           parameters:
           - name: course
             in: query
             required: true
           responses:
             200:
               description: OK
             404:
               description: Not found
             500:
               description: Internal server error
           produces:
             - application/json
        """
        arguments = self.__get_arguments()
        return self.student_repo.get_all_by_course_name(arguments['course'])
