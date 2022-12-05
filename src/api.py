from flask_restful import Api

from src import app

from src.resourses import (CourseResource, GroupsSearch, StudentResource,
                           StudentsResource, StudentsSearch)

api = Api(app)
api.add_resource(StudentsResource, '/students')
api.add_resource(StudentResource, '/students/<int:id>')
api.add_resource(StudentsSearch, '/students/search')
api.add_resource(CourseResource, '/courses/<int:course_id>/students/<int:student_id>')
api.add_resource(GroupsSearch, '/groups/search')

if __name__ == '__main__':
    app.run(port=5003)
