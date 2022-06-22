from app.DataBase.db import *


def generate_roles():
    Guest = Roles.create("Guest")
    Customer = Roles.create("Customer")
    Moderator = Roles.create("Moderator")
    Administrator = Roles.create("Administrator")

    add_customs_toLobby = Perms.create("add_customs_tolobby")
    do_balance = Perms.create("do_balance")
    change_player_roles = Perms.create("change_player_roles")
    create_player = Perms.create("create_player")
    delete_your_player = Perms.create("delete_your_player")
    change_your_player = Perms.create("change_your_player")
    create_custom = Perms.create("create_custom")
    change_your_custom = Perms.create("change_your_custom")
    delete_your_custom = Perms.create("delete_your_custom")
    admin_panel_access = Perms.create("admin_panel_access")
    delete_custom = Perms.create("delete_custom")
    change_player = Perms.create("change_player")
    delete_player = Perms.create("delete_player")
    change_profile_role = Perms.create("change_profile_role")

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


def createDB():
    db.create_tables([Profile, Custom, Player, Perms, Roles, RolePerms, Games, PlayerRoles])