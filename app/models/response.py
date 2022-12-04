from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class Address(BaseModel):
    street: str
    city: str
    country: str
    postcode: str


class Dates(BaseModel):
    year: int
    month: int
    day: Optional[int]


class Officer(BaseModel):
    first_name: Optional[str]
    middlenames: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    date_from: Dates
    date_to: Optional[Dates]
    role: str
    date_of_birth: Optional[Dates]
    nationality: Optional[str]
    country: Optional[str]


class Owner(BaseModel):
    first_name: Optional[str]
    middlenames: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    date_from: Dates
    date_to: Optional[Dates]
    ownership_type: str
    shares_held: Optional[float]
    date_of_birth: Optional[Dates]
    nationality: Optional[str]
    country: Optional[str]


class Activities(BaseModel):
    activity_code: int
    activity_description: str


class Company(BaseModel):
    company_number: str
    company_name: str
    jurisdiction_code: str
    company_type: str | None = None
    status: str | None = None
    date_established: Dates | None = None
    date_dissolved: Dates | None = None
    official_address: Address
    activities: Optional[List[Activities]]
    officers: Optional[List[Officer]]
    owners: Optional[List[Owner]]
