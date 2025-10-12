from typing import List, Dict, Union, TypeAlias

User: TypeAlias = Dict[str, Union[str, int]]

UserDataset: TypeAlias = List[User]

invalid_data: UserDataset = [
    {"id": 1, "name": 1}
]