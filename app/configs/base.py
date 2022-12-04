from app.models.third_party_a import Company


class Base:

    URL = None
    SUPPORTED_JURISDICTIONS = []
    RESPONSE_MODEL = None
    
    def __init__(self, input):
        self.jurisdiction_code = input.jurisdiction_code
        self.company_number = input.company_number
        self.response_object: self.RESPONSE_MODEL = None

    @property
    def endpoint(self):
        raise NotImplementedError()

    def parse_response(self, response):
        self.response_object = self.RESPONSE_MODEL(**response)
