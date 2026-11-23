import pytest

from cryptocore.kdf.pbkdf2 import (
    pbkdf2_hmac_sha256,
)


@pytest.mark.parametrize(
    (
        "password",
        "salt",
        "iterations",
        "dklen",
        "expected",
    ),
    [
        (
            b"password",
            b"salt",
            1,
            32,
            (
                "120fb6cffcf8b32c"
                "43e7225256c4f837"
                "a86548c92ccc3548"
                "0805987cb70be17b"
            ),
        ),
        (
            b"password",
            b"salt",
            2,
            32,
            (
                "ae4d0c95af6b46d3"
                "2d0adff928f06dd0"
                "2a303f8ef3c251df"
                "d6e2d85a95474c43"
            ),
        ),
        (
            b"password",
            b"salt",
            4096,
            32,
            (
                "c5e478d59288c841"
                "aa530db6845c4c8d"
                "962893a001ce4e11"
                "a4963873aa98134a"
            ),
        ),
    ],
)
def test_pbkdf2_known_answers(
    password,
    salt,
    iterations,
    dklen,
    expected,
):
    result = pbkdf2_hmac_sha256(
        password=password,
        salt=salt,
        iterations=iterations,
        dklen=dklen,
    )

    assert result.hex() == expected


def test_pbkdf2_is_deterministic():
    first = pbkdf2_hmac_sha256(
        password=b"my-password",
        salt=b"my-salt",
        iterations=1000,
        dklen=32,
    )

    second = pbkdf2_hmac_sha256(
        password=b"my-password",
        salt=b"my-salt",
        iterations=1000,
        dklen=32,
    )

    assert first == second


@pytest.mark.parametrize(
    "length",
    [
        1,
        16,
        31,
        32,
        33,
        64,
        100,
    ],
)
def test_pbkdf2_output_length(
    length,
):
    result = pbkdf2_hmac_sha256(
        password=b"password",
        salt=b"salt",
        iterations=10,
        dklen=length,
    )

    assert len(result) == length


def test_pbkdf2_accepts_string_password():
    result_from_string = (
        pbkdf2_hmac_sha256(
            password="password",
            salt=b"salt",
            iterations=10,
            dklen=32,
        )
    )

    result_from_bytes = (
        pbkdf2_hmac_sha256(
            password=b"password",
            salt=b"salt",
            iterations=10,
            dklen=32,
        )
    )

    assert (
        result_from_string
        == result_from_bytes
    )


def test_different_salts_produce_different_keys():
    first = pbkdf2_hmac_sha256(
        password=b"password",
        salt=b"salt-one",
        iterations=100,
        dklen=32,
    )

    second = pbkdf2_hmac_sha256(
        password=b"password",
        salt=b"salt-two",
        iterations=100,
        dklen=32,
    )

    assert first != second


def test_different_passwords_produce_different_keys():
    first = pbkdf2_hmac_sha256(
        password=b"password-one",
        salt=b"salt",
        iterations=100,
        dklen=32,
    )

    second = pbkdf2_hmac_sha256(
        password=b"password-two",
        salt=b"salt",
        iterations=100,
        dklen=32,
    )

    assert first != second


def test_iterations_must_be_positive():
    with pytest.raises(
        ValueError,
        match="итераций",
    ):
        pbkdf2_hmac_sha256(
            password=b"password",
            salt=b"salt",
            iterations=0,
            dklen=32,
        )


def test_length_must_be_positive():
    with pytest.raises(
        ValueError,
        match="Длина ключа",
    ):
        pbkdf2_hmac_sha256(
            password=b"password",
            salt=b"salt",
            iterations=1,
            dklen=0,
        )