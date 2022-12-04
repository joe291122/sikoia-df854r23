from pydantic import BaseModel, ValidationError, validator


#TODO: Ideally, pull this from a DB
JURISDICTION_CODES = [
    'uk',
    'de',
    'nl'
]

#TODO: run this against a DB
VALID_COMPANY_NUMBERS = [
    ('uk', '1111'),
    ('uk', '2222'),
    ('de', '3333'),
    ('de', '4444'),
    ('nl', '5555'),
    ('nl', '6666'),
]

class Input(BaseModel):
    jurisdiction_code: str
    company_number: str

    @validator('jurisdiction_code')
    def code_must_be_valid(cls, v):
        if v.lower() not in JURISDICTION_CODES:
            raise ValueError('must be a valid Jurisdiction Code')
        return v.lower()

    @validator('company_number')
    def company_number_must_be_valid(cls, v, values):
        if 'jurisdiction_code' in values and (values['jurisdiction_code'], v) not in VALID_COMPANY_NUMBERS:
            raise ValueError('must be a valid Company Number')
        return v
