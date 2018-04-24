from flask import request
from flask_restful import Resource, marshal_with

from ..util import authenticate, restrict_editor, get_user_from_token
from ..models import db, WikiPage, WikiEdit


class PagesResource(Resource):

    @authenticate
    @marshal_with(WikiPage.resource_fields)
    def get(self):
        """ Return all pages (that are not deleted) """
        return WikiPage.query.filter_by(deleted=False).all()

    @restrict_editor
    def post(self):
        """ Create a new page """
        name = request.json['name']
        category_id = request.json['category_id']
        page = WikiPage.query.filter_by(name=name, category_id=category_id).first()
        if not page:
            page = WikiPage(name=name, category_id=category_id)
            db.session.add(page)
            db.session.commit()
            db.session.add(WikiEdit(
                page.id,
                page.category_name,
                get_user_from_token().id,
                request.json['name'],
                ''
            ))
            db.session.commit()
        return {
            'category': page.category.name,
            'page': page.name,
        }


class PageResource(Resource):

    @authenticate
    @marshal_with(WikiPage.resource_fields_full)
    def get(self, id):
        """ Return the data for this page """
        return WikiPage.query.get(id)

    @restrict_editor
    def put(self, id):
        """ Edit the page """
        page = WikiPage.query.get(id)
        db.session.add(WikiEdit(
            page.id,
            page.category_name,
            get_user_from_token().id,
            request.json.get('name', page.name),
            request.json.get('content', page.content),
            request.json.get('deleted', page.deleted)
        ))
        page.name = request.json.get('name', page.name)
        page.category_id = int(request.json.get('category_id', page.category_id))
        page.content = request.json.get('content', page.content)
        page.deleted = request.json.get('deleted', page.deleted)
        db.session.commit()
        return {}, 204

    @restrict_editor
    def delete(self, id):
        """ Delete the page """
        page = WikiPage.query.get(id)
        db.session.add(WikiEdit(
            page.id,
            page.category_name,
            get_user_from_token().id,
            page.name,
            page.content,
            deleted=True
        ))
        page.deleted = True
        db.session.commit()
        return {}, 204


class LookupResource(Resource):

    method_decorators = [authenticate]

    @marshal_with(WikiPage.resource_fields_full)
    def get(self, category_name, page_name):
        """ Return the page by its name and category name """
        for page in WikiPage.query.filter_by(name=page_name).all():
            if page.category.name == category_name:
                return page
        return {}, 404


class DeletedPagesResource(Resource):

    # For now, this endpoint is accessed by the admin page, but
    # the content here isn't anything special, so restrict to editors.
    method_decorators = [restrict_editor]

    @marshal_with(WikiPage.resource_fields)
    def get(self):
        return WikiPage.query.filter_by(deleted=True).all()
