"""Contains various constants and other static values which are used
to fascilitate the operations carried out by the 'unittest_utils'
package (the main executioner of this application)
"""

from pathlib import Path


TESTING_ROOT = Path(__file__).parent
TEST_CASES_ROOT = TESTING_ROOT / Path("test_cases")


if __name__ == "__main__":
    pass
