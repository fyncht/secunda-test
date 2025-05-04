# app/routers/activities.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas, database
from ..database import get_db
from ..dependencies import get_api_key

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[schemas.Activity])
def list_activities(
    db: Session = Depends(get_db),
):
    return db.query(crud.models.Activity).all()


@router.get("/{activity_id}/organizations", response_model=list[schemas.Organization])
def orgs_by_activity(
    activity_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_orgs_by_activity(db, activity_id)


@router.get("/{activity_id}/organizations_tree", response_model=list[schemas.Organization])
def orgs_by_activity_tree(
    activity_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_orgs_by_activity_tree(db, activity_id)
