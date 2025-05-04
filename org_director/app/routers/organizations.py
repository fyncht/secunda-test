# app/routers/organizations.py
from __future__ import annotations
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas, database
from ..database import get_db
from ..dependencies import get_api_key

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[schemas.Organization])
def list_orgs(
    name: Optional[str] = Query(None, description="По подстроке названия"),
    activity_id: Optional[int] = Query(None, description="ID activity"),
    lat: Optional[float] = Query(None, description="latitude"),
    lng: Optional[float] = Query(None, description="longitude"),
    radius: Optional[float] = Query(None, description="в км"),
    min_lat: Optional[float] = Query(None, description="bounding-box min lat"),
    max_lat: Optional[float] = Query(None, description="bounding-box max lat"),
    min_lng: Optional[float] = Query(None, description="bounding-box min lng"),
    max_lng: Optional[float] = Query(None, description="bounding-box max lng"),
    db: Session = Depends(get_db),
):
    if name:
        return crud.get_orgs_by_name(db, name)
    if activity_id and not (lat or min_lat):
        return crud.get_orgs_by_activity_tree(db, activity_id)
    if lat is not None and lng is not None and radius is not None:
        return crud.get_orgs_within_radius(db, lat, lng, radius)
    if None not in (min_lat, max_lat, min_lng, max_lng):
        return crud.get_orgs_within_box(db, min_lat, max_lat, min_lng, max_lng)
    return db.query(crud.models.Organization).all()


@router.get("/{org_id}", response_model=schemas.Organization)
def get_org(
    org_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_org(db, org_id)
