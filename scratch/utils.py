from io import BytesIO

import shutil as shell_utils


class SystemIO:

    # @NOTE<WARNING: NOT THREAD-SAFE>

    # __DESCRIPTOR_ID = 0

    # @classmethod
    # def __new__(cls, *args, **kwargs):
    #     _descriptor_id = cls.__DESCRIPTOR_ID
    #     _new_cls = super().__new__(*args, descriptor_id=_descriptor_id, **kwargs)
    #     cls.__DESCRIPTOR_ID += 1

    def __init__(self, init_bytes=b""):
        self._bytes_io = BytesIO()
        self._descriptor_id = descriptor_id
        self._std_input = sys.stdin
        self._std_output = sys.stdout

    @property
    def descriptor_id(self):
        return self._descriptor_id

    @property
    def STD_INPUT(self):
        return self._std_input

    @property
    def STD_OUTPUT(self):
        return self._std_output


def center_text(text):
    terminal_width, _ = shell_utils.get_terminal_size()
    padding = (terminal_width - len(text)) // 2
    centered_text = f"\x1B[{padding}C{text}"
    return centered_text


def apply_color(color_index, text):
    return f"\033[38;5;{color_index}m{text}\033[0m"


def underline_text(text):
    return f"\x1B[4m{text}\x1B[0m"


def bold_text(text):
    return f"\x1B[1m{text}\x1B[0m"


def is_UTF_8(string):
    try:
        return True if hasattr(string, "decode") and (isinstance(string, bytes) or string.decode("UTF-8")) else False
    except UnicodeDecodeError:
        return False


def _convert_to_bytes(string, encoding="UTF-8"):
    print(f"STRING IN '_convert_to_bytes' function ---> {string}")
    return string.encoding(encoding) if not (isinstance(string, bytes) and hasattr(string, "encoding")) else (string.decode(encoding) if hasattr(string, "decode") else string)


def _convert_to_str(string, encoding="UTF-8"):
    return string.decode(encoding) if hasattr(string, "decode") else string


def chunkify(string_data, chunk_size=1024):
    total_size = len(string_data)
    _encoded_response = string_data
    if not isinstance(string_data, bytes):    # Determine a better check for this  
        _encoded_response = _convert_to_bytes(string_data, encoding="UTF-8")

    for i in range(0, total_size, chunk_size):
        yield _encoded_response[i:i+chunk_size]


def display_ANSI_colors():
    for i in range(257):
        print(f"{i} ---> {apply_color(i, 'COLOR')}")


def display_result(input, parser_result, passing_msg=None):
    if parser_result:
        _color = 10
        _text = underline_text(bold_text(apply_color(_color, f"INPUT IS VALID")))
        _text += f"\n    |"
        _text += f"\n    |"
        _text += f"\n    • ----> {bold_text(apply_color(11, input))}\n\n{bold_text(passing_msg)}\n" if isinstance(passing_msg, str) else f"\n    • ----> {bold_text(apply_color(11, input))}\n"
        _border_text = f"-" * int(len(_text)/2)
        _result = bold_text(apply_color(_color, _text))
    else:
        _color = 9
        _text = underline_text(bold_text(apply_color(_color, f"INPUT IS INVALID")))
        _text += f"\n    |"
        _text += f"\n    |"
        _text += f"\n    • ----> {bold_text(apply_color(11, input))}\n\n{bold_text(passing_msg)}\n" if isinstance(passing_msg, str) else f"\n    • ----> {bold_text(apply_color(11, input))}\n"
        _border_text = f"-" * int(len(_text)/2)
        _result = _text
    print(apply_color(10, _border_text))
    print(_result)
    print(apply_color(10, _border_text))
    print()


def display_item_states(item_sets):
    print()
    for item_state, _items in item_sets.items():
        print(f"STATE: {item_state}")
        for _item in _items:
            print(f"\t{_item.rule_head} ---> {_item.status()}")
        print()
    print()


if __name__ == "__main__":
    display_ANSI_colors()
