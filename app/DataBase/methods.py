import random

from app.DataBase.db import *


def generate_roles():
    Guest = Roles.create("Guest").data
    Customer = Roles.create("Customer").data
    Moderator = Roles.create("Moderator").data
    Administrator = Roles.create("Administrator").data

    add_customs_toLobby = Perms.create("add_customs_tolobby").data
    do_balance = Perms.create("do_balance").data
    change_player_roles = Perms.create("change_player_roles").data
    create_player = Perms.create("create_player").data
    delete_your_player = Perms.create("delete_your_player").data
    change_your_player = Perms.create("change_your_player").data
    create_custom = Perms.create("create_custom").data
    change_your_custom = Perms.create("change_your_custom").data
    delete_your_custom = Perms.create("delete_your_custom").data
    admin_panel_access = Perms.create("admin_panel_access").data
    delete_custom = Perms.create("delete_custom").data
    change_player = Perms.create("change_player").data
    delete_player = Perms.create("delete_player").data
    change_profile_role = Perms.create("change_profile_role").data

    # права Guest
    RolePerms.create(Guest, add_customs_toLobby)
    RolePerms.create(Guest, do_balance)

    # Права Customer
    RolePerms.create(Customer, create_player)
    RolePerms.create(Customer, delete_your_player)
    RolePerms.create(Customer, change_your_player)
    RolePerms.create(Customer, create_custom)
    RolePerms.create(Customer, change_your_custom)
    RolePerms.create(Customer, delete_your_custom)
    RolePerms.create(Customer, change_player_roles)
    RolePerms.create(Customer, add_customs_toLobby)
    RolePerms.create(Customer, do_balance)

    # Права Moderator
    RolePerms.create(Moderator, create_player)
    RolePerms.create(Moderator, delete_your_player)
    RolePerms.create(Moderator, change_your_player)
    RolePerms.create(Moderator, create_custom)
    RolePerms.create(Moderator, change_your_custom)
    RolePerms.create(Moderator, change_player_roles)
    RolePerms.create(Moderator, delete_your_custom)
    RolePerms.create(Moderator, add_customs_toLobby)
    RolePerms.create(Moderator, do_balance)
    RolePerms.create(Moderator, delete_player)
    RolePerms.create(Moderator, change_player)
    RolePerms.create(Moderator, delete_custom)

    # права Administrator
    RolePerms.create(Administrator, create_player)
    RolePerms.create(Administrator, delete_your_player)
    RolePerms.create(Administrator, change_your_player)
    RolePerms.create(Administrator, create_custom)
    RolePerms.create(Administrator, change_your_custom)
    RolePerms.create(Administrator, change_player_roles)
    RolePerms.create(Administrator, delete_your_custom)
    RolePerms.create(Administrator, add_customs_toLobby)
    RolePerms.create(Administrator, do_balance)
    RolePerms.create(Administrator, delete_player)
    RolePerms.create(Administrator, change_player)
    RolePerms.create(Administrator, delete_custom)
    RolePerms.create(Administrator, admin_panel_access)
    RolePerms.create(Administrator, change_profile_role)


tables = ['custom', 'games', 'perms', 'player', 'playerroles', 'profile', 'roleperms', 'roles',
          'workspace', 'workspaceprofile', 'keydata']
role_tabels = ['perms', 'roleperms', 'roles']


def createDB():
    if any(table not in db.get_tables() for table in tables):
        if any(table not in db.get_tables() for table in role_tabels):
            db.drop_tables([Perms, RolePerms, Roles])
            db.create_tables([Perms, RolePerms, Roles])
            generate_roles()
        db.create_tables([Profile, Custom, Player, Games, PlayerRoles, Workspace, WorkspaceProfile, KeyData])
        return AnswerForm(status=True, error=None)
    return AnswerForm(status=False, error=None)


# if __name__ == "__main__":
#     U = WorkspaceProfile.get(WorkspaceProfile.ID == 1)
#     C = Custom.getInstance(13)
#     print(U.addToLobby(C))
    # print(U)
    # createDB()
    # U = Profile.create("Ivarys", "123").data
    # W = Workspace.create(U, "IvarysWorkspace", '{"CustomSystem": true}').data
    # WU = WorkspaceProfile.create(U, W).data
    # # U = Profile.getInstance(1)
    # # W = Workspace.getInstance(1)
    # # WU = WorkspaceProfile.getInstance(1)
    # for i in range(12):
    #     P = Player.create(WU, str(i)).data
    #     PR = PlayerRoles.getPR(WU, P).data
    #     PR.setFlex(True)
    #     C = Custom.create(WU, P).data
    #     C.changeSR("T", random.randint(1000, 2000))
    #     C.changeSR("H", random.randint(1000, 2000))
    #     C.changeSR("D", random.randint(1000, 2000))
