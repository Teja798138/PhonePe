import logging
import pytest
import requests
from Utilities.utils import device_id
from conftest import  get_userid_url, token_generate
import random
from datetime import datetime, timedelta
import time


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.crm
def test_crm_non_push(call_crm_base_url, token_generate, get_userid_url):
    url = get_userid_url
    userid_header = {
        "Authorization": token_generate
    }
    try:
        send_request = requests.get(url, headers=userid_header)
        response = send_request.json()
        capture_userid = response.get("userId")
    except Exception as e:
        logger.info("API request failed", e)
    custom_header_crm = {
        "Authorization": token_generate,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json",
        "Content-Type": "application/json",
        "host": "zencast.nixy.stg-drove.phonepe.nb6"
    }
    random_integer = random.randint(15, 90)
    random_message = random.randint(10, 80)
    random_grouping = random.randint(18, 98)
    fetch_device_id = device_id()
    random_request_id = f"test-apr-14-1st{random_integer}"
    random_message_id = f"test-apr-14-1st{random_message}"
    random_grouping_id = f"test-apr-14-1st{random_grouping}"
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_ago_epoch = int(time.mktime(one_day_ago.timetuple()) * 1000)
    current_epoch_milliseconds = int((datetime.now() + timedelta(minutes=5)).timestamp() * 1000)
    crm_non_push_payload = {
        "requestId": random_request_id,
        "userId": capture_userid,
        "deviceId": fetch_device_id,
        "profileId": "CONSUMER_PROMOTIONAL",
        "appMessage": {
            "version": 2,
            "messageId": random_message_id,
            "groupingKey": random_grouping_id,
            "source": {
                "type": "PHONEPE"
            },
            "data": {
                "syncSections": [
                    {
                        "type": "all"
                    }
                ],
                "placements": [
                    {
                        "scope": "DRAWER",
                        "template": {
                            "templateId": "TITLE_MESSAGE_IMAGE",
                            "templateParams": {
                                "value": {
                                    "title": "Teja-auto-14-1st",
                                    "message": "Teja-auto-14-1st"
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "action_nav": "prepaidMobile",
                                    "redirection_data": {
                                        "type": "STATIC",
                                        "content": "{\"data\":[]}"
                                    }
                                }
                            }
                        },
                        "deferment": {
                            "type": "NONE",
                            "minutes": 1
                        }
                    }
                ],
                "campaignId": "testcampaign1",
                "communicationIntent": "PROMOTIONAL",
                "utm_source": "Push",
                "utm_medium": "Hawkeye",
                "utm_campaign": "testcampaign"
            },
            "properties": {
                "editable": True,
                "deletable": True,
                "override": True,
                "unsubscriptionSupported": False
            },
            "sentAt": one_day_ago_epoch,
            "expiresAt": current_epoch_milliseconds
        }
    }
    send_request = requests.post('http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast',
                                 headers=custom_header_crm, json=crm_non_push_payload)
    print(crm_non_push_payload)
    response = send_request.json()
    print(response)
    request_id = crm_non_push_payload.get("requestId")
    grouping_key = crm_non_push_payload.get("appMessage", {}).get("groupingKey")
    sent_at = crm_non_push_payload.get("appMessage", {}).get("sentAt")
    expires_at = crm_non_push_payload.get("appMessage", {}).get("expiresAt")
    response_message_id = response.get("data", {}).get("messageId")
    capture_deviceid = device_id()

    time.sleep(20)
    payload = {
        "requestId": request_id,
        "entityId": capture_userid,
        "deviceId": capture_deviceid,
        "profileId": "CONSUMER_PROMOTIONAL",
        "appMessage": {
            "version": 2,
            "messageId": response_message_id,
            "groupingKey": grouping_key,
            "source": {
                "type": "PHONEPE"
            },
            "data": {
                "syncSections": [
                    {
                        "type": "crm_kill_switch",
                        "params": {
                            "createdAt": sent_at,
                            "killSwitch": {
                                "mode": "PERPETUAL",
                                "killSwitchScope": {
                                    "campaignId": "karthik-test-campa631",
                                    "scope": "CAMPAIGN"
                                }
                            }
                        }
                    }
                ],
                "placements": [],
                "campaignId": "testcampaign1",
                "communicationIntent": "PROMOTIONAL",
                "utm_source": "Push",
                "utm_medium": "Hawkeye",
                "utm_campaign": "testcampaign"
            },
            "properties": {
                "editable": True,
                "deletable": True,
                "override": True,
                "unsubscriptionSupported": False
            },
            "sentAt": sent_at,
            "expiresAt": expires_at
        }
    }
    try:
        send_kill_request = requests.post(
            'http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast', headers=custom_header_crm,
            json=payload)
        response = send_kill_request.json()
        print(response)
    except Exception as e:
        logger.info("API request is failed", e)
        raise
    logger.info("Received Response", response)
