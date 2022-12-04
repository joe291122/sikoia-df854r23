import json
import unittest
from datetime import date
from app.configs import third_party_b
from app.models.input import Input
from app.models.third_party_b import Company


RAW_3333 = 'tests/data/raw_third_party_b_de_3333.json'
RAW_4444 = 'tests/data/raw_third_party_b_de_4444.json'
RAW_5555 = 'tests/data/raw_third_party_b_nl_5555.json'
RESULT_3333 = 'tests/data/parsed_third_party_b_de_3333.json'
RESULT_4444 = 'tests/data/parsed_third_party_b_de_4444.json'
RESULT_5555 = 'tests/data/parsed_third_party_b_nl_5555.json'


class TestThirdPartyB(unittest.TestCase):

    def _open_file(self, file):

        with open(file) as f:
            return json.loads(f.read())

    def test_class_variables(self):
        self.assertEqual(third_party_b.ThirdPartyB.URL,  "https://interview-df854r23.sikoia.com")
        self.assertListEqual(third_party_b.ThirdPartyB.SUPPORTED_JURISDICTIONS, [
            'de',
            'nl'
        ])
        self.assertEqual(third_party_b.ThirdPartyB.RESPONSE_MODEL,  Company)

    def test_endpoint(self):
        b = third_party_b.ThirdPartyB(
            input=Input(jurisdiction_code='nl', company_number='5555')
        )
        self.assertEqual(b.endpoint, "https://interview-df854r23.sikoia.com/v1/company-data?jurisdictionCode=nl&companyNumber=5555")

    def test_parse_repsonse(self):

        with self.subTest("NL: 5555"):
            b = third_party_b.ThirdPartyB(
                    input=Input(jurisdiction_code='nl', company_number='5555')
                )
            response = self._open_file(RAW_5555)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_5555))
            self.assertEqual(b.response_object.company_number, '5555')
            self.assertEqual(b.response_object.company_name, 'How I Met Your Mother N.V.')
            self.assertEqual(b.response_object.jurisdiction_code, 'nl')
            self.assertIsNone(b.response_object.date_established)
            self.assertIsNone(b.response_object.date_dissolved)
            self.assertEqual(b.response_object.activities[0].activity_code, 12)
            self.assertEqual(b.response_object.owners[0].ownership_type, "Shareholder")
            self.assertEqual(b.response_object.officers[0].date_from.year, 1974)
            self.assertEqual(b.response_object.officers[0].date_from.month, 8)
            self.assertEqual(b.response_object.officers[0].date_from.day, 11)
            self.assertEqual(b.response_object.official_address.street, 'Eerste van Swindenstraat 40')
            self.assertEqual(b.response_object.official_address.city, 'Amsterdam')
            self.assertEqual(b.response_object.official_address.country, 'Netherlands')
            self.assertEqual(b.response_object.official_address.postcode, '1093 GE')
            self.assertEqual(len(b.response_object.officers), 2)
            self.assertEqual(len(b.response_object.owners), 2)

        with self.subTest("DE: 3333"):
            b = third_party_b.ThirdPartyB(
                input=Input(jurisdiction_code='de', company_number='3333')
            )
            response = self._open_file(RAW_3333)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_3333))
            self.assertEqual(b.response_object.company_number, '3333')

        with self.subTest("DE: 4444"):
            b = third_party_b.ThirdPartyB(
                input=Input(jurisdiction_code='de', company_number='4444')
            )
            response = self._open_file(RAW_4444)
            b.parse_response(response=response)
            self.assertIsInstance(b.response_object, Company)
            self.assertEqual(b.response_object.dict(), self._open_file(RESULT_4444))
            self.assertEqual(b.response_object.company_number, '4444')

        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThirdPartyB)
    unittest.TextTestRunner(verbosity=2).run(suite)