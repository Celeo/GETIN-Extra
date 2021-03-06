from datetime import datetime

from flask_restful import fields

from .shared import db


class User(db.Model):

    __tablename__ = 'user'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'corporation': fields.String,
        'alliance': fields.String,
        'editor': fields.Boolean,
        'admin': fields.Boolean,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    corporation = db.Column(db.String)
    alliance = db.Column(db.String)
    editor = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, corporation, alliance, editor=True, admin=False):
        self.name = name
        self.corporation = corporation
        self.alliance = alliance
        self.editor = editor
        self.admin = admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def in_alliance(self):
        return self.alliance == 'The Society For Unethical Treatment Of Sleepers'

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return '<User-{}>'.format(self.name)


class WikiCategory(db.Model):

    __tablename__ = 'wiki_category'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pages = db.relationship('WikiPage', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class WikiPage(db.Model):

    __tablename__ = 'wiki_page'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'category_id': fields.Integer,
        'category_name': fields.String,
        'deleted': fields.Integer,
    }

    resource_fields_full = {
        'id': fields.Integer,
        'name': fields.String,
        'content': fields.String,
        'category_id': fields.Integer,
        'category_name': fields.String,
        'deleted': fields.Integer,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('wiki_category.id'))
    content = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    edits = db.relationship('WikiEdit', backref='page', lazy='dynamic')

    def __init__(self, name, category_id, content=''):
        self.name = name
        self.category_id = category_id
        self.content = content
        self.deleted = False

    @property
    def category_name(self):
        return self.category.name


class WikiEdit(db.Model):

    __tablename__ = 'wiki_edit'

    resource_fields = {
        'id': fields.Integer,
        'page_id': fields.Integer,
        'category_name': fields.String,
        'user_id': fields.Integer,
        'new_name': fields.String,
        'deleted': fields.Boolean,
        'timestamp': fields.DateTime,
        'approved_by': fields.String,
        'user_name': fields.String,
        'timestamp_print': fields.String
    }

    resource_fields_full = {
        'id': fields.Integer,
        'page_id': fields.Integer,
        'category_name': fields.String,
        'user_id': fields.Integer,
        'new_name': fields.String,
        'new_content': fields.String,
        'deleted': fields.Boolean,
        'timestamp': fields.DateTime,
        'approved_by': fields.String,
        'user_name': fields.String,
        'timestamp_print': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('wiki_page.id'))
    category_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    new_name = db.Column(db.String)
    new_content = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    approved_by = db.Column(db.String)

    def __init__(self, page_id, category_name, user_id, new_name, new_content, deleted=False, approved_by='*server*'):
        self.page_id = page_id
        self.category_name = category_name
        self.user_id = user_id
        self.new_name = new_name
        self.new_content = new_content
        self.deleted = deleted
        self.timestamp = datetime.utcnow()
        self.approved_by = approved_by

    @property
    def user_name(self):
        return User.query.get(self.user_id).name

    @property
    def timestamp_print(self):
        return self.timestamp.strftime('%b %d, %Y @ %H:%M:%S')


class FitsCategory(db.Model):

    __tablename__ = 'fits_category'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'order': fields.Integer,
        'has_linked_fits': fields.Boolean
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    order = db.Column(db.Integer)
    fits = db.relationship('FitsFit', backref='category', lazy='dynamic')

    def __init__(self, name, order=100):
        self.name = name
        self.order = order

    @property
    def has_linked_fits(self):
        return self.fits.count() > 0


class FitsFit(db.Model):

    __tablename__ = 'fits_fit'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'category_id': fields.Integer,
        'content': fields.String,
        'order': fields.Integer,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('fits_category.id'))
    content = db.Column(db.String)
    order = db.Column(db.Integer)

    def __init__(self, name, category_id=None, content='', order=100):
        self.name = name
        self.category_id = category_id or FitsCategory.query.first().id
        self.content = content
        self.order = order
