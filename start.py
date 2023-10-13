from app.DataBase.methods import createDB
import logging.config
from app.Site.main import Site

logging.config.fileConfig('logging.conf')

site = Site()
siteApp = site.app

if __name__ == "__main__":
    createDB()
    site.start()
