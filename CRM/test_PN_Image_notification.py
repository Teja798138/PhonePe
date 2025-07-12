import logging
import pytest
import requests
import time
from conftest import  get_userid_url, token_generate
import random
from datetime import datetime, timedelta
from Utilities.utils import device_id


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.crm
def test_crm_push_notification(call_crm_base_url, token_generate, get_userid_url):
    url = get_userid_url
    userid_header = {
        "Authorization": token_generate
    }
    send_request = requests.get(url, headers=userid_header)
    response = send_request.json()
    capture_userid = response.get("userId")
    random_integer = random.randint(10, 900)
    random_group_integer = random.randint(25, 980)
    fetch_device_id = device_id()
    request_id = f"Requeestb{random_integer}cbcb"
    message_id = f"Requeestb22cbcb{random_integer}"
    grouping_id = f"Requeestb22cbcb{random_group_integer}"
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
    crm_cta_payload = {
        "requestId": request_id,
        "userId": capture_userid,
        "profileId": "CONSUMER_PROMOTIONAL",
        "deviceId": fetch_device_id,
        "appMessage": {
            "version": 2,
            "messageId": message_id,
            "groupingKey": grouping_id,
            "source": {
                "type": "PHONEPE"
            },
            "data": {
                "placements": [
                    {
                        "scope": "DRAWER",
                        "template": {
                            "templateId": "TITLE_MESSAGE_IMAGE",
                            "templateParams": {
                                "value": {
                                    "image": "https://imgstatic.phonepe.com/images/notifications/900/480/notification-15-04-22-health999.png",
                                    "title": "Test",
                                    "message": "Starting at just ₹999*. Secure yourself against rising medical costs right away!",
                                    "headerSubText": "Test",
                                    "largeIconUrl": "https://imgstatic.phonepe.com/images/notifications/900/480/notification-15-04-22-health999.png",
                                    "fontColor": "red",
                                    "bgColor": "#F00000"
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "deepLinkIOS": "phonepe://sachetInsurance?category=HEALTH_INSURANCE&product=SIMPLE_HEALTH",
                                    "action_nav": "sachetInsuranceHome",
                                    "redirection_data": {
                                        "data": [
                                            {
                                                "key": "category",
                                                "value": "HEALTH_INSURANCE",
                                                "isEncoded": False
                                            },
                                            {
                                                "key": "productType",
                                                "value": "SIMPLE_HEALTH",
                                                "isEncoded": False
                                            }
                                        ]
                                    }
                                },
                                "callToAction": [
                                    {
                                        "text": "test",
                                        "action_nav": "sachetInsuranceHome",
                                        "redirection_data": {
                                            "data": [
                                                {
                                                    "key": "category",
                                                    "value": "HEALTH_INSURANCE",
                                                    "isEncoded": False
                                                },
                                                {
                                                    "key": "productType",
                                                    "value": "SIMPLE_HEALTH",
                                                    "isEncoded": False
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        "fallbackStrategy": "NONE",
                        "deferment": {
                            "type": "NONE",
                            "future": current_epoch_milliseconds,
                            "retryWindowInSec": 0
                        },
                        "nav": {
                            "key": "action_redirection",
                            "params": {
                                "deepLinkIOS": "phonepe://sachetInsurance?category=HEALTH_INSURANCE&product=SIMPLE_HEALTH",
                                "action_nav": "sachetInsuranceHome",
                                "redirection_data": {
                                    "data": [
                                        {
                                            "key": "category",
                                            "value": "HEALTH_INSURANCE",
                                            "isEncoded": False
                                        },
                                        {
                                            "key": "productType",
                                            "value": "SIMPLE_HEALTH",
                                            "isEncoded": False
                                        }
                                    ]
                                }
                            },
                            "callToAction": [
                                {
                                    "text": "PAY",
                                    "action_nav": "sachetInsuranceHome",
                                    "redirection_data": {
                                        "data": [
                                            {
                                                "key": "category",
                                                "value": "HEALTH_INSURANCE",
                                                "isEncoded": False
                                            },
                                            {
                                                "key": "productType",
                                                "value": "SIMPLE_HEALTH",
                                                "isEncoded": False
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ],
                "campaignId": "testCampaignBETAAutomation",
                "syncSections": [],
                "communicationIntent": "PROMOTIONAL",
                "utm_source": "marketing",
                "utm_medium": "push",
                "utm_campaign": "test123"
            },
            "properties": {
                "editable": True,
                "deletable": True,
                "override": True,
                "unsubscriptionSupported": False
            },
            "customParams": {
                "campaignId": "C121212",
                "interventionId": "12",
                "userId": capture_userid
            },
            "sentAt": one_day_ago_epoch,
            "expiresAt": current_epoch_milliseconds
        }
    }

    global send_request_id, response_message_id, grouping_key, sent_at, expires_at
    print(crm_cta_payload)
    try:
        send_request = requests.post('http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast',
                                     headers=custom_header_crm, json=crm_cta_payload)
        response = send_request.json()
        print(custom_header_crm)
        print(response)
        send_request_id = crm_cta_payload.get("requestId")
        grouping_key = crm_cta_payload.get("appMessage", {}).get("groupingKey")
        sent_at = crm_cta_payload.get("appMessage", {}).get("sentAt")
        expires_at = crm_cta_payload.get("appMessage", {}).get("expiresAt")
        response_message_id = response.get("data", {}).get("messageId")
    except Exception as e:
        logger.error("Failed to send Push Notification API", e)
        raise
    logger.info("Response received", response)

    time.sleep(20)
    capture_deviceid = device_id()
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
            'http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast', headers=custom_header_crm,
            json=payload)
        kill_response = send_kill_request.json()
        print(kill_response)
    except Exception as e:
        logger.error("Failed to send API request kill switch", e)
        raise
    logger.info("Response Received", kill_response)
