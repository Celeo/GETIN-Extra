from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from preston import Preston

from .models import db
from .shared import eveapi, config
from .views.login import EVE_SSO_Resource
from .views.token import Token_Resource
from .views.user import UserResource

from .views.wiki_category import WikiCategoriesResource, WikiCategoryResource, IndexResource
from .views.wiki_page import PagesResource, PageResource, LookupResource, DeletedPagesResource
from .views.wiki_edit import EditResource, RollbackResource

from .views.fits_fit import FitsResource, FitResource
from .views.fits_category import FitsCategoriesResource, FitsCategoryResource


# generic setup
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
config.update(app.config)

CORS(app)
api = Api(app)

db.app = app
db.init_app(app)

# EVE API setup
eveapi['user_agent'] = 'github.com/Celeo/GETIN-Extra for GETIN alliance'
eveapi['preston'] = Preston(
    user_agent=eveapi['user_agent'],
    client_id=app.config['EVE_OAUTH_CLIENT_ID'],
    client_secret=app.config['EVE_OAUTH_SECRET'],
    callback_url=app.config['EVE_OAUTH_CALLBACK']
)


@app.route('/')
def index():
    """ Basic top-level smoketest-ish endpoint """
    return jsonify({
        'message': 'API index page'
    })


# cross-functionality endpoints
api.add_resource(EVE_SSO_Resource, '/eve/sso')
api.add_resource(Token_Resource, '/tokens')
api.add_resource(UserResource, '/admin')

# wiki endpoints
api.add_resource(WikiCategoriesResource, '/wiki/category')
api.add_resource(WikiCategoryResource, '/wiki/category/<int:id>')
api.add_resource(PagesResource, '/wiki/page')
api.add_resource(PageResource, '/wiki/page/<int:id>')
api.add_resource(EditResource, '/wiki/history/<int:page_id>')
api.add_resource(RollbackResource, '/wiki/rollback/<int:id>')
api.add_resource(LookupResource, '/wiki/lookup/<category_name>/<page_name>')
api.add_resource(IndexResource, '/wiki/index')
api.add_resource(DeletedPagesResource, '/wiki/deleted_pages')

# fits endpoints
api.add_resource(FitsResource, '/fits/fits')
api.add_resource(FitResource, '/fits/fits/<int:id>')
api.add_resource(FitsCategoriesResource, '/fits/categories')
api.add_resource(FitsCategoryResource, '/fits/categories/<int:id>')
