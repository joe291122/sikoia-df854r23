from pydantic import BaseModel, validator
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


class CorporateOwner(BaseModel):
    name: str
    date_from: Dates
    date_to: Optional[Dates]
    ownership_type: str
    shares_held: Optional[float]


class PersonalOwner(BaseModel):
    first_name: str
    middlenames: Optional[str]
    last_name: str
    date_from: Dates
    date_to: Optional[Dates]
    ownership_type: str
    shares_held: Optional[float]
    date_of_birth: Dates


class Company(BaseModel):
    company_number: str
    company_name: str
    jurisdiction_code: str
    company_type: str
    status: str
    date_established: Optional[Dates]
    date_dissolved: Optional[Dates]
    official_address: Address
    officers: List[Officer]
    owners: List[CorporateOwner | PersonalOwner] = []

    def __init__(self, owners, **data):

        new_owners = []
        if owners:
            for i in owners:
                if 'name' in i:
                    new_owners.append(CorporateOwner(**i))
                else:
                    new_owners.append(PersonalOwner(**i))

        super().__init__(
            owners=new_owners,
            **data
        )
