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


if __name__ == "__main__":
    pass
