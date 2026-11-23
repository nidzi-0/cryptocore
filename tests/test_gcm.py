import pytest

from cryptocore.modes.gcm import (
    AuthenticationError,
    GCM,
    TAG_SIZE,
    _build_gf_multiplication_table,
    gf_multiply,
    gf_multiply_precomputed,
)


KEY = bytes.fromhex(
    "FEFFE9928665731C"
    "6D6A8F9467308308"
)

NONCE = bytes.fromhex(
    "CAFEBABEFACEDBADDECAF888"
)


def test_gf_multiply_zero():
    value = int(
        "B83B533708BF535D"
        "0AA6E52980D53B78",
        16,
    )

    assert (
        gf_multiply(
            0,
            value,
        )
        == 0
    )


@pytest.mark.parametrize(
    "x,y",
    [
        (
            0x00000000000000000000000000000000,
            0x00000000000000000000000000000000,
        ),
        (
            0x00000000000000000000000000000001,
            0x00000000000000000000000000000001,
        ),
        (
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
        ),
        (
            0x0388DACE60B6A392F328C2B971B2FE78,
            0x66E94BD4EF8A2C3B884CFA59CA342B2E,
        ),
        (
            0x42831EC2217774244B7221B784D0D49C,
            0xB83B533708BF535D0AA6E52980D53B78,
        ),
    ],
)
def test_precomputed_gf_matches_reference(
    x,
    y,
):

    reference = gf_multiply(
        x,
        y,
    )

    optimized = (
        gf_multiply_precomputed(
            x,
            y,
        )
    )

    assert optimized == reference


def test_gf_table_is_cached():

    multiplier = int(
        "B83B533708BF535D"
        "0AA6E52980D53B78",
        16,
    )

    first = (
        _build_gf_multiplication_table(
            multiplier
        )
    )

    second = (
        _build_gf_multiplication_table(
            multiplier
        )
    )

    assert first is second


def test_nist_gcm_example_1():


    gcm = GCM(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        gcm.encrypt(
            b"",
            b"",
        )
    )

    assert ciphertext == b""

    assert tag.hex().upper() == (
        "3247184B"
        "3C4F69A4"
        "4DBCD228"
        "87BBB418"
    )

    assert len(tag) == TAG_SIZE


def test_nist_gcm_example_4():

    aad = bytes.fromhex(
        "3AD77BB40D7A3660"
        "A89ECAF32466EF97"
        "F5D3D58503B9699D"
        "E785895A96FDBAAF"
        "43B1CD7F598ECE23"
        "881B00E3ED030688"
        "7B0C785E27E8AD3F"
        "8223207104725DD4"
    )

    plaintext = bytes.fromhex(
        "D9313225F88406E5"
        "A55909C5AFF5269A"
        "86A7A9531534F7DA"
        "2E4C303D8A318A72"
        "1C3C0C9595680953"
        "2FCF0E2449A6B525"
        "B16AEDF5AA0DE657"
        "BA637B391AAFD255"
    )

    expected_ciphertext = (
        "42831EC221777424"
        "4B7221B784D0D49C"
        "E3AA212F2C02A4E0"
        "35C17E2329ACA12E"
        "21D514B25466931C"
        "7D8F6A5AAC84AA05"
        "1BA30B396A0AAC97"
        "3D58E091473F5985"
    )

    expected_tag = (
        "64C0232904AF398A"
        "5B67C10B53A5024D"
    )

    gcm = GCM(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        gcm.encrypt(
            plaintext,
            aad,
        )
    )

    assert (
        ciphertext.hex().upper()
        == expected_ciphertext
    )

    assert (
        tag.hex().upper()
        == expected_tag
    )


def test_nist_gcm_example_4_decryption():
    aad = bytes.fromhex(
        "3AD77BB40D7A3660"
        "A89ECAF32466EF97"
        "F5D3D58503B9699D"
        "E785895A96FDBAAF"
        "43B1CD7F598ECE23"
        "881B00E3ED030688"
        "7B0C785E27E8AD3F"
        "8223207104725DD4"
    )

    expected_plaintext = bytes.fromhex(
        "D9313225F88406E5"
        "A55909C5AFF5269A"
        "86A7A9531534F7DA"
        "2E4C303D8A318A72"
        "1C3C0C9595680953"
        "2FCF0E2449A6B525"
        "B16AEDF5AA0DE657"
        "BA637B391AAFD255"
    )

    ciphertext = bytes.fromhex(
        "42831EC221777424"
        "4B7221B784D0D49C"
        "E3AA212F2C02A4E0"
        "35C17E2329ACA12E"
        "21D514B25466931C"
        "7D8F6A5AAC84AA05"
        "1BA30B396A0AAC97"
        "3D58E091473F5985"
    )

    tag = bytes.fromhex(
        "64C0232904AF398A"
        "5B67C10B53A5024D"
    )

    gcm = GCM(
        KEY,
        NONCE,
    )

    plaintext = gcm.decrypt(
        ciphertext,
        tag,
        aad,
    )

    assert (
        plaintext
        == expected_plaintext
    )


def test_wrong_tag_rejected():
    plaintext = (
        b"CryptoCore Sprint 6"
    )

    aad = (
        b"authenticated metadata"
    )

    gcm = GCM(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        gcm.encrypt(
            plaintext,
            aad,
        )
    )

    wrong_tag = bytearray(
        tag
    )

    wrong_tag[0] ^= 0x01

    with pytest.raises(
        AuthenticationError,
        match="Authentication failed",
    ):
        gcm.decrypt(
            ciphertext,
            bytes(wrong_tag),
            aad,
        )


def test_wrong_aad_rejected():
    plaintext = (
        b"Secret authenticated data"
    )

    gcm = GCM(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        gcm.encrypt(
            plaintext,
            b"correct aad",
        )
    )

    with pytest.raises(
        AuthenticationError,
        match="Authentication failed",
    ):
        gcm.decrypt(
            ciphertext,
            tag,
            b"wrong aad",
        )


def test_non_96_bit_nonce_round_trip():
    nonce = bytes.fromhex(
        "CAFEBABEFACEDBAD"
    )

    plaintext = (
        b"GCM must support "
        b"non-96-bit nonce lengths."
    )

    aad = (
        b"associated data"
    )

    gcm = GCM(
        KEY,
        nonce,
    )

    ciphertext, tag = (
        gcm.encrypt(
            plaintext,
            aad,
        )
    )

    restored = gcm.decrypt(
        ciphertext,
        tag,
        aad,
    )

    assert restored == plaintext


def test_tag_is_16_bytes():
    gcm = GCM(
        KEY,
        NONCE,
    )

    _, tag = gcm.encrypt(
        b"message",
        b"aad",
    )

    assert len(tag) == 16