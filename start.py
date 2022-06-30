from app.DataBase.methods import createDB
from app.Site.SiteMain import FlaskSite
import logging.config

if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    createDB()
    site = FlaskSite()
    site.startFlask()