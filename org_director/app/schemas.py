from typing import List, Optional
from pydantic import BaseModel, Field


class PhoneBase(BaseModel):
    number: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int

    class Config:
        orm_mode = True


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []

    class Config:
        orm_mode = True


Activity.update_forward_refs()


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    activities_ids: List[int] = Field(default_factory=list)
    phones: List[PhoneCreate] = Field(default_factory=list)


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity]
    phones: List[Phone]

    class Config:
        orm_mode = True
