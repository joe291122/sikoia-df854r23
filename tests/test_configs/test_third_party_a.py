import json
import unittest
from app.configs import third_party_a
from app.models.input import Input
from app.models.third_party_a import Company


RAW_1111 = 'tests/data/raw_third_party_a_uk_1111.json'
RAW_3333 = 'tests/data/raw_third_party_a_de_3333.json'
RAW_4444 = 'tests/data/raw_third_party_a_de_4444.json'
RESULT_1111 = 'tests/data/parsed_third_party_a_uk_1111.json'
RESULT_3333 = 'tests/data/parsed_third_party_a_de_3333.json'
RESULT_4444 = 'tests/data/parsed_third_party_a_de_4444.json'


class TestThirdPartyA(unittest.TestCase):

    def _open_file(self, file):

        with open(file) as f:
            return json.loads(f.read())

    def test_class_variables(self):
        self.assertEqual(third_party_a.ThirdPartyA.URL,  "https://interview-df854r23.sikoia.com")
        self.assertListEqual(third_party_a.ThirdPartyA.SUPPORTED_JURISDICTIONS, [
            'uk',
            'de'
        ])
        self.assertEqual(third_party_a.ThirdPartyA.RESPONSE_MODEL,  Company)

    def test_endpoint(self):
        b = third_party_a.ThirdPartyA(
            input=Input(jurisdiction_code='uk', company_number='1111')
        )
        self.assertEqual(b.endpoint, "https://interview-df854r23.sikoia.com/v1/company/uk/1111")

    def test_parse_repsonse(self):

        with self.subTest("UK: 1111"):
            b = third_party_a.ThirdPartyA(
                    input=Input(jurisdiction_code='uk', company_number='1111')
                ) 
            response = self._open_file(RAW_1111)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_1111))
            self.assertEqual(b.response_object.company_number, '1111')
            self.assertEqual(b.response_object.company_name, 'Breaking Bad Ltd')
            self.assertEqual(b.response_object.jurisdiction_code, 'uk')
            self.assertIsNotNone(b.response_object.officers)
            self.assertIsNotNone(b.response_object.owners)
            self.assertEqual(len(b.response_object.officers), 2)
            self.assertEqual(len(b.response_object.owners), 2)

        with self.subTest("DE: 3333"):
            b = third_party_a.ThirdPartyA(
                    input=Input(jurisdiction_code='de', company_number='3333')
                )
            response = self._open_file(RAW_3333)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_3333))
            self.assertEqual(b.response_object.company_number, '3333')

        with self.subTest("DE: 4444"):
            b = third_party_a.ThirdPartyA(
                    input=Input(jurisdiction_code='de', company_number='4444')
                )
            response = self._open_file(RAW_4444)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_4444))
            self.assertEqual(b.response_object.company_number, '4444')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThirdPartyA)
    unittest.TextTestRunner(verbosity=2).run(suite)