import ulid


def generate_public_id() -> str:
    return str(ulid.new())
