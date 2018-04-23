from flask import request
from flask_restful import Resource, marshal_with

from ..util import restrict_admin
from ..models import db, FitsCategory


class FitsCategoriesResource(Resource):

    method_decorators = [restrict_admin]

    @marshal_with(FitsCategory.resource_fields)
    def get(self):
        return FitsCategory.query.all()

    def post(self):
        db.session.add(FitsCategory(request.json['name']))
        db.session.commit()
        return {}, 204


class FitsCategoryResource(Resource):

    method_decorators = [restrict_admin]

    def put(self, id):
        FitsCategory.query.get(id).order = int(request.json['order'])
        db.session.commit()
        return {}, 204

    def delete(self, id):
        db.session.delete(FitsCategory.query.get(id))
        db.session.commit()
        return {}, 204
