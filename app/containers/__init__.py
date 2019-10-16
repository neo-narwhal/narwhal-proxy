from flask import Blueprint, Response, request, make_response
from flask_restplus import Api, Resource

from app.model.user import User
from ..model.project import Project
from sqlalchemy import and_
import requests
import re
import json

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
                reponse = Response(data, status=200)
                reponse.set_cookie('np', json.dumps({
                    'username': username,
                    'project_name': project_name
                }))
                return reponse
            else:
                return Response('', status=404)
        else:
            return Response('', status=403)


@api.route('/<path:dummy>', subdomain='<username>')
class Static(Resource):
    def get(self, dummy, username):
        print('Static GET')
        cookie = request.cookies['np']
        if cookie:
            user_info = json.loads(cookie)
            username = user_info['username']
            project_name = user_info['project_name']
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
