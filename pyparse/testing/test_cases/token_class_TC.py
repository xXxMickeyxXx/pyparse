import importlib
from unittest import TestCase, skip, skipIf, skipUnless

from unittest_utils import register_test


_pyparse_core = importlib.import_module(".core", package="pyparse")


# print(f"CHECKING PACKAGE DIR")
# for i in dir(_pyparse_core):
# 	print(i)
# print()


@register_test("token_class_TC")
class TokenClassTestCase(TestCase):

	def setUp(self):
		self._token_name_1 = "TEST_TOKEN"
		self._token_val_1 = "TOKEN VALUE"
		self._token_1 = _pyparse_core.Token(self._token_name_1, value=self._token_val_1)
		
		self._token_name_2 = "TEST_TOKEN"
		self._token_val_2 = "TOKEN VALUE"
		self._token_2 = _pyparse_core.Token(self._token_name_2, value=self._token_val_2)

	def test_token_equality(self):
		self.assertTrue(self._token_1 == self._token_2)

	def tearDown(self):
		pass


if __name__ == "__main__":
	pass
