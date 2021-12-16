from app.DataBase.db import *


class Member:
    def __init__(self, d=None):
        if d:
            self.Player = d["P"]
            self.Roles = d["Roles"]
            self.Custom = d["C"]
            C = Custom.select().where(Custom.ID == self.Custom)
            if C.exists():
                self.Name = C[0].Player.Username
                self.Rating = [C[0].TSR, C[0].DSR, C[0].HSR]
            else:
                self.Name = "None"
                self.Rating = [-1, -1, -1]
            self.isFlex = d["isFlex"]

    def setData(self, P, C):
        self.Player = P
        self.Custom = C
        self.Rating = [C.TSR, C.DSR, C.HSR]
        self.Roles = ""
        self.isFlex = False

    def setRoles(self, R, isFlex):
        self.Roles = [0 if j == "T" else 1 if j == "D" else 2 if j == "H" else -1 for j in R]
        self.isFlex = isFlex

    def serialization(self):
        return {"C": self.Custom.ID, "Roles": self.Roles, "isFlex": self.isFlex, "P": self.Player.ID,
                "Rating": self.Rating}


class Balance:
    def __init__(self, AVG, Mask, PriorityPoints):
        self.AVG = AVG
        self.Mask = Mask
        self.PriorityPoints = PriorityPoints

    def __sub__(self, other):
        return abs(self.AVG - other.AVG)