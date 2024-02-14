from pathlib import Path
from setuptools import setup, find_packages


def default_requirement_filepath(requirement_filename="requirements.txt"):
    _current_path = Path(__file__).resolve()
    return _current_path.parent / Path(requirement_filename)


def setup_main(requirement_filepath=None, requirement_filename="requirements.txt"):
    if requirement_filepath is None:
        _requirement_filepath = default_requirement_filepath(
            requirement_filename=requirement_filename
        )
    else:
        _requirement_filepath = requirement_filepath

    requirements_txt = None
    with open(_requirement_filepath, "r") as in_file:
        requirements_txt = in_file.readlines()

    if requirements_txt is None:
        _error_details = f"unable to parse application's 'requirements.txt' file..."
        raise RuntimeError(_error_details)

    setup(
        name="pyparse",
        version="0.0.1",
        url="",
        description="",
        packages=find_packages(),
        install_requires=requirements_txt,
    )


if __name__ == "__main__":
    setup_main()
