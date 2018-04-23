from flask import request
from flask_restful import Resource

from ..util import authenticate, restrict_editor
from ..models import db, FitsFit, FitsCategory


class FitsResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        fit_list = [
            {
                'id': fit.id,
                'name': fit.name,
                'category': fit.category.name,
                'category_id': fit.category.id,
                'content': fit.content,
                'order': fit.order
            } for fit in FitsFit.query.all()
        ]
        category_list = [
            {
                'id': category.id,
                'name': category.name,
                'order': category.order
            } for category in FitsCategory.query.all()
        ]
        return {
            'fits': sorted(fit_list, key=lambda e: e['order']),
            'categories': sorted(category_list, key=lambda e: e['order'])
        }

    def post(self):
        db.session.add(FitsFit(request.json['name']))
        db.session.commit()
        return {}, 204


class FitResource(Resource):

    method_decorators = [restrict_editor]

    def put(self, id):
        fit = FitsFit.query.get(id)
        fit.content = request.json['content']
        fit.category_id = request.json['category_id']
        fit.order = int(request.json['order'])
        db.session.commit()
        return {}, 204

    def delete(self, id):
        db.session.delete(FitsFit.query.get(id))
        db.session.commit()
        return {}, 204
