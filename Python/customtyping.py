from typing import List, Dict, Union, TypeAlias, TypedDict, Required, NotRequired, ReadOnly

User: TypeAlias = Dict[str, Union[str, int]]

UserDataset: TypeAlias = List[User]

invalid_data: UserDataset = [
    {"id": 1, "name": 1}
]

class Settings(TypedDict):
    notificationsEnabled: NotRequired[bool]
    notificationsVolume: NotRequired[int]

class CustomUser(TypedDict):
    id: ReadOnly[int]
    username: str
    avatar: str
    settings: Settings


Usuario: CustomUser = {"id": 2}
Usuario["id"] = 3
