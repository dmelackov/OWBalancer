from app.DataBase.methods import createDB
from app.Site.SiteMain import FlaskSite
from threading import Thread
import logging.config


class SiteThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        site = FlaskSite()
        site.startFlask()


if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    createDB()
    site = FlaskSite()
    site.startFlask()
    #stThr = SiteThread()
    #stThr.start()  
    #stThr.join()
