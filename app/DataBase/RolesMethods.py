from app.DataBase.db import *


# Создание ролей
def createRole(Name):
    R = Roles.select().where(Roles.Name == Name)
    if not R.exists():
        R = Roles.create(Name=Name)
        return R
    else:
        return False


# Создание прав
def createPermision(Data):
    Perm = Perms.select().where(Perms.Name == Data)
    if not Perm.exists():
        Perm = Perms.create(Name=Data)
        return Perm
    else:
        return False


# Прикрепление ролей и прав
def addPermToRole(Role, Perm):
    RP = RolePerms.select().where(RolePerms.Perm == Perm, RolePerms.Role == Role)
    if not RP.exists():
        RP = RolePerms.create(Perm=Perm, Role=Role)
        return RP
    else:
        return False


# выдать человеку роль
def addRoleToProfile(P, Role):
    if P.Role != Role:
        P.Role = Role
        P.save()
        return True
    else:
        return False


# -----------------------------------------

def getUserPermissions(P):
    if P.Role is not None:
        RPs = RolePerms.select().where(RolePerms.Role == P.Role)
        mass = []
        for RP in RPs:
            mass.append(RP)
        return mass
    else:
        return None


# createRole("RoleTest")
# createPermision("PermTest2")
# addPermToRole(
#     Roles.select().where(Roles.Name == "RoleTest")[0],
#     Perms.select().where(Perms.Name == "PermTest2")[0]
# )
# addRoleToProfile(
#     Profile.select().where(Profile.Username == "Ivarys")[0],
#     Roles.select().where(Roles.Name == "RoleTest")[0]
# )
# getUserPermissions(Profile.select().where(Profile.Username == "Ivarys")[0])
