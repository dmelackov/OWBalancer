from app.DataBase.methods import createDB
from app.Site.SiteMain import FlaskSite
from threading import Thread
import logging.config
import torch


class SiteThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        site = FlaskSite()
        site.startFlask()


# pre-init Network
def minmaxscaler(data):
    mass = []
    for ind, el in enumerate(data):
        mass.append(el / 5000)
    return mass


class Network(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.Sigm = torch.nn.Sigmoid()
        self.fc1 = torch.nn.Linear(6, 12)
        self.Act1 = torch.nn.LeakyReLU()
        self.fc2 = torch.nn.Linear(12, 6)
        self.Act2 = torch.nn.LeakyReLU()
        self.Last = torch.nn.Linear(12, 1)

    def forward(self, x):
        t1 = self.fc1(torch.tensor(minmaxscaler(x[1])))
        t2 = self.fc1(torch.tensor(minmaxscaler(x[0])))
        t1 = self.Act1(t1)
        t2 = self.Act1(t2)
        t1 = self.fc2(t1)
        t2 = self.fc2(t2)
        x = self.Act2(torch.cat((t1, t2), 0))
        x = self.Last(x)
        x = self.Sigm(x)
        return x


logging.config.fileConfig('logging.conf')
createDB()
stThr = SiteThread()
stThr.start()
