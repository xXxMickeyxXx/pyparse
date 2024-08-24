from pathlib import Path


THIS_MODULE = Path(__file__)
PYPARSE_ROOT = THIS_MODULE.parent.parent
FILES_ROOT = PYPARSE_ROOT / "files"
SCRATCH_ROOT = PYPARSE_ROOT / Path("scratch")

LOGGING_ROOT = FILES_ROOT / Path("logging")


TEST_INPUT_1 = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_06_13.txt"
TEST_INPUT_2 = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_07_16.txt"


if __name__ == "__main__":
    print(f"FILES ROOT ---> {FILES_ROOT}")
