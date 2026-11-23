from cryptocore.mac.hmac import HMACSHA256


HMAC_OUTPUT_SIZE = 32
MAX_COUNTER = (1 << 32) - 1


def _hmac_sha256(
    key: bytes,
    message: bytes,
) -> bytes:
    hmac = HMACSHA256(
        key
    )

    hmac.update(
        message
    )

    return hmac.digest()


def derive_key(
    master_key: bytes,
    context: str,
    length: int = 32,
) -> bytes:


    if not isinstance(
        master_key,
        bytes,
    ):
        raise TypeError(
            "Master key должен быть bytes."
        )

    if not isinstance(
        context,
        str,
    ):
        raise TypeError(
            "Context должен быть строкой."
        )

    if not context:
        raise ValueError(
            "Context не может быть пустым."
        )

    if not isinstance(
        length,
        int,
    ):
        raise TypeError(
            "Длина ключа должна быть "
            "целым числом."
        )

    if length <= 0:
        raise ValueError(
            "Длина ключа должна быть "
            "больше нуля."
        )

    context_bytes = context.encode(
        "utf-8"
    )

    blocks_needed = (
        length
        + HMAC_OUTPUT_SIZE
        - 1
    ) // HMAC_OUTPUT_SIZE

    if blocks_needed > MAX_COUNTER:
        raise ValueError(
            "Запрошенная длина ключа "
            "слишком велика."
        )

    derived = bytearray()

    counter = 1

    while len(
        derived
    ) < length:

        counter_bytes = (
            counter.to_bytes(
                4,
                byteorder="big",
            )
        )

        block = _hmac_sha256(
            master_key,
            context_bytes
            + counter_bytes,
        )

        derived.extend(
            block
        )

        counter += 1

    return bytes(
        derived[:length]
    )