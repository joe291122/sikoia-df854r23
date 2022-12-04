from app.models.third_party_a import Company
from app.configs.base import Base


class ThirdPartyA(Base):

    URL = "https://interview-df854r23.sikoia.com"
    SUPPORTED_JURISDICTIONS = [
        'uk',
        'de'
    ]
    RESPONSE_MODEL = Company

    @property
    def endpoint(self):
        return f"{self.URL}/v1/company/{self.jurisdiction_code}/{self.company_number}"
