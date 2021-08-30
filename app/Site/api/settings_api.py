import logging
from flask import Blueprint, request, Response, send_file
from flask_login import login_required, current_user

module_logger = logging.getLogger("api")

api = Blueprint('settings_api', __name__, template_folder='templates',
                static_folder='static')

