import pytest
from pathlib import Path
import json
import requests

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "endpoints.json"


def get_base_endpoint():
    try:
        with CONFIG_PATH.open() as json_file:
            properties = json.load(json_file)
            env = properties["mock_environment"]["mock_env"]
            return properties[env]["base_url"]
    except(FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load the base endpoint: {e}")


@pytest.fixture(scope="session", autouse=True)
def mock_base_url():
    return get_base_endpoint()


def get_crm_base_endpoint():
    try:
        with CONFIG_PATH.open() as json_file:
            properties = json.load(json_file)
            env = properties["crm_stage_endpoint"]["crm_base_url"]
            return env
    except(FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load the base endpoint: {e}")


@pytest.fixture(scope="session", autouse=True)
def call_crm_base_url():
    return get_crm_base_endpoint()


@pytest.fixture(scope="session")
def token_generate():
    url = "https://olympus-im-stage.phonepe.com/olympus/im/v1/auth/login"
    olympus_payload = {
        "type": "PASSWORD",
        "username": "voduri.quali.con@phonepe.com",
        "password": "Tejamech1@",
        "ttlInfo": {
            "ttlSeconds": 86400,
            "jwtTtlSeconds": 86400
        }
    }
    olympus_header = {
        "X-CLIENT-ID": "olympusim",
        "Content-Type": "application/json"
    }
    send_request = requests.post(url, headers=olympus_header, json=olympus_payload)
    response = send_request.json()
    capture_token = response.get("token")
    bearer_token = f"O-Bearer {capture_token}"
    return bearer_token


@pytest.fixture(scope="function")
def get_userid_url():
    return "http://userservice.nixy.stg-drove.phonepe.nb6/v1/lookups/phone/8459495500"
