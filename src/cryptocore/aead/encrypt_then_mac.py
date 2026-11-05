from secrets import compare_digest

from cryptocore.csprng import generate_random_bytes
from cryptocore.mac.hmac import HMACSHA256
from cryptocore.modes.ctr import (
    decrypt_ctr,
    encrypt_ctr,
)


IV_SIZE = 16
TAG_SIZE = 32

ENC_KEY_LABEL = (
    b"CryptoCore-ETM-encryption-key"
)

MAC_KEY_LABEL = (
    b"CryptoCore-ETM-mac-key"
)


class EncryptThenMACAuthenticationError(
    ValueError
):
    """Ошибка аутентификации Encrypt-then-MAC."""


def _to_bytes(
    value,
    name: str,
) -> bytes:
    if not isinstance(
        value,
        (
            bytes,
            bytearray,
            memoryview,
        ),
    ):
        raise TypeError(
            f"{name} должен быть "
            "байтовой строкой."
        )

    return bytes(value)


def derive_keys(
    master_key: bytes,
) -> tuple[bytes, bytes]:
    """
    Разделяет master key на:

    K_e — AES-128 encryption key;
    K_m — HMAC-SHA256 key.

    Используется domain-separated
    HMAC-SHA256.
    """

    master_key = _to_bytes(
        master_key,
        "Master key",
    )

    if not master_key:
        raise ValueError(
            "Master key не может быть пустым."
        )

    encryption_deriver = HMACSHA256(
        master_key
    )

    encryption_deriver.update(
        ENC_KEY_LABEL
    )

    encryption_material = (
        encryption_deriver.digest()
    )

    mac_deriver = HMACSHA256(
        master_key
    )

    mac_deriver.update(
        MAC_KEY_LABEL
    )

    mac_key = (
        mac_deriver.digest()
    )

    # AES-128 использует 16 байт.
    encryption_key = (
        encryption_material[:16]
    )

    return (
        encryption_key,
        mac_key,
    )


def compute_tag(
    mac_key: bytes,
    authenticated_ciphertext: bytes,
    aad: bytes,
) -> bytes:
    mac = HMACSHA256(
        mac_key
    )

    # По требованиям Sprint 6:
    #
    # T = MAC(K_m, C || AAD)
    mac.update(
        authenticated_ciphertext
    )

    mac.update(
        aad
    )

    return mac.digest()


def encrypt_then_mac(
    plaintext: bytes,
    master_key: bytes,
    aad: bytes = b"",
) -> bytes:
    """
    Encrypt-then-MAC:

    C = IV || AES-CTR(K_e, P)

    T = HMAC-SHA256(
        K_m,
        C || AAD
    )

    Output:
        IV || ciphertext || tag
    """

    plaintext = _to_bytes(
        plaintext,
        "Plaintext",
    )

    aad = _to_bytes(
        aad,
        "AAD",
    )

    encryption_key, mac_key = (
        derive_keys(
            master_key
        )
    )

    iv = generate_random_bytes(
        IV_SIZE
    )

    ciphertext = encrypt_ctr(
        data=plaintext,
        key=encryption_key,
        iv=iv,
    )

    authenticated_ciphertext = (
        iv
        + ciphertext
    )

    tag = compute_tag(
        mac_key,
        authenticated_ciphertext,
        aad,
    )

    return (
        authenticated_ciphertext
        + tag
    )


def decrypt_then_verify(
    data: bytes,
    master_key: bytes,
    aad: bytes = b"",
) -> bytes:
    """
    Сначала проверяет MAC.

    Только после успешной проверки
    выполняет AES-CTR decryption.
    """

    data = _to_bytes(
        data,
        "Encrypted data",
    )

    aad = _to_bytes(
        aad,
        "AAD",
    )

    minimum_size = (
        IV_SIZE
        + TAG_SIZE
    )

    if len(data) < minimum_size:
        raise EncryptThenMACAuthenticationError(
            "Authentication failed: "
            "encrypted data is too short."
        )

    encryption_key, mac_key = (
        derive_keys(
            master_key
        )
    )

    authenticated_ciphertext = (
        data[:-TAG_SIZE]
    )

    supplied_tag = (
        data[-TAG_SIZE:]
    )

    expected_tag = compute_tag(
        mac_key,
        authenticated_ciphertext,
        aad,
    )

    # КРИТИЧЕСКИ ВАЖНО:
    # plaintext ещё не вычисляется.
    if not compare_digest(
        supplied_tag,
        expected_tag,
    ):
        raise EncryptThenMACAuthenticationError(
            "Authentication failed: "
            "AAD mismatch or "
            "ciphertext/tag tampered."
        )

    iv = (
        authenticated_ciphertext[
            :IV_SIZE
        ]
    )

    ciphertext = (
        authenticated_ciphertext[
            IV_SIZE:
        ]
    )

    return decrypt_ctr(
        data=ciphertext,
        key=encryption_key,
        iv=iv,
    )