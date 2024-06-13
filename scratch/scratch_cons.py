from enum import StrEnum, auto


class FileDescriptorMode(StrEnum):

    # Reading related modes
    READ = "r"  # NOTE: file must exist
    READ_BIN = "rb"  # NOTE: file must exist
    READ_WRITE = "r+"  # NOTE: file must exist
    READ_WRITE_BIN = "rb+"  # NOTE: file must exist

    # Writing related modes
    WRITE = "w"  # NOTE: create new file if not exists or truncate existing one
    WRITE_BIN = "wb"  # NOTE: create new file if not exists or truncate existing one
    WRITE_READ = "w+"  # NOTE: create new file if not exists or truncate existing one
    WRITE_READ_BIN = "wb+"  # NOTE: create new file if not exists or truncate existing one

    # TODO: implement remaining file descriptor modes
    # Appending related modes


if __name__ == "__main__":
    pass
