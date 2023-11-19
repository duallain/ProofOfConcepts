from pydantic import BaseModel, Field
from typing import Literal, Dict, List
import uuid

# good obj
# MDI_Object(
#     name="mycustom command",
#     command="the command\nthecommand line 2",
#     grid={"xs": 2},
# )

class MDI_Object(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    command: str
    grid: Dict[
        Literal["xs", "sm", "md", "lg", "xl"],
        Literal[
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        ],  # this seems scuffed, but ignoring for now
    ]


class Controller(BaseModel):
    exception: Dict[str, bool]


class State(BaseModel):
    checkForUpdates: bool
    controller: Controller


class Config(BaseModel):
    watchDirectory: str
    accessTokenLifetime: str
    allowRemoteAccess: bool
    state: State
    secret: str
    macros: List  # should probably define this more specifically
    mdi: List[MDI_Object]