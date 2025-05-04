from sqlalchemy.orm import Session
from typing import List, Tuple
from . import models, schemas
from math import radians, cos, sin, sqrt, atan2


# 1) Buildings
def get_buildings(db: Session) -> List[models.Building]:
    return db.query(models.Building).all()


# 2) Organizations
def get_org(db: Session, org_id: int) -> models.Organization:
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()


def get_orgs_by_building(db: Session, building_id: int) -> List[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()


def get_orgs_by_name(db: Session, name_substr: str) -> List[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.name.ilike(f"%{name_substr}%")).all()


def get_orgs_by_activity(db: Session, activity_id: int) -> List[models.Organization]:
    return (
        db.query(models.Organization)
            .join(models.Organization.activities)
            .filter(models.Activity.id == activity_id)
            .all()
    )


# 3) Геопоиск: по радиусу (в километрах)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли, км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_orgs_within_radius(db: Session, lat: float, lng: float, radius_km: float) -> List[models.Organization]:
    all_orgs = db.query(models.Organization).all()
    result = []
    for org in all_orgs:
        b = org.building
        if haversine(lat, lng, b.latitude, b.longitude) <= radius_km:
            result.append(org)
    return result


def get_orgs_within_box(db: Session, min_lat: float, max_lat: float, min_lng: float, max_lng: float) -> List[
    models.Organization]:
    return (
        db.query(models.Organization)
            .join(models.Organization.building)
            .filter(models.Building.latitude.between(min_lat, max_lat))
            .filter(models.Building.longitude.between(min_lng, max_lng))
            .all()
    )


# 4) Поиск по дереву деятельностей
def collect_descendants(db: Session, root_id: int, max_depth: int = 3) -> List[int]:
    ids = []

    def dfs(act_id, depth):
        if depth > max_depth:
            return
        ids.append(act_id)
        children = db.query(models.Activity).filter(models.Activity.parent_id == act_id).all()
        for c in children:
            dfs(c.id, depth + 1)

    dfs(root_id, 1)
    return ids


def get_orgs_by_activity_tree(db: Session, root_id: int) -> List[models.Organization]:
    ids = collect_descendants(db, root_id, max_depth=3)
    return (
        db.query(models.Organization)
            .join(models.Organization.activities)
            .filter(models.Activity.id.in_(ids))
            .all()
    )


from sqlalchemy.orm import Session
from typing import List, Tuple
from . import models, schemas
from math import radians, cos, sin, sqrt, atan2


# 1) Buildings
def get_buildings(db: Session) -> List[models.Building]:
    return db.query(models.Building).all()


# 2) Organizations
def get_org(db: Session, org_id: int) -> models.Organization:
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()


def get_orgs_by_building(db: Session, building_id: int) -> List[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()


def get_orgs_by_name(db: Session, name_substr: str) -> List[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.name.ilike(f"%{name_substr}%")).all()


def get_orgs_by_activity(db: Session, activity_id: int) -> List[models.Organization]:
    return (
        db.query(models.Organization)
            .join(models.Organization.activities)
            .filter(models.Activity.id == activity_id)
            .all()
    )


# 3) Геопоиск: по радиусу (в километрах)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли, км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_orgs_within_radius(db: Session, lat: float, lng: float, radius_km: float) -> List[models.Organization]:
    all_orgs = db.query(models.Organization).all()
    result = []
    for org in all_orgs:
        b = org.building
        if haversine(lat, lng, b.latitude, b.longitude) <= radius_km:
            result.append(org)
    return result


def get_orgs_within_box(db: Session, min_lat: float, max_lat: float, min_lng: float, max_lng: float) -> List[
    models.Organization]:
    return (
        db.query(models.Organization)
            .join(models.Organization.building)
            .filter(models.Building.latitude.between(min_lat, max_lat))
            .filter(models.Building.longitude.between(min_lng, max_lng))
            .all()
    )


# 4) Поиск по дереву деятельностей
def collect_descendants(db: Session, root_id: int, max_depth: int = 3) -> List[int]:
    ids = []

    def dfs(act_id, depth):
        if depth > max_depth:
            return
        ids.append(act_id)
        children = db.query(models.Activity).filter(models.Activity.parent_id == act_id).all()
        for c in children:
            dfs(c.id, depth + 1)

    dfs(root_id, 1)
    return ids


def get_orgs_by_activity_tree(db: Session, root_id: int) -> List[models.Organization]:
    ids = collect_descendants(db, root_id, max_depth=3)
    return (
        db.query(models.Organization)
            .join(models.Organization.activities)
            .filter(models.Activity.id.in_(ids))
            .all()
    )
