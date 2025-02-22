# @DOC<'ToDoLang' aims to take advantage of python's comment and docstring
# syntax/semantics to embed a project's remaining TODO's, and the
# organization thereof, into a document for arbitrary analysis, be
# it for planning or tracking, among other things.>
#
# @NOTE<Similar to the roles of linters and formatters, project source
# code becomes the input to the 'ToDoLang' runtime, resulting in the
# generation of a '.todo' document. This document can then go on to
# be analyzed manually or programatically, as a data structure
# that can be referenced within the python runtime environment
# itself. Given that ability, arbitrary logic can be executed
# within the host's runtime>

# @NOTE<This module represents the type of input expected when parsing
# and running application logic associated with the 'ToDoLang'
# mini-language.>
<                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               []

def print_result(result, msg=""):
    print()
    if msg:
        print(f"{msg}{result}")
        print()
        return
    print(result)
    print()


def test_add_func(num_1, num_2) -> int:
    """
    @TODO<This is the syntax for a 'TODO' data structure in the 'ToDoLang' language>
    @NOTE<This is the syntax for a 'NOTE' data structure in the 'ToDoLang' language>
    @TODO<Implement addition logic >
    """


def main():
    _number_1, _number_2 = 10, 13
    _result = test_add_func(_number_1, _number_2)
    _msg = f"{_number_1} + {_number_2} = "
    print_result(_result, msg=_msg)


if __name__ == "__main__":
    main()
