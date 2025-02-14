import httpx

from utils.env import get_env_var

_WCOMMANDA_ZONE_ID = get_env_var("WCOMMANDA_ZONE_ID")
_WCOMMANDA_IP_ADDRESS = get_env_var("WCOMMANDA_SERVER_IP_ADDRESS")

_CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"
_CLOUDFLARE_API_TOKEN = f"Bearer {get_env_var('CLOUDFLARE_API_TOKEN')}"
_CLOUDFLARE_API_HEADERS = {
    "Authorization": _CLOUDFLARE_API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

cloudlfare_client = httpx.Client(
    base_url=_CLOUDFLARE_API_URL,
    headers=_CLOUDFLARE_API_HEADERS,
)


def get_dns_records(zone_id: str):
    url = f"zones/{zone_id}/dns_records"
    response = cloudlfare_client.get(url)
    return response.json()


def criar_subdominio(subdomain: str):
    url = f"zones/{_WCOMMANDA_ZONE_ID}/dns_records"
    data = {
        "type": "A",
        "name": subdomain,
        "content": _WCOMMANDA_IP_ADDRESS,
        "ttl": 1,
        "proxied": True,
    }
    response = cloudlfare_client.post(url, json=data)
    return response.json()


def get_dns_record_details(zone_id: str, record_id: str):
    url = f"zones/{zone_id}/dns_records/{record_id}"
    response = cloudlfare_client.get(url)
    return response.json()
