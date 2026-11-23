from cryptocore.mac.hmac import (
    HMACSHA256,
)


SHA256_DIGEST_SIZE = 32
MAX_BLOCK_INDEX = (1 << 32) - 1


def pbkdf2_hmac_sha256(
    password: bytes | str,
    salt: bytes,
    iterations: int = 100_000,
    dklen: int = 32,
) -> bytes:
    if isinstance(
        password,
        str,
    ):
        password = password.encode(
            "utf-8"
        )

    if not isinstance(
        password,
        bytes,
    ):
        raise TypeError(
            "Password должен быть "
            "строкой или bytes."
        )

    if not isinstance(
        salt,
        bytes,
    ):
        raise TypeError(
            "Salt должен быть bytes."
        )

    if not isinstance(
        iterations,
        int,
    ):
        raise TypeError(
            "Количество итераций "
            "должно быть целым числом."
        )

    if iterations <= 0:
        raise ValueError(
            "Количество итераций "
            "должно быть больше нуля."
        )

    if not isinstance(
        dklen,
        int,
    ):
        raise TypeError(
            "Длина ключа должна быть "
            "целым числом."
        )

    if dklen <= 0:
        raise ValueError(
            "Длина ключа должна быть "
            "больше нуля."
        )

    blocks_needed = (
        dklen
        + SHA256_DIGEST_SIZE
        - 1
    ) // SHA256_DIGEST_SIZE

    if blocks_needed > MAX_BLOCK_INDEX:
        raise ValueError(
            "Запрошенная длина ключа "
            "слишком велика."
        )

    prf = HMACSHA256(
        password
    )

    derived_key = bytearray()

    for block_index in range(
        1,
        blocks_needed + 1,
    ):

        u = prf.digest_message(
            salt
            + block_index.to_bytes(
                4,
                byteorder="big",
            )
        )

        block_value = int.from_bytes(
            u,
            byteorder="big",
        )

        for _ in range(
            2,
            iterations + 1,
        ):
            u = prf.digest_message(
                u
            )

            block_value ^= (
                int.from_bytes(
                    u,
                    byteorder="big",
                )
            )

        block = block_value.to_bytes(
            SHA256_DIGEST_SIZE,
            byteorder="big",
        )

        derived_key.extend(
            block
        )

    return bytes(
        derived_key[:dklen]
    )