from sqlmodel import Field, SQLModel


# Shared properties
class FarmBase(SQLModel):
    name: str
    description: str | None = None


# Properties to receive on farm creation
class FarmCreate(FarmBase):
    name: str


# Properties to receive on item update
class FarmUpdate(FarmBase):
    name: str | None = None
    description: str | None = None


# Database model, database table inferred from class name
class Farm(FarmBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None


# properties to return via API, id is always required
class FarmOut(FarmBase):
    id: int
    name: str


class FarmsOut(SQLModel):
    data: list[FarmOut]
    count: int
