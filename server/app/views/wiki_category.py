from flask import request
from flask_restful import Resource, marshal, marshal_with

from ..util import authenticate, restrict_admin
from ..models import db, WikiCategory, WikiPage


class WikiCategoriesResource(Resource):

    @authenticate
    @marshal_with(WikiCategory.resource_fields)
    def get(self):
        """ Return all categories """
        return WikiCategory.query.all()

    @restrict_admin
    def post(self):
        """ Create a new category """
        db.session.add(WikiCategory(request.json['name']))
        db.session.commit()
        return {}, 204


class WikiCategoryResource(Resource):

    method_decorators = [restrict_admin]

    def put(self, id):
        """ Change the name of the category """
        WikiCategory.query.get(id).name = request.json['name']
        db.session.commit()
        return {}, 204

    def delete(self, id):
        """ Delete the category """
        db.session.delete(WikiCategory.query.get(id))
        db.session.commit()
        return 204, {}


class IndexResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        """ Return a listing of all categories and their pages """
        return [
            {
                'name': category.name,
                'pages': [
                    marshal(page, WikiPage.resource_fields) for page in
                    category.pages.filter_by(deleted=False).order_by(WikiPage.name.asc()).all()
                ]
            } for category in WikiCategory.query.order_by(WikiCategory.name.asc()).all()
        ]
