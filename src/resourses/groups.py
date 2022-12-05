from flask_restful import Resource, reqparse, fields, marshal_with

from src import db
from src.repositories import GroupRepository


group_fields = {"id": fields.Integer, "name": fields.String}


class GroupsSearch(Resource):
    def __init__(self):
        super().__init__()
        self.group_repo = GroupRepository(db)

    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('student_count', type=int, required=True, location="args")
        return parser.parse_args()

    @marshal_with(group_fields, envelope="groups")
    def get(self):
        """Returns all groups with less or equals student count.
           ---
           parameters:
           - name: student_count
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
        return self.group_repo.get_by_student_count(arguments['student_count'])
