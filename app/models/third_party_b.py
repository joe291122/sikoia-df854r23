from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional


def parse_date(value: str):
    return Dates(date_object=datetime.strptime(value,"%d/%m/%Y").date())


class Dates(BaseModel):
    year: int
    month: int
    day: int

    def __init__(self, date_object, **data):
        super().__init__(
            year=datetime.strftime(date_object,"%Y"),
            month=datetime.strftime(date_object,"%m"),
            day=datetime.strftime(date_object,"%d"),
            **data
        )


class Address(BaseModel):
    street: str
    city: str
    country: str
    postcode: str


class PersonalOfficer(BaseModel):
    name: str
    date_from: Dates = Field(alias="dateFrom")
    date_to: Optional[Dates] = Field(alias="dateTo")
    role: str = Field(alias="type")
    date_of_birth: Dates = Field(alias="birthDate")
    nationality: str

    @validator("date_from", pre=True)
    def parse_dateFrom(cls, v):
        if v:
            return parse_date(v)

    @validator("date_to", pre=True)
    def parse_dateTo(cls, v):
        if v:
            return parse_date(v)

    @validator("date_of_birth", pre=True)
    def parse_birthDate(cls, v):
        if v:
            return parse_date(v)


class CorporateOfficer(BaseModel):
    name: str
    date_from: Dates = Field(alias="dateFrom")
    date_to: Optional[Dates] = Field(alias="dateTo")
    role: str = Field(alias="type")
    country: str

    @validator("date_from", pre=True)
    def parse_dateFrom(cls, v):
        if v:
            return parse_date(v)

    @validator("date_to", pre=True)
    def parse_dateTo(cls, v):
        if v:
            return parse_date(v)


class PersonalOwner(BaseModel):
    name: str
    date_from: Dates = Field(alias="dateFrom")
    date_to: Optional[Dates] = Field(alias="dateTo")
    role: str = Field(alias="type")
    shares_held: float | None = Field(default_value=None, alias="ownership")
    ownership_type: str = "Shareholder"
    date_of_birth: Optional[Dates] = Field(default_value=None, alias="birthDate")
    nationality: Optional[str]

    @validator("date_from", pre=True)
    def parse_dateFrom(cls, v):
        if v:
            return parse_date(v)

    @validator("date_to", pre=True)
    def parse_dateTo(cls, v):
        if v:
            return parse_date(v)

    @validator("date_of_birth", pre=True)
    def parse_birthDate(cls, v):
        if v:
            return parse_date(v)


class CorporateOwner(BaseModel):
    name: str
    date_from: Dates = Field(alias="dateFrom")
    date_to: Optional[Dates] = Field(alias="dateTo")
    role: str = Field(alias="type")
    country: Optional[str]
    shares_held: float | None = Field(default_value=None, alias="ownership")
    ownership_type: str = "Shareholder"
    
    @validator("date_from", pre=True)
    def parse_dateFrom(cls, v):
        if v:
            return parse_date(v)

    @validator("date_to", pre=True)
    def parse_dateTo(cls, v):
        if v:
            return parse_date(v)


class Activities(BaseModel):
    activity_code: int = Field(alias="activityCode")
    activity_description: str = Field(alias="activityDescription")


class Company(BaseModel):
    company_number: str = Field(alias="companyNumber")
    company_name: str = Field(alias="companyName")
    jurisdiction_code: str = Field(alias="country")
    date_established: Optional[Dates] = Field(alias="dateFrom")
    date_dissolved: Optional[Dates] = Field(alias="dateTo")
    official_address: Address = Field(alias="address")
    activities: Optional[List[Activities]]
    officers: Optional[List[PersonalOfficer | CorporateOfficer]]
    owners: Optional[List[PersonalOwner | CorporateOwner]]

    def __init__(self, relatedPersons, relatedCompanies, **data):

        officers = []
        if relatedPersons:
            for i in relatedPersons:
                if i['type'] != 'Owner':
                    officers.append(PersonalOfficer(**i))
        if relatedCompanies:
            for i in relatedCompanies:
                if i['type'] != 'Owner':
                    officers.append(CorporateOfficer(**i))

        owners = []
        if relatedPersons:
            for i in relatedPersons:
                if i['type'] == 'Owner':
                    owners.append(PersonalOwner(**i))
        if relatedCompanies:
            for i in relatedCompanies:
                if i['type'] == 'Owner':
                    owners.append(CorporateOwner(**i))

        super().__init__(
            officers=officers,
            owners=owners,
            **data
        )

    @validator("date_established", pre=True)
    def parse_dateFrom(cls, v):
        if v:
            return parse_date(v)

    @validator("date_dissolved", pre=True)
    def parse_dateTo(cls, v):
        if v:
            return parse_date(v)

    @validator("official_address", pre=True)
    def parse_official_address(cls, v):
        if v:
            split_ad = [x.strip() for x in v.split(',')]
            # this needs a lot more work
            return Address(
                street=split_ad[0],
                city=split_ad[1],
                country=split_ad[2],
                postcode=split_ad[3]
            )
    