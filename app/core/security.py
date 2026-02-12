import hashlib
import os
import hmac

PBKDF2_ITERATIONS = 100_000

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PBKDF2_ITERATIONS
    )
    return salt.hex() + ":" + pwd_hash.hex()


def verify_password(password: str, stored: str) -> bool:
    salt_hex, hash_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PBKDF2_ITERATIONS
    )

    return hmac.compare_digest(pwd_hash.hex(), hash_hex)
