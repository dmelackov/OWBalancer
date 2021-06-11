from flask import Blueprint
from flask_login import login_required
import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
from flask import jsonify

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getPlayers/')
@api.route('/getPlayers/<searchStr>')
@login_required
def getPlayers(searchStr=""):
    players = DataBaseMethods.searchPlayer(searchStr)
    return jsonify(list(map(lambda x: x.getJsonInfo(), players)))
