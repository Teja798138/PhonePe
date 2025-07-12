import time
import logging
import pytest
import requests
from conftest import  get_userid_url, token_generate
import random
from datetime import datetime, timedelta
from Utilities.utils import device_id

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.crm
def test_crm_inbox(call_crm_base_url, token_generate, get_userid_url):
    url = get_userid_url
    userid_header = {
        "Authorization": token_generate
    }
    try:
        send_request_userid = requests.get(url, headers=userid_header)
        response_userid = send_request_userid.json()
        capture_userid = response_userid.get("userId")
    except Exception as e:
        logger.info("API request failed", e)
        raise
    logger.info("received Response", response_userid)
    fetch_device_id = device_id()
    random_integer = random.randint(120, 9000)
    random_message_id = random.randint(105, 945)
    random_group_id = random.randint(143, 865)
    req_id = f"reqShru{random_integer}"
    mess_id = f"msgShru{random_message_id}"
    group_id = f"msgShru{random_group_id}"
    current_epoch_milliseconds = int((datetime.now() + timedelta(minutes=5)).timestamp() * 1000)
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_ago_epoch = int(time.mktime(one_day_ago.timetuple()) * 1000)
    custom_header_crm = {
        "Authorization": token_generate,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json",
        "Content-Type": "application/json",
        "host": "zencast.nixy.stg-drove.phonepe.nb6"
    }
    crm_inbox_payload = {
        "requestId": req_id,
        "profileId": "CONSUMER_TRANSACTIONAL",
        "enableRetry": False,
        "entityId": capture_userid,
        "deviceId": fetch_device_id,
        "customTags": {
            "tag1": "karthik-test-campa631",
            "tag2": "1",
            "tag3": capture_userid,
            "tag4": "HE@CM22041319515587550137252@1@d675e16c-8285-455a-8649-1046d3098c50",
            "tag5": ""
        },
        "appMessage": {
            "messageId": mess_id,
            "groupingKey": group_id,
            "source": {
                "type": "PHONEPE"
            },
            "data": {
                "placements": [
                    {
                        "scope": "INBOX",
                        "expiresAt": one_day_ago_epoch,
                        "template": {
                            "templateId": "ICON_TITLE_SUBTITLE",
                            "templateParams": {
                                "value": {
                                    "title": "myinboxstagetest",
                                    "subTitle": "Click here",
                                    "iconURL": "https:October was a memorable month for us. We hit the 250 million user mark in India."
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "deepLinkIOS": "phonepestage://dg?providerId=SAFEGOLD"
                                }
                            }
                        },
                        "deferment": {
                            "type": "NONE",
                            "minutes": 1,
                            "future": current_epoch_milliseconds,
                            "retryWindowInSec": 0
                        }
                    },
                    {
                        "scope": "DRAWER",
                        "expiresAt": current_epoch_milliseconds,
                        "template": {
                            "templateId": "TITLE_MESSAGE_IMAGE",
                            "templateParams": {
                                "value": {
                                    "title": "Shrudrawernotif",
                                    "message": "Click here",
                                    "image": "https://hexcode.in/wp-content/uploads/phonepe-refer-earn-offer.jpg"
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "deepLinkIOS": "phonepestage://dg?providerId=SAFEGOLD"
                                }
                            }
                        },
                        "deferment": {
                            "type": "NONE",
                            "minutes": 1,
                            "future": current_epoch_milliseconds,
                            "retryWindowInSec": 0
                        }
                    }
                ],
                "campaignId": "karthik-test-campa631",
                "communicationIntent": "TRANSACTIONAL",
                "syncSections": [
                    {
                        "type": "all",
                        "params": {
                            "testKey1": "testValue1",
                            "testKey2": "testValue2"
                        }
                    }
                ],
                "utm_source": "Push",
                "utm_medium": "Hawkeye",
                "utm_campaign": "HAWKEYE@OWRkYmRmMmNiYzdhZThiMWZmYjNkNmNjMDg3Y2Q1MTA3OTNlNjczOTM3MzdjMGQ2MGJlYjM3MDZmMTUxMGQ4MThlOGQ3NzJjM2EwZjRhYTI0NTk5NGQ1ZGQ0YzcxM2VjNTkwN2IzMjRmOWIzYjM0YjFlOGVlMjMxMDliYTNmNGE3Y2RlOWI4NTgzYWU2Zjc5MDU5ZjZkNDY2NThiYTNjOGY3MmUyNTE1Zjk4YmJmNWU6ZTNjMzZlMzQ5YWFkYzZhOWUwMTA2ZTkxODJhNTE0NjY"
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
    try:
        send_request = requests.post('http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/pubSub/unicast',
                                 headers=custom_header_crm, json=crm_inbox_payload)
        print(crm_inbox_payload)
        response = send_request.json()
        print(response)
    except Exception as e:
        logger.info("API request failed", e)
        raise
    logger.info("Received API response", response)
    request_id = crm_inbox_payload.get("requestId")
    grouping_key = crm_inbox_payload.get("appMessage", {}).get("groupingKey")
    sent_at = crm_inbox_payload.get("appMessage", {}).get("sentAt")
    expires_at = crm_inbox_payload.get("appMessage", {}).get("expiresAt")
    response_message_id = response.get("data", {}).get("messageId")
    capture_deviceid = device_id()
    logger.info("Received Response", response)
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
                                    "campaignId": "testcampaign1",
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
            'http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/pubSub/unicast', headers=custom_header_crm,
            json=payload)
        kill_response = send_kill_request.json()
        print(kill_response)
    except Exception as e:
        logger.info("API request is failed", e)
        raise
    logger.info("Received response", kill_response)
