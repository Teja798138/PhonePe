import logging
import pytest
import requests
from conftest import  get_userid_url, token_generate
from Utilities.utils import device_id
import random
from datetime import datetime, timedelta
import time


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.rewards_nudge
def test_offers_nudge(call_crm_base_url, token_generate, get_userid_url):
    url = get_userid_url
    userid_header = {
        "Authorization": token_generate
    }
    try:
        send_request_userid = requests.get(url, headers=userid_header)
        response_userid = send_request_userid.json()
        capture_userid = response_userid.get("userId")
    except Exception as e:
        logger.info("API request is failed", e)
        raise
    logger.info("Received API response ", response_userid)
    fetch_device_id = device_id()
    generate_message = random.randint(102, 940)
    generate_groupingkey = random.randint(110,870)
    generate_priority = random.randint(1000, 8000)
    generate_requestid = random.randint(102,980)
    message_id = f"RE{generate_message}"
    request_id = f"RE{generate_requestid}"
    grouping_id = f"RE{generate_groupingkey}"
    priority = f"{generate_priority}"
    current_epoch_milliseconds = int((datetime.now() + timedelta(minutes=5)).timestamp() * 1000)
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_ago_epoch = int(time.mktime(one_day_ago.timetuple()) * 1000)
    offer_header = {
        "Authorization":token_generate,
        "Content-Type":"application/json"
    }
    offer_payload = {
        "requestId": request_id,
        "userId": capture_userid,
        "deviceId": fetch_device_id,
        "profileId": "CONSUMER_TRANSACTIONAL",
        "appMessage": {
            "messageId": message_id,
            "groupingKey": grouping_id,
            "source": {
                "type": "PHONEPE"
            },
            "data": {
                "placements": [
                    {
                        "tags": [
                            "REWARDS_V3"
                        ],
                        "template": {
                            "templateId": "INAPP_WIDGET",
                            "templateParams": {
                                "value": {
                                    "title": {
                                        "defaultValue": "default_title",
                                        "translationKey": "REWARDS_NUDGE_POPULAR_OFFERS",
                                        "translationTag": "general_messages_v2"
                                    },
                                    "subTitle": {
                                        "defaultValue": "Test Get upto 25% off",
                                        "translationKey": "REWARDS_NUDGE_SUBTITLE",
                                        "translationTag": "general_messages_v2"
                                    },
                                    "recommendationStrategy": "PAYDAY",
                                    "background": "",
                                    "icon": "https://imgstatic.phonepe.com/images/phonepeconsumer/v3/light/bento/m/500/500/home-rewards.png",
                                    "tickerCount": 11,
                                    "tagLabel": {
                                        "defaultValue": "8 New",
                                        "translationKey": "REWARDS_TESTNUDGE_NEW",
                                        "translationTag": "general_messages_v2"
                                    },
                                    "layoutId": "default",
                                    "priority": priority
                                }
                            },
                            "templateGroupParams": {
                                "value": {}
                            }
                        },
                        "fallbackStrategy": "NONE",
                        "deferment": {
                            "type": "NONE"
                        },
                        "expiresAt": current_epoch_milliseconds,
                        "active": True,
                        "scope": "WIDGET"
                    }
                ],
                "campaignId": "CM2204131951551550343789",
                "syncSections": [],
                "communicationIntent": "TRANSACTIONAL",
                "utm_source": "Push",
                "utm_medium": "Hawkeye",
                "utm_campaign": "HE@CM2204131951551550343789@1@d675e16c-8285-455a-8649-1046d3098c50"
            },
            "properties": {
                "editable": True,
                "deletable": True,
                "override": True,
                "unsubscriptionSupported": False
            },
            "customParams": {
                "customTag2": "1",
                "customTag1": capture_userid,
                "customTag4": "HE@CM2204131951551550343789@1@d675e16c-8285-455a-8649-1046d3098c50",
                "customTag3": capture_userid,
                "customTag5": ""
            },
            "sentAt": one_day_ago_epoch,
            "expiresAt": current_epoch_milliseconds,
            "version": 2,
            "updateGroup": False,
            "destination": {
                "mailboxName": "CONSUMER_U2404051214212395591233@zencast",
                "type": "USER_RESTRICTED"
            }
        }
    }
    try:
        send_request = requests.post('http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast', headers=offer_header, json=offer_payload)
        print(offer_payload)
        response = send_request.json()
        print(response)
    except Exception as e:
        logger.error("API request is failed", e)
        raise
    logger.info("Response Received", response)
