import httpx


BASE_URL_API_IFOOD = "https://merchant-api.ifood.com.br"


def criar_client_ifood() -> httpx.Client:
    client = httpx.Client(base_url=BASE_URL_API_IFOOD)
    return client


def login(client_id: str, client_secret: str) -> None:
    data = {
        "grantType": "client_credentials",
        "clientId": client_id,
        "clientSecret": client_secret,
        "authorizationCode": "",
        "authorizationCodeVerifier": "",
        "refreshToken": "",
    }
