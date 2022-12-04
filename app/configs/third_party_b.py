from app.models.third_party_b import Company
from app.configs.base import Base


class ThirdPartyB(Base):

    URL = "https://interview-df854r23.sikoia.com"
    SUPPORTED_JURISDICTIONS = [
        'de',
        'nl'
    ]
    RESPONSE_MODEL = Company

    @property
    def endpoint(self):
        return f"{self.URL}/v1/company-data?jurisdictionCode={self.jurisdiction_code}&companyNumber={self.company_number}"
