import json
import httpx
import time
import unittest
from app.configs import third_party_a
from app.models.input import Input
from app.models.third_party_a import Company


TEST_CASES = [
    {
        'jurisdiction_code': 'uk',
        'company_number': '1111'
    },
    {
        'jurisdiction_code': 'uk',
        'company_number': '2222'
    },
    {
        'jurisdiction_code': 'de',
        'company_number': '3333'
    },
    {
        'jurisdiction_code': 'de',
        'company_number': '4444'
    },
    {
        'jurisdiction_code': 'nl',
        'company_number': '5555'
    },
    {
        'jurisdiction_code': 'nl',
        'company_number': '6666'
    },
]


class TestIntegration(unittest.TestCase):

    def _open_file(self, file):

        with open(file) as f:
            return json.loads(f.read())

    def call_api(self, endpoint):
        response = httpx.get(endpoint)
        print(response)
        return json.loads(response.text)

    def test_all_cases(self):
        for i in TEST_CASES:
            start_time = time.time()
            result = self.call_api(f"http://app:8000/v1/company/{i['jurisdiction_code']}/{i['company_number']}")
            print("--- %s seconds ---" % round(time.time() - start_time, 2))
            expected_result = self._open_file(f"tests/integration_tests/expected_results/{i['jurisdiction_code']}_{i['company_number']}.json")
            print(i)
            print("-----Result------")
            print(result)
            print("-----Expected Result------")
            print(expected_result)
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegration)
    unittest.TextTestRunner(verbosity=2).run(suite)