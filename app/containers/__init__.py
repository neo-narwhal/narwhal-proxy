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
    @jwt_required
    def get(self, project_name, username):
        claims = get_jwt_claims()
        user_id = claims['user_id']

        user = User.query.filter(User.id == user_id).first()
        if user.username == username:
            project = Project.query.filter(and_(Project.user_id == user_id,
                                                Project.name == project_name)).first()
            if project:
                return Response(requests.get('http://localhost:{}'.format(project.port)).content, status=200)
            else:
                return Response('', status=404)
        else:
            return Response('', status=403)
