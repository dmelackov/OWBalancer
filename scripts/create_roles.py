from DataBase.database import sessionmanager
from DataBase.repository import PermissionRepository, RoleRepository

async def create_roles():
    async with sessionmanager.session() as session:
        role_repository = RoleRepository(session)
        permission_repository = PermissionRepository(session)

        Guest = await role_repository.create("Guest")
        Customer = await role_repository.create("Customer")
        Moderator = await role_repository.create("Moderator")
        Administrator = await role_repository.create("Administrator")

        add_customs_toLobby = await permission_repository.create("add_customs_tolobby")
        do_balance = await permission_repository.create("do_balance")
        change_player_roles = await permission_repository.create("change_player_roles")
        create_player = await permission_repository.create("create_player")
        delete_your_player = await permission_repository.create("delete_your_player")
        change_your_player = await permission_repository.create("change_your_player")
        create_custom = await permission_repository.create("create_custom")
        change_your_custom = await permission_repository.create("change_your_custom")
        delete_your_custom = await permission_repository.create("delete_your_custom")
        admin_panel_access = await permission_repository.create("admin_panel_access")
        delete_custom = await permission_repository.create("delete_custom")
        change_player = await permission_repository.create("change_player")
        delete_player = await permission_repository.create("delete_player")
        change_profile_role = await permission_repository.create("change_profile_role")
        moderate_workspace = await permission_repository.create("moderate_workspace")

        # права Guest
        await role_repository.add_permission(Guest, add_customs_toLobby)
        await role_repository.add_permission(Guest, change_player_roles)
        await role_repository.add_permission(Guest, do_balance)

        # Права Customer
        await role_repository.add_permission(Customer, create_player)
        await role_repository.add_permission(Customer, delete_your_player)
        await role_repository.add_permission(Customer, change_your_player)
        await role_repository.add_permission(Customer, create_custom)
        await role_repository.add_permission(Customer, change_your_custom)
        await role_repository.add_permission(Customer, delete_your_custom)
        await role_repository.add_permission(Customer, change_player_roles)
        await role_repository.add_permission(Customer, add_customs_toLobby)
        await role_repository.add_permission(Customer, do_balance)

        # Права Moderator
        await role_repository.add_permission(Moderator, create_player)
        await role_repository.add_permission(Moderator, delete_your_player)
        await role_repository.add_permission(Moderator, change_your_player)
        await role_repository.add_permission(Moderator, create_custom)
        await role_repository.add_permission(Moderator, change_your_custom)
        await role_repository.add_permission(Moderator, change_player_roles)
        await role_repository.add_permission(Moderator, delete_your_custom)
        await role_repository.add_permission(Moderator, add_customs_toLobby)
        await role_repository.add_permission(Moderator, do_balance)
        await role_repository.add_permission(Moderator, delete_player)
        await role_repository.add_permission(Moderator, change_player)
        await role_repository.add_permission(Moderator, delete_custom)

        # права Administrator
        await role_repository.add_permission(Administrator, create_player)
        await role_repository.add_permission(Administrator, delete_your_player)
        await role_repository.add_permission(Administrator, change_your_player)
        await role_repository.add_permission(Administrator, create_custom)
        await role_repository.add_permission(Administrator, change_your_custom)
        await role_repository.add_permission(Administrator, change_player_roles)
        await role_repository.add_permission(Administrator, delete_your_custom)
        await role_repository.add_permission(Administrator, add_customs_toLobby)
        await role_repository.add_permission(Administrator, do_balance)
        await role_repository.add_permission(Administrator, delete_player)
        await role_repository.add_permission(Administrator, change_player)
        await role_repository.add_permission(Administrator, delete_custom)
        await role_repository.add_permission(Administrator, admin_panel_access)
        await role_repository.add_permission(Administrator, change_profile_role)
        await role_repository.add_permission(Administrator, moderate_workspace)

        await session.commit()

