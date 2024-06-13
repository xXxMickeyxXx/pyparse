from .scratch_init_grammar import grammar_factory, init_grammar


        #####################################################################################################################
        #                                                                                                                   #
        # • -------------------------------------------------- TESTING -------------------------------------------------- • #
        #                                                                                                                   #
        #####################################################################################################################


def generate_lr_items(grammar):
    raise NotImplementedError("Logic for generating item sets/states for the LR(0) automaton not yet implemented")


def read_source(filepath):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    _file_data = ""
    with open(filepath, "r") as in_file:
        _file_data = in_file.read()

    if not bool(_file_data):
        # TODO: create and raise custom error here
        _error_details = f"Error Reading File Contents -- unable to read data contained within file @ path ---> {filepath}"
        raise RuntimeError
    return _file_data


def tokenize(source):
    raise NotImplementedError


def _parse_helper(source):
    raise NotImplementedError


def parse(filepath):
    _source_data = read_source(filepath)


def parse_main():
    


if __name__ == "__main__":
    pass
