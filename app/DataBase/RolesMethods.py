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
def createPermission(Data):
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


def checkProfilePermission(P, Perm):
    Prs = getUserPermissions(P)
    if Prs:
        for i in Prs:
            if i.Name == Perm:
                return True
    return False


def generate_roles():
    Guest = createRole("Guest")
    Customer = createRole("Customer")
    Moderator = createRole("Moderator")
    Administrator = createRole("Administrator")

    add_customs_tolobby = createPermission("add_customs_tolobby")
    do_balance = createPermission("do_balance")
    change_player_roles = createPermission("change_player_roles")
    create_player = createPermission("create_player")
    delete_your_player = createPermission("delete_your_player")
    change_your_player = createPermission("change_your_player")
    create_custom = createPermission("create_custom")
    change_your_custom = createPermission("change_your_custom")
    delete_your_custom = createPermission("delete_your_custom")
    admin_panel_access = createPermission("admin_panel_access")
    delete_custom = createPermission("delete_custom")
    change_player = createPermission("change_player")
    delete_player = createPermission("delete_player")
    change_profile_role = createPermission("change_profile_role")

    # права Guest
    addPermToRole(Guest, add_customs_tolobby)
    addPermToRole(Guest, do_balance)

    # Права Customer
    addPermToRole(Customer, create_player)
    addPermToRole(Customer, delete_your_player)
    addPermToRole(Customer, change_your_player)
    addPermToRole(Customer, create_custom)
    addPermToRole(Customer, change_your_custom)
    addPermToRole(Customer, delete_your_custom)
    addPermToRole(Customer, change_player_roles)
    addPermToRole(Customer, add_customs_tolobby)
    addPermToRole(Customer, do_balance)

    # Права Moderator
    addPermToRole(Moderator, create_player)
    addPermToRole(Moderator, delete_your_player)
    addPermToRole(Moderator, change_your_player)
    addPermToRole(Moderator, create_custom)
    addPermToRole(Moderator, change_your_custom)
    addPermToRole(Moderator, change_player_roles)
    addPermToRole(Moderator, delete_your_custom)
    addPermToRole(Moderator, add_customs_tolobby)
    addPermToRole(Moderator, do_balance)
    addPermToRole(Moderator, delete_player)
    addPermToRole(Moderator, change_player)
    addPermToRole(Moderator, delete_custom)

    # права Administrator
    addPermToRole(Administrator, create_player)
    addPermToRole(Administrator, delete_your_player)
    addPermToRole(Administrator, change_your_player)
    addPermToRole(Administrator, create_custom)
    addPermToRole(Administrator, change_your_custom)
    addPermToRole(Administrator, change_player_roles)
    addPermToRole(Administrator, delete_your_custom)
    addPermToRole(Administrator, add_customs_tolobby)
    addPermToRole(Administrator, do_balance)
    addPermToRole(Administrator, delete_player)
    addPermToRole(Administrator, change_player)
    addPermToRole(Administrator, delete_custom)
    addPermToRole(Administrator, admin_panel_access)
    addPermToRole(Administrator, change_profile_role)


# generate_roles()
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
