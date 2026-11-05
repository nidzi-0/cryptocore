import shutil
import subprocess

from Crypto.Cipher import AES

from cryptocore.modes.gcm import GCM


KEY = bytes.fromhex(
    "00112233445566778899aabbccddeeff"
)

NONCE = bytes.fromhex(
    "aabbccddeeff001122334455"
)

AAD = bytes.fromhex(
    "112233445566778899aabbcc"
)

PLAINTEXT = (
    b"CryptoCore AES-GCM "
    b"interoperability test."
)


def check_openssl_cli():
    openssl = shutil.which(
        "openssl"
    )

    if openssl is None:
        print(
            "OpenSSL CLI: SKIPPED "
            "(openssl not found)"
        )

        return

    result = subprocess.run(
        [
            openssl,
            "enc",
            "-aes-128-gcm",
            "-help",
        ],
        capture_output=True,
        text=True,
    )

    output = (
        result.stdout
        + result.stderr
    ).lower()

    if (
        result.returncode != 0
        or "unknown cipher" in output
        or "unsupported" in output
    ):
        print(
            "OpenSSL enc AES-GCM: "
            "SKIPPED "
            "(AEAD is not supported "
            "by openssl enc)"
        )

        return

    print(
        "OpenSSL enc AES-GCM: available"
    )


def main():
    print(
        "AES-GCM interoperability test"
    )

    check_openssl_cli()

    reference = AES.new(
        KEY,
        AES.MODE_GCM,
        nonce=NONCE,
        mac_len=16,
    )

    reference.update(
        AAD
    )

    (
        reference_ciphertext,
        reference_tag,
    ) = reference.encrypt_and_digest(
        PLAINTEXT
    )

    cryptocore = GCM(
        KEY,
        NONCE,
    )

    ciphertext, tag = (
        cryptocore.encrypt(
            PLAINTEXT,
            AAD,
        )
    )

    assert (
        ciphertext
        == reference_ciphertext
    )

    assert (
        tag
        == reference_tag
    )

    reference_decryptor = AES.new(
        KEY,
        AES.MODE_GCM,
        nonce=NONCE,
        mac_len=16,
    )

    reference_decryptor.update(
        AAD
    )

    restored_reference = (
        reference_decryptor
        .decrypt_and_verify(
            ciphertext,
            tag,
        )
    )

    assert (
        restored_reference
        == PLAINTEXT
    )

    restored_cryptocore = (
        cryptocore.decrypt(
            reference_ciphertext,
            reference_tag,
            AAD,
        )
    )

    assert (
        restored_cryptocore
        == PLAINTEXT
    )

    print(
        "CryptoCore -> reference: PASSED"
    )

    print(
        "Reference -> CryptoCore: PASSED"
    )

    print(
        "AES-GCM interoperability: PASSED"
    )


if __name__ == "__main__":
    main()