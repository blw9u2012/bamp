from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.models import Farm, FarmCreate, FarmOut, FarmsOut, FarmUpdate, Message

router = APIRouter()


@router.get("/", response_model=FarmsOut)
def read_farms(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve Farms
    """
    if current_user.is_superuser:
        statement = select(func.count()).select_from(Farm)
        count = session.exec(statement).one()
        statement = select(Farm).offset(skip).limit(limit)
        farms = session.exec(statement).all()
    else:
        statement = select(func.count()).select_from(Farm)
        count = session.exec(statement).one()
        statement = select(Farm).offset(skip).limit(limit)
        farms = session.exec(statement).all()
    return FarmsOut(data=farms, count=count)


@router.get("/{id}", response_model=FarmOut)
def read_farm(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get farm by ID
    """
    farm = session.get(Farm, id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm


@router.post("/", response_model=FarmOut)
def create_farm(
    *, session: SessionDep, current_user: CurrentUser, farm_in: FarmCreate
) -> Any:
    """
    Create a new farm
    """
    farm = Farm.model_validate(farm_in)
    session.add(farm)
    session.commit()
    session.refresh(farm)
    return farm


@router.put("/{id}", response_model=FarmOut)
def update_farm(
    *, session: SessionDep, current_user: CurrentUser, id: int, farm_in: FarmUpdate
) -> Any:
    """
    Update a farm
    """
    farm = session.get(Farm, id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    update_dict = farm_in.model_dump(exclude_unset=True)
    farm.sqlmodel_update(update_dict)
    session.add(farm)
    session.commit()
    session.refresh(farm)
    return farm


@router.delete("/{id}")
def delete_farm(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete a farm
    """
    farm = session.get(Farm, id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if not current_user.is_superuser and (farm.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(farm)
    session.commit()
    return Message(message="Farm deleted successfully")
