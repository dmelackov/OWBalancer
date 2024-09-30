from pydantic import BaseModel


class SettingsRoleAmount(BaseModel):
    tank: int
    damage: int
    support: int


class SettingsTeam(BaseModel):
    name: str
    color: str


class SettingsTeams(BaseModel):
    first: SettingsTeam
    second: SettingsTeam


class SettingsMath(BaseModel):
    balance_limit: int
    alpha: int | float
    beta: int | float
    gamma: int | float
    p: int | float
    q: int | float
    tank_weight: int | float
    damage_weight: int | float
    support_weight: int | float


class Settings(BaseModel):
    auto_custom: bool
    auto_increment: bool
    extended_lobby: bool
    expanded_result: bool
    amount: SettingsRoleAmount
    team: SettingsTeams
    math: SettingsMath
