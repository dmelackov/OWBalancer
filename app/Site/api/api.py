from flask import Blueprint
import logging
from app.Site.api.customs_api import api as customs_api
from app.Site.api.profile_api import api as profile_api
from app.Site.api.players_api import api as players_api
from app.Site.api.lobby_api import api as lobby_api


module_logger = logging.getLogger("api")

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static')

api.register_blueprint(customs_api, url_prefix='/customs')
api.register_blueprint(profile_api, url_prefix='/profile')
api.register_blueprint(players_api, url_prefix='/players')
api.register_blueprint(lobby_api, url_prefix='/lobby')
