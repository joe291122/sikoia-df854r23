import json
import unittest
from app import main
from app.models.input import Input
from app.models.response import Company
from app.models import third_party_a
from app.models import third_party_b
from app.models.response import Company
from app.configs.third_party_a import ThirdPartyA
from app.configs.third_party_b import ThirdPartyB
from pydantic.error_wrappers import ValidationError
from pydantic import BaseModel


RAW_1111 = 'tests/data/raw_third_party_a_uk_1111.json'
RAW_5555 = 'tests/data/raw_third_party_b_nl_5555.json'
RAW_A_3333 = 'tests/data/raw_third_party_a_de_3333.json'
RAW_B_3333 = 'tests/data/raw_third_party_b_de_3333.json'
RESULT_1111 = 'tests/data/main/expected_results/uk_1111.json'
RESULT_2222 = 'tests/data/main/expected_results/uk_2222.json'
RESULT_5555 = 'tests/data/main/expected_results/nl_5555.json'
MERGED_3333 = 'tests/data/main/expected_results/de_3333.json'
MERGED_4444 = 'tests/data/main/expected_results/de_4444.json'

class TestMain(unittest.TestCase):

    def _open_file(self, file):

        with open(file) as f:
            return json.loads(f.read())

    def test_validate_input(self):

        with self.subTest("Lowercase uk"):
            result = main.validate_input(
                jurisdiction_code='uk',
                company_number='1111'
            )
            self.assertEqual(result.jurisdiction_code, 'uk')

        with self.subTest("Uppercase uk"):
            result = main.validate_input(
                jurisdiction_code='UK',
                company_number='1111'
            )
            self.assertEqual(result.jurisdiction_code, 'uk')

        with self.subTest("Not in our list"):
            with self.assertRaises(ValidationError):
                result = main.validate_input(
                    jurisdiction_code='ZE',
                    company_number='3333'
                )

    def test_get_api_list(self):

        with self.subTest("uk"):
            input = Input(
                jurisdiction_code='uk',
                company_number = '1111'
            )
            result = main.get_api_list(input=input)
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], ThirdPartyA)

        with self.subTest("de"):
            input = Input(
                jurisdiction_code='de',
                company_number = '3333'
            )
            result = main.get_api_list(input=input)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], ThirdPartyA)
            self.assertIsInstance(result[1], ThirdPartyB)

        with self.subTest("nl"):
            input = Input(
                jurisdiction_code='nl',
                company_number = '5555'
            )
            result = main.get_api_list(input=input)
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], ThirdPartyB)

    def get_from_cache(self):
        self.assertIsNone(main.get_from_cache())

    def test_call_api(self):
        input = Input(
                jurisdiction_code='uk',
                company_number='1111'
            )
        api_a = ThirdPartyA(input=input)
        result = main.call_api(api_a)
        expected_result = self._open_file(RAW_1111)
        self.assertEqual(result, expected_result)

    def test_call_third_party(self):
        with self.subTest("No cache value"):
            input = Input(
                    jurisdiction_code='uk',
                    company_number='1111'
                )
            api_a = ThirdPartyA(input=input)
            main.call_third_party(api_a)
            result_file = 'tests/data/parsed_third_party_a_uk_1111.json'
            expected_result = self._open_file(result_file)
            self.assertEqual(api_a.response_object, expected_result)

    def test_merge_two_dicts(self):

        with self.subTest('merge dict into an emtpy dict'):
            a = {}
            b = {'a':1}
            expected_result = {'a':1}
            main.merge_two_dicts(a,b)
            self.assertEqual(a, b)

        with self.subTest('merge two dicts'):
            a = {'a':1, 'b':2}
            b = {'b':3, 'c':3}
            main.merge_two_dicts(a,b)
            expected_result = {'a':1, 'b':3, 'c':3}
            self.assertEqual(a, expected_result)

        with self.subTest('merge None into data dicts'):
            a = {'a':1, 'b':2}
            b = {'b': None, 'c':3}
            main.merge_two_dicts(a,b)
            expected_result = {'a':1, 'b':2, 'c':3}
            self.assertEqual(a, expected_result)

        with self.subTest('merge three dicts'):
            a = {'a':1, 'b':2}
            b = {'b':3, 'c':3}
            main.merge_two_dicts(a,b)
            c = {'c':4, 'd':4}
            main.merge_two_dicts(a,c)
            expected_result = {'a':1, 'b':3, 'c':4, 'd':4}
            self.assertEqual(a, expected_result)

    def test_filter_empty_data(self):

        with self.subTest("not None values"):
            a = {'a': 1, 'b': 'b', 'c': True}
            result = main.filter_empty_data(a)
            self.assertEqual(result, a)

        with self.subTest("None values"):
            a = {'a': 1, 'b': 'b', 'c': True, 'd': None}
            expected_result = {'a': 1, 'b': 'b', 'c': True}
            result = main.filter_empty_data(a)
            self.assertEqual(result, expected_result)

        with self.subTest("Nested"):
            a = {'a': 1, 'b': 'b', 'c': True, 'd': {'d1': {'d2': 2}}}
            result = main.filter_empty_data(a)
            self.assertEqual(result, a)

        with self.subTest("Nested with None"):
            a = {'a': 1, 'b': 'b', 'c': True, 'd': {'d1': {'d2': 2, 'd2_none': None}, 'd1_none': None}}
            expected_result = {'a': 1, 'b': 'b', 'c': True, 'd': {'d1': {'d2': 2}}}
            result = main.filter_empty_data(a)
            self.assertEqual(result, expected_result)

        with self.subTest("List values"):
            a = {'a': 1, 'b': 'b', 'c': True, 'd': [1,2,3], 'e': [{'e1_none': None, 'e2': 'a'}]}
            expected_result = {'a': 1, 'b': 'b', 'c': True, 'd': [1,2,3], 'e': [{'e2': 'a'}]}
            result = main.filter_empty_data(a)
            self.assertEqual(result, expected_result)

    def test_create_response(self):

        with self.subTest('No output'):
            input = {'a': 1}
            result = main.create_response(
                api_list=[], 
                input=input
            )
            self.assertEqual(result, input)

        with self.subTest('badly formatted result'):

            input = Input(
                jurisdiction_code='uk',
                company_number='1111'
            )
            class DummyModel(BaseModel):
                a: int
            api_a = ThirdPartyA(input=input)
            api_a.response_object = DummyModel(a=1)
            api_list = [api_a]
            
            with self.assertRaises(ValidationError):
                result = main.create_response(
                    api_list=api_list, 
                    input=input
                )

        with self.subTest('1 resultset (API A)'):

            input = Input(
                jurisdiction_code='uk',
                company_number='1111'
            )
            api_a = ThirdPartyA(input=input)
            api_a.response_object = third_party_a.Company(**self._open_file(RAW_1111))
            api_list = [api_a]
            result = main.create_response(
                api_list=api_list, 
                input=input
            )
            expected_result = Company(**self._open_file(RESULT_1111))
            self.assertEqual(result, expected_result)

        with self.subTest('1 resultset (API B)'):

            input = Input(
                jurisdiction_code='nl',
                company_number='5555'
            )
            api_b = ThirdPartyB(input=input)
            api_b.response_object = third_party_b.Company(**self._open_file(RAW_5555))
            api_list = [api_b]
            result = main.create_response(
                api_list=api_list, 
                input=input
            )
            expected_result = Company(**self._open_file(RESULT_5555))
            self.assertEqual(result, expected_result)

        with self.subTest('2 resultsets (API A & B)'):

            input = Input(
                jurisdiction_code='de',
                company_number='3333'
            )
            api_a = ThirdPartyA(input=input)
            api_a.response_object = third_party_a.Company(**self._open_file(RAW_A_3333))
            api_b = ThirdPartyB(input=input)
            api_b.response_object = third_party_b.Company(**self._open_file(RAW_B_3333))
            api_list = [api_a, api_b]
            result = main.create_response(
                api_list=api_list, 
                input=input
            )
            expected_result = Company(**self._open_file(MERGED_3333))
            self.assertEqual(result, expected_result)


    def test_process_request(self):

        with self.subTest("uk: 1111"):
            result = main.process_request(
                jurisdiction_code='uk',
                company_number='1111'
            )
            expected_result = self._open_file(RESULT_1111)
            self.assertEqual(result, Company(**expected_result))

        with self.subTest("uk: 2222"):
            result = main.process_request(
                jurisdiction_code='uk',
                company_number='2222'
            )
            expected_result = self._open_file(RESULT_2222)
            self.assertEqual(result, Company(**expected_result))

        with self.subTest("DE: 3333"):
            result = main.process_request(
                jurisdiction_code='de',
                company_number='3333'
            )
            expected_result = self._open_file(MERGED_3333)
            self.assertEqual(result, Company(**expected_result))

        with self.subTest("DE: 4444"):
            result = main.process_request(
                jurisdiction_code='de',
                company_number='4444'
            )
            expected_result = self._open_file(MERGED_4444)
            self.assertEqual(result, Company(**expected_result))

        with self.subTest("nl: 5555"):
            result = main.process_request(
                jurisdiction_code='nl',
                company_number='5555'
            )
            expected_result = self._open_file(RESULT_5555)
            self.assertEqual(result, Company(**expected_result))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2).run(suite)