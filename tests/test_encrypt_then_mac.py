import pytest

import cryptocore.aead.encrypt_then_mac as etm

from cryptocore.aead.encrypt_then_mac import (
    EncryptThenMACAuthenticationError,
    IV_SIZE,
    TAG_SIZE,
    decrypt_then_verify,
    derive_keys,
    encrypt_then_mac,
)


MASTER_KEY = bytes.fromhex(
    "00112233445566778899aabbccddeeff"
    "102132435465768798a9babbdcddedef"
)


def test_key_separation():
    encryption_key, mac_key = (
        derive_keys(
            MASTER_KEY
        )
    )

    assert len(
        encryption_key
    ) == 16

    assert len(
        mac_key
    ) == 32

    assert (
        encryption_key
        != mac_key[:16]
    )


def test_key_derivation_is_deterministic():
    first = derive_keys(
        MASTER_KEY
    )

    second = derive_keys(
        MASTER_KEY
    )

    assert first == second


def test_encrypt_then_mac_round_trip():
    plaintext = (
        b"CryptoCore Sprint 6 "
        b"Encrypt-then-MAC test."
        b"\x00\x01\xff"
    )

    aad = (
        b"authenticated metadata"
    )

    encrypted = encrypt_then_mac(
        plaintext,
        MASTER_KEY,
        aad,
    )

    restored = decrypt_then_verify(
        encrypted,
        MASTER_KEY,
        aad,
    )

    assert restored == plaintext

    assert len(
        encrypted
    ) == (
        IV_SIZE
        + len(plaintext)
        + TAG_SIZE
    )


def test_wrong_aad_rejected():
    plaintext = (
        b"Secret message"
    )

    encrypted = encrypt_then_mac(
        plaintext,
        MASTER_KEY,
        b"correct aad",
    )

    with pytest.raises(
        EncryptThenMACAuthenticationError,
        match="Authentication failed",
    ):
        decrypt_then_verify(
            encrypted,
            MASTER_KEY,
            b"wrong aad",
        )


def test_ciphertext_tamper_rejected():
    plaintext = (
        b"Authenticated secret"
    )

    aad = (
        b"metadata"
    )

    encrypted = bytearray(
        encrypt_then_mac(
            plaintext,
            MASTER_KEY,
            aad,
        )
    )

    # Меняем первый байт ciphertext,
    # сразу после 16-байтового IV.
    encrypted[IV_SIZE] ^= 0x01

    with pytest.raises(
        EncryptThenMACAuthenticationError,
        match="Authentication failed",
    ):
        decrypt_then_verify(
            bytes(encrypted),
            MASTER_KEY,
            aad,
        )


def test_iv_tamper_rejected():
    encrypted = bytearray(
        encrypt_then_mac(
            b"message",
            MASTER_KEY,
            b"aad",
        )
    )

    encrypted[0] ^= 0x01

    with pytest.raises(
        EncryptThenMACAuthenticationError,
        match="Authentication failed",
    ):
        decrypt_then_verify(
            bytes(encrypted),
            MASTER_KEY,
            b"aad",
        )


def test_tag_tamper_rejected():
    encrypted = bytearray(
        encrypt_then_mac(
            b"message",
            MASTER_KEY,
            b"aad",
        )
    )

    encrypted[-1] ^= 0x01

    with pytest.raises(
        EncryptThenMACAuthenticationError,
        match="Authentication failed",
    ):
        decrypt_then_verify(
            bytes(encrypted),
            MASTER_KEY,
            b"aad",
        )


def test_wrong_master_key_rejected():
    encrypted = encrypt_then_mac(
        b"message",
        MASTER_KEY,
        b"aad",
    )

    wrong_key = bytes.fromhex(
        "ffeeddccbbaa99887766554433221100"
        "00112233445566778899aabbccddeeff"
    )

    with pytest.raises(
        EncryptThenMACAuthenticationError,
        match="Authentication failed",
    ):
        decrypt_then_verify(
            encrypted,
            wrong_key,
            b"aad",
        )


def test_empty_aad_supported():
    plaintext = (
        b"Empty AAD test"
    )

    encrypted = encrypt_then_mac(
        plaintext,
        MASTER_KEY,
    )

    restored = decrypt_then_verify(
        encrypted,
        MASTER_KEY,
    )

    assert restored == plaintext


def test_random_iv_per_encryption():
    first = encrypt_then_mac(
        b"same plaintext",
        MASTER_KEY,
        b"same aad",
    )

    second = encrypt_then_mac(
        b"same plaintext",
        MASTER_KEY,
        b"same aad",
    )

    first_iv = (
        first[:IV_SIZE]
    )

    second_iv = (
        second[:IV_SIZE]
    )

    assert (
        first_iv
        != second_iv
    )


def test_decryption_not_called_before_authentication(
    monkeypatch,
):
    encrypted = bytearray(
        encrypt_then_mac(
            b"very secret plaintext",
            MASTER_KEY,
            b"aad",
        )
    )

    # Повреждаем tag.
    encrypted[-1] ^= 0x01

    decrypt_called = False

    def forbidden_decrypt(
        *args,
        **kwargs,
    ):
        nonlocal decrypt_called

        decrypt_called = True

        raise AssertionError(
            "decrypt_ctr не должен "
            "вызываться до успешной "
            "аутентификации."
        )

    monkeypatch.setattr(
        etm,
        "decrypt_ctr",
        forbidden_decrypt,
    )

    with pytest.raises(
        EncryptThenMACAuthenticationError
    ):
        decrypt_then_verify(
            bytes(encrypted),
            MASTER_KEY,
            b"aad",
        )

    assert decrypt_called is False