import hmac
import hashlib

import pytest

from cryptocore.mac.hmac import (
    HMACSHA256,
)


def test_rfc4231_case_1():
    key = bytes.fromhex(
        "0b" * 20
    )

    data = b"Hi There"

    expected = (
        "b0344c61d8db38535ca8afceaf0bf12b"
        "881dc200c9833da726e9376c2e32cff7"
    )

    result = HMACSHA256(
        key
    ).compute(data)

    assert result == expected


def test_rfc4231_case_2():
    key = b"Jefe"

    data = (
        b"what do ya want "
        b"for nothing?"
    )

    expected = (
        "5bdcc146bf60754e6a042426089575c75"
        "a003f089d2739839dec58b964ec3843"
    )

    result = HMACSHA256(
        key
    ).compute(data)

    assert result == expected


def test_rfc4231_case_3():
    key = bytes.fromhex(
        "aa" * 20
    )

    data = bytes.fromhex(
        "dd" * 50
    )

    expected = (
        "773ea91e36800e46854db8ebd09181a7"
        "2959098b3ef8c122d9635514ced565fe"
    )

    result = HMACSHA256(
        key
    ).compute(data)

    assert result == expected


def test_rfc4231_case_4():
    key = bytes.fromhex(
        "0102030405060708090a0b0c0d0e0f"
        "10111213141516171819"
    )

    data = bytes.fromhex(
        "cd" * 50
    )

    expected = (
        "82558a389a443c0ea4cc819899f2083a"
        "85f0faa3e578f8077a2e3ff46729665b"
    )

    result = HMACSHA256(
        key
    ).compute(data)

    assert result == expected


@pytest.mark.parametrize(
    "key",
    [
        bytes(range(16)),
        bytes(range(64)),
        bytes(
            index % 256
            for index in range(100)
        ),
    ],
)
def test_different_key_sizes(
    key,
):
    data = (
        b"CryptoCore Sprint 5"
    )

    result = HMACSHA256(
        key
    ).compute(data)

    expected = hmac.new(
        key,
        data,
        hashlib.sha256,
    ).hexdigest()

    assert result == expected


def test_empty_message():
    key = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )

    result = HMACSHA256(
        key
    ).compute(b"")

    expected = hmac.new(
        key,
        b"",
        hashlib.sha256,
    ).hexdigest()

    assert result == expected


def test_incremental_update():
    key = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )

    mac = HMACSHA256(
        key
    )

    mac.update(
        b"Crypto"
    )

    mac.update(
        b"Core"
    )

    mac.update(
        b" Sprint 5"
    )

    data = (
        b"CryptoCore Sprint 5"
    )

    expected = hmac.new(
        key,
        data,
        hashlib.sha256,
    ).hexdigest()

    assert mac.hexdigest() == expected


def test_hexdigest_is_repeatable():
    key = b"test-key"

    mac = HMACSHA256(
        key
    )

    mac.update(
        b"message"
    )

    first = mac.hexdigest()
    second = mac.hexdigest()

    assert first == second


def test_rejects_non_bytes_key():
    with pytest.raises(TypeError):
        HMACSHA256(
            "not bytes"
        )


def test_rejects_non_bytes_message():
    mac = HMACSHA256(
        b"key"
    )

    with pytest.raises(TypeError):
        mac.update(
            "message"
        )
def test_hmac_stream_uses_chunks():
    import hashlib
    import hmac

    from cryptocore.digest import (
        CHUNK_SIZE,
        hmac_stream,
    )

    key = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )

    class ControlledStream:
        def __init__(self):
            self.remaining = (
                CHUNK_SIZE * 5 + 123
            )

            self.read_sizes = []

        def read(self, size):
            self.read_sizes.append(
                size
            )

            if self.remaining == 0:
                return b""

            amount = min(
                size,
                self.remaining,
            )

            self.remaining -= amount

            return b"A" * amount

    stream = ControlledStream()

    result = hmac_stream(
        stream,
        key,
    )

    data = (
        b"A"
        * (
            CHUNK_SIZE * 5
            + 123
        )
    )

    expected = hmac.new(
        key,
        data,
        hashlib.sha256,
    ).hexdigest()

    assert result == expected

    assert all(
        size == CHUNK_SIZE
        for size in stream.read_sizes
    )