from unittest_utils import (
    UnittestRunner,
    TESTCASE_REGISTRY,
    DIRS_REGISTRY
)
from .testing_cons import (
    TESTING_ROOT,
    TEST_CASES_ROOT
)


def runner_factory(runner_id=None, test_registry=TESTCASE_REGISTRY, dirs_registry=DIRS_REGISTRY):
    dirs_registry.register("test_cases_root", TEST_CASES_ROOT)
    test_runner = UnittestRunner(runner_id=runner_id, test_registry=test_registry, dirs_registry=dirs_registry)
    test_runner.load_runner()
    return test_runner


def run_tests():
    test_runner = runner_factory(runner_id="test_runner")
    test_runner.run()


def main():
    print()
    run_tests()
    print()


if __name__ == "__main__":
    pass
