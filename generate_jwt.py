import os
from jwt import JWT, jwk_from_pem
import time
import logging


def get_private_key_from_pem(pem: str) -> str | None:
    """Load a private key from a `.pem` file.

    Args:
        pem (str): The path to the `.pem` file.

    Returns:
        str: The private key.
    """
    try:
        with open(pem, "r") as pem_file:
            return pem_file.read()
    except FileNotFoundError:
        logging.error(f"Could not locate PEM file {pem}")
        return None


def get_private_key_from_env(env_key: str) -> str | None:
    """Load a private key from the environment.

    Args:
        env_key (str): The key for the variable with the private key.

    Returns:
        str: The private key.
    """
    return os.getenv(env_key)


def generate_jwt(key: str, client_id: str) -> str:
    """Generate a JWT using your private key to verify Github API requests.

    To learn how to generate a private key, see https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps#generating-private-keys.

    Args:
        key (str): The private key.
        client_id (str): The client ID.

    Returns:
        str: The JWT.
    """
    signing_key = jwk_from_pem(bytes(key))

    now = int(time.time())
    payload = {
        # Issued at time
        'iat': now,
        # JWT expiration time (10 minutes maximum)
        'exp': now + 600,
        # GitHub App's client ID
        'iss': client_id
    }

    # Create JWT
    jwt_instance = JWT()
    return jwt_instance.encode(payload, signing_key, alg='RS256')