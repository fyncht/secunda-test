from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..database import get_db
from ..dependencies import get_api_key

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[schemas.Building])
def list_buildings(db: Session = Depends(get_db)):
    return crud.get_buildings(db)


@router.get("/{building_id}/organizations", response_model=list[schemas.Organization])
def orgs_in_building(
        building_id: int,
        db: Session = Depends(get_db),
):
    return crud.get_orgs_by_building(db, building_id)
