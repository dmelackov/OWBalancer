from enum import Enum


class Permissions(Enum):
    add_customs_toLobby = "add_customs_tolobby"
    do_balance = "do_balance"
    change_player_roles = "change_player_roles"
    create_player = "create_player"
    delete_your_player = "delete_your_player"
    change_your_player = "change_your_player"
    create_custom = "create_custom"
    change_your_custom = "change_your_custom"
    delete_your_custom = "delete_your_custom"
    admin_panel_access = "admin_panel_access"
    delete_custom = "delete_custom"
    change_player = "change_player"
    delete_player = "delete_player"
    change_profile_role = "change_profile_role"
    moderate_workspace = "moderate_workspace"
