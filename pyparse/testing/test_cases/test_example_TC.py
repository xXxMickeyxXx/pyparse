from unittest import TestCase, skip, skipIf, skipUnless

from unittest_utils import DIRS_REGISTRY, TESTCASE_REGISTRY, register_test


# NOTE: Below is an example that allows you to import using the dot notation
# 		path name (much like you would in an actual import), using a string,
# 		and starting with the root of package/application/etc
# 			(must import it like: "import MODULE_OR_PACKAGE_NAME" and not like:
# 			"from "MODULE_OR_PACKAGE_NAME import SOMETHING")
#
# 			----------> importlib.import_module("DOT_NOTATION_PATH_STARTING_WITH_ROOT_DIR")
# 			----------> NOTE: import the "importlib" ('import importlib') library in order
# 							  to use this feature


@register_test("test_TEST_CASE")
class TestCaseTestingTest(TestCase):

    def test_a_thing_that_should_pass(self):
        a = True
        self.assertTrue(a)

    def test_another_thing_that_should_pass(self):
        b = True
        self.assertTrue(b)

    def test_yet_another_thing_that_should_pass(self):
        c = True
        self.assertTrue(c)

    def test_one_more_thing_that_should_fail(self):
        _msg = f"THIS MESSAGE BEING VISIBLE INDICATES THAT MY EXAMPLE TEST IS WORKING, AS INTENDED"
        with self.subTest(_msg):
            d = False
            self.assertTrue(d)


if __name__ == "__main__":
    pass
