import unittest
from pydantic import BaseModel
from app.configs import base
from app.models.input import Input


class MockResponse(BaseModel):
    name: str


class TestBase(unittest.TestCase):

    def test_class_variables(self):
        self.assertIsNone(base.Base.URL)
        self.assertListEqual(base.Base.SUPPORTED_JURISDICTIONS, [])
        self.assertIsNone(base.Base.RESPONSE_MODEL)

    def test_init(self):
        result = base.Base(
            input=Input(jurisdiction_code='uk', company_number='1111'),
        )
        self.assertEqual(result.jurisdiction_code, 'uk')
        self.assertEqual(result.company_number, '1111')
        self.assertIsNone(result.response_object)

    def test_endpoint(self):
        with self.assertRaises(NotImplementedError):
            b = base.Base(
                input=Input(jurisdiction_code='uk', company_number='1111'),
            )
            b.endpoint

    def test_parse_repsonse(self):
        b = base.Base(
                input=Input(jurisdiction_code='uk', company_number='1111'),
            )
        response = {'name':'test'}
        b.RESPONSE_MODEL = MockResponse
        b.parse_response(response=response)
        self.assertIsInstance(b.response_object, MockResponse)
        self.assertEqual(b.response_object.name, 'test')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBase)
    unittest.TextTestRunner(verbosity=2).run(suite)