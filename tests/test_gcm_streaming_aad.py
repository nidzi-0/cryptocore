from io import BytesIO

import pytest

import cryptocore.aead.gcm_stream as stream_module

from cryptocore.aead.gcm_stream import (
    GCMStreamingAAD,
    ghash_aad_stream,
)
from cryptocore.modes.gcm import (
    AuthenticationError,
    GCM,
)


KEY = bytes.fromhex(
    "feffe9928665731c"
    "6d6a8f9467308308"
)

NONCE = bytes.fromhex(
    "cafebabefacedbaddecaf888"
)


def test_streaming_aad_matches_regular_gcm():
    plaintext = (
        b"CryptoCore streaming AAD "
        b"compatibility test."
    )

    aad = (
        b"associated-data-" * 37
        + b"end"
    )

    regular = GCM(
        KEY,
        NONCE,
    )

    expected_ciphertext, expected_tag = (
        regular.encrypt(
            plaintext,
            aad,
        )
    )

    streaming = GCMStreamingAAD(
        KEY,
        NONCE,
    )

    ciphertext, tag = streaming.encrypt(
        plaintext,
        BytesIO(aad),
        chunk_size=7,
    )

    assert (
        ciphertext
        == expected_ciphertext
    )

    assert tag == expected_tag


def test_streaming_aad_round_trip():
    plaintext = (
        b"Secret message with "
        b"streaming AAD."
    )

    aad = b"A" * 10003

    encryptor = GCMStreamingAAD(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        encryptor.encrypt(
            plaintext,
            BytesIO(aad),
            chunk_size=127,
        )
    )

    decryptor = GCMStreamingAAD(
        KEY,
        NONCE,
    )

    restored = decryptor.decrypt(
        ciphertext,
        tag,
        BytesIO(aad),
        chunk_size=333,
    )

    assert restored == plaintext


def test_streaming_wrong_aad_rejected():
    plaintext = (
        b"Authenticated plaintext"
    )

    correct_aad = (
        b"correct streaming aad"
    )

    wrong_aad = (
        b"wrong streaming aad"
    )

    gcm = GCMStreamingAAD(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        gcm.encrypt(
            plaintext,
            BytesIO(
                correct_aad
            ),
        )
    )

    with pytest.raises(
        AuthenticationError,
        match="Authentication failed",
    ):
        gcm.decrypt(
            ciphertext,
            tag,
            BytesIO(
                wrong_aad
            ),
        )


def test_aad_stream_is_read_in_chunks():
    class TrackingStream:
        def __init__(
            self,
            data: bytes,
        ):
            self._stream = BytesIO(
                data
            )

            self.maximum_read = 0

        def read(
            self,
            size: int,
        ):
            self.maximum_read = max(
                self.maximum_read,
                size,
            )

            return self._stream.read(
                size
            )

    aad = b"B" * (
        1024 * 1024
        + 123
    )

    stream = TrackingStream(
        aad
    )

    gcm = GCMStreamingAAD(
        KEY,
        NONCE,
    )

    gcm.encrypt(
        b"message",
        stream,
        chunk_size=4096,
    )

    assert (
        stream.maximum_read
        <= 4096
    )


def test_virtual_aad_over_20_gib_is_streamed(
    monkeypatch,
):
    logical_size = (
        20 * 1024**3
        + 123
    )

    chunk_size = (
        16 * 1024**2
    )

    class VirtualHugeAAD:
        def __init__(self):
            self.remaining = (
                logical_size
            )

            self.maximum_read = 0
            self.total_returned = 0

            self.block = (
                b"A" * chunk_size
            )

        def read(
            self,
            size: int,
        ) -> bytes:
            self.maximum_read = max(
                self.maximum_read,
                size,
            )

            if self.remaining == 0:
                return b""

            amount = min(
                size,
                self.remaining,
            )

            self.remaining -= amount
            self.total_returned += amount

            return self.block[
                :amount
            ]

    processed = {
        "bytes": 0,
    }

    def fake_process_full_blocks(
        state,
        hash_subkey,
        data,
    ):
        processed["bytes"] += len(
            data
        )

        return state

    monkeypatch.setattr(
        stream_module,
        "_process_full_blocks",
        fake_process_full_blocks,
    )

    stream = VirtualHugeAAD()

    result = ghash_aad_stream(
        b"\x01" * 16,
        stream,
        b"",
        chunk_size=chunk_size,
    )

    assert len(result) == 16

    assert (
        stream.total_returned
        == logical_size
    )

    assert stream.remaining == 0

    assert (
        stream.maximum_read
        <= chunk_size
    )

    assert (
        logical_size
        > stream.maximum_read
        * 1000
    )