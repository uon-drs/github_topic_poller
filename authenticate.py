import requests


def get_access_token(installation_id: int, jwt: str) -> str | None:
    """Get the access token for the app installation with the given ID.

    Args:
        installation_id (int): The ID of the app installation to authenticate.
        jwt (str): The JWT for the app.

    Returns:
        str | None: The access token for the app installation.
    """
    res = requests.post(
        url=f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {jwt}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    return res.json().get("token")
