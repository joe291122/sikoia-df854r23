import unittest
from app.models import input
from pydantic.error_wrappers import ValidationError


class TestInput(unittest.TestCase):

    def test_jurisdiction_code(self):

        with self.subTest("Lowercase uk"):
            result = input.Input(
                jurisdiction_code='uk',
                company_number='1111'
            )
            self.assertEqual(result.jurisdiction_code, 'uk')
            self.assertEqual(result.company_number, '1111')

        with self.subTest("Uppercase uk"):
            result = input.Input(
                jurisdiction_code='UK',
                company_number='1111'
            )
            self.assertEqual(result.jurisdiction_code, 'uk')

        with self.subTest("Not in our list"):
            with self.assertRaises(ValidationError):
                result = input.Input(
                    jurisdiction_code='ZE',
                    company_number='3333'
                )

    def test_company_number(self):

        with self.subTest("correct company_number and jurisdiction_code - uk"):
            result = input.Input(
                jurisdiction_code='uk',
                company_number='1111'
            )
            self.assertEqual(result.jurisdiction_code, 'uk')
            self.assertEqual(result.company_number, '1111')

        with self.subTest("correct company_number and jurisdiction_code - de"):
            result = input.Input(
                jurisdiction_code='de',
                company_number='3333'
            )
            self.assertEqual(result.jurisdiction_code, 'de')
            self.assertEqual(result.company_number, '3333')

        with self.subTest("company_number not in our list"):
            with self.assertRaises(ValidationError):
                result = input.Input(
                    jurisdiction_code='ZE',
                    company_number='0000'
                )

        with self.subTest("company_number in our list, but wrong jurisdiction"):
            with self.assertRaises(ValidationError):
                result = input.Input(
                    jurisdiction_code='ZE',
                    company_number='3333'
                )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInput)
    unittest.TextTestRunner(verbosity=2).run(suite)