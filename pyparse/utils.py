import shutil as shell_utils
from uuid import uuid1


def generate_id(*, prefix=None, suffix=None, uuid_factory=uuid1, uuid_type=None):
    uuid_obj = uuid_factory()

    if uuid_type is None:
        uuid_obj = str(uuid_obj)
        if prefix is not None:
            uuid_obj = str(prefix) + uuid_obj
        if suffix is not None:
            uuid_obj = uuid_obj + str(suffix)
    else:
        uuid_obj = uuid_type(uuid_obj)

    return uuid_obj


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


if __name__ == "__main__":
    display_ANSI_colors()
