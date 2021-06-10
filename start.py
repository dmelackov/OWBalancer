from app.DataBase.methods import createDB
from app.Site.SiteMain import FlaskSite
from threading import Thread


class SiteThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        site = FlaskSite()
        site.startFlask()


createDB()
stThr = SiteThread()
stThr.start()
