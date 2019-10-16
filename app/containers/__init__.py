from flask import Blueprint, Response, request
from flask_restplus import Api, Resource

from app.model.user import User
from ..model.project import Project
from sqlalchemy import and_
import requests
import re

blueprint = Blueprint('containers', __name__)
api = Api(blueprint)


@api.route('/<project_name>', subdomain='<username>')
class Containers(Resource):
    def get(self, project_name, username):
        print('Containers GET')
        user = User.query.filter(User.username == username).first()
        if user:
            project = Project.query.filter(and_(Project.user_id == user.id,
                                                Project.name == project_name)).first()
            if project:
                data = requests.get('http://localhost:{}'.format(project.port))
                return Response(data, status=200)
            else:
                return Response('', status=404)
        else:
            return Response('', status=403)


@api.route('/<path:dummy>', subdomain='<username>')
class Static(Resource):
    def get(self, dummy, username):
        print('Static GET')
        referer = request.headers.get("Referer")
        if referer:
            pattern = re.compile(r'^https?://(.*)\.narwhal\.ntut\.club/(.*)$')
            m = pattern.match(referer)
            username, project_name = m.group(1), m.group(2)
            print(username, project_name)
            user = User.query.filter(User.username == username).first()
            if user:
                project = Project.query.filter(and_(Project.user_id == user.id,
                                                    Project.name == project_name)).first()
                if project:
                    data = requests.get('http://localhost:{}'.format(project.port))
                    return Response(data, status=200)
                else:
                    return Response('', status=404)
            else:
                return Response('', status=403)
        else:
            return Response('', status=403)
