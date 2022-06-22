from app.DataBase.methods.methods import createDB
from app.Site.SiteMain import FlaskSite
from threading import Thread
import logging.config
import multiprocessing
class SiteThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        site = FlaskSite()
        site.startFlask()
if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    createDB()
    multiprocessing.freeze_support()
    stThr = SiteThread()
    stThr.start()  
    stThr.join()
