from flask import Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import Api, Resource

from app.model.user import User
from ..model.project import Project
from sqlalchemy import and_

import requests

blueprint = Blueprint('containers', __name__)
api = Api(blueprint)


@api.route('/<project_name>', subdomain='<username>')
class Containers(Resource):
    def get(self, project_name, username):
        user = User.query.filter(User.username == username).first()
        if user:
            project = Project.query.filter(and_(Project.user_id == user.id,
                                                Project.name == project_name)).first()
            if project:
                return Response(requests.get('http://localhost:{}'.format(project.port)).content, status=200)
            else:
                return Response('', status=404)
        else:
            return Response('', status=403)
