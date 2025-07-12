import logging
import time
import pytest
import requests
from conftest import  get_userid_url, token_generate
from Utilities.utils import device_id
import random
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.androidcrm
def test_android_crm(call_crm_base_url, token_generate, get_userid_url):
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
    random_integer = random.randint(11, 98)
    random_message_id = random.randint(14, 88)
    random_grouping_id = random.randint(17, 93)
    fetch_device_id = device_id()
    request_id = f"RSF-Ssatyam-G{random_integer}G4"
    message_id = f"M1G-5483GP-{random_message_id}TG"
    grouping_key = f"G2G-5483GP-{random_grouping_id}TG"
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
    crm_PN_and_inbox_Android = {
        "requestId": request_id,
        "userId": capture_userid,
        "deviceId": fetch_device_id,
        "profileId": "CONSUMER_TRANSACTIONAL",
        "appMessage": {
            "messageId": message_id,
            "groupingKey": grouping_key,
            "authorisedFor": capture_userid,
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
                                    "title": "Hi Satyam- Hit The Pay Button",
                                    "message": "Starting at just ₹999*. Secure yourself against rising medical costs right away!",
                                    "headerSubText": "{{templatePush}}",
                                    "largeIconUrl": "https://imgstatic.phonepe.com/images/notifications/900/480/notification-15-04-22-health999.png",
                                    "fontColor": "red",
                                    "bgColor": "#f00000"
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "deepLinkIOS": "phonepe://sachetInsurance?category=HEALTH_INSURANCE&product=SIMPLE_HEALTH",
                                    "deepLinkAndroid": "phonepe://externalapp?externalAppMeta=ewogICAgICAgICJwYWNrYWdlTmFtZSI6ImNvbS5pbmR1cy5hcHBzdG9yZSIsCiAgICAgICAgImRlZmF1bHRSZWRpcmVjdGlvblVybCI6Imh0dHBzOi8vaWFzLm9uZWxpbmsubWUvajN6by85cWJxaTFyOSIsCiAgICAgICAgImRlZXBsaW5rIjoiaHR0cHM6Ly9pYXMub25lbGluay5tZS9qM3pvLzlxYnFpMXI5IgoKfQ==",
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
                                "callToAction": [{
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
                                }]
                            }
                        },
                        "fallbackStrategy": "NONE",
                        "deferment": {
                            "type": "FIXED_DELAY",
                            "minutes": 3
                        },
                        "expiresAt": current_epoch_milliseconds,
                        "nav": {
                            "key": "action_redirection",
                            "params": {
                                "deepLinkIOS": "phonepe://sachetInsurance?category=HEALTH_INSURANCE&product=SIMPLE_HEALTH",
                                "deepLinkAndroid": "phonepe://externalapp?externalAppMeta=ewogICAgICAgICJwYWNrYWdlTmFtZSI6ImNvbS5pbmR1cy5hcHBzdG9yZSIsCiAgICAgICAgImRlZmF1bHRSZWRpcmVjdGlvblVybCI6Imh0dHBzOi8vd3d3LmluZHVzYXBwc3RvcmUuY29tLyIsCiAgICAgICAgImRlZXBsaW5rIjoiaHR0cHM6Ly9pYXMub25lbGluay5tZS9qM3pvLzlxYnFpMXI5IgoKfQ==",
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
                            "callToAction": [{
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
                            }]
                        },
                        "properties": {
                            "visibilityImportance": "URGENT"
                        }
                    },
                    {
                        "category": "ANNOUNCEMENT",
                        "scope": "INTERSTITIAL",
                        "restrictions": {
                            "maxAttempts": 2,
                            "coolOffDuration": {
                                "timeSpec": "MINUTE",
                                "units": 1
                            }
                        },
                        "template": {
                            "templateId": "HTML",
                            "templateParams": {
                                "value": {
                                    "url": "https://www.phonepe.com/apollo/emailers/2023/june/05/central-mapper-popup/en.html",
                                    "dismissable": False
                                }
                            }
                        },
                        "fallbackStrategy": "NONE",
                        "deferment": {
                            "type": "NONE"
                        },
                        "expiresAt": current_epoch_milliseconds,
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
                    },
                    {
                        "scope": "INBOX",
                        "template": {
                            "templateId": "ICON_TITLE_SUBTITLE",
                            "templateParams": {
                                "value": {
                                    "title": "SATYAM_INTERVENTION",
                                    "subTitle": "Click here",
                                    "iconURL": "https://imgstatic.phonepe.com/images/app-icons/wealth-management/mutual-funds/providers/{height}/{width}/SUPER_FUND_AGGRESSIVE.png"
                                }
                            },
                            "nav": {
                                "key": "action_redirection",
                                "params": {
                                    "deepLinkIOS": "phonepestage://dg?providerId=SAFEGOLD",
                                    "deepLinkAndroid": "phonepe://externalapp?externalAppMeta=ewogICAgICAgICJwYWNrYWdlTmFtZSI6ImNvbS5waG9uZXBlLnN0b2NrYnJva2luZyIsCiAgICAgICAgImRlZmF1bHRSZWRpcmVjdGlvblVybCI6Imh0dHBzOi8vc2hhcmVtYXJrZXQub25lbGluay5tZS91TUhaL2Rpd2FsaTIzbXVodXJhdCIsCiAgICAgICAgImRlZXBsaW5rIjoiaHR0cHM6Ly9zaGFyZW1hcmtldC5vbmVsaW5rLm1lL3VNSFovZGl3YWxpMjNtdWh1cmF0IgoKfQ==",
                                    "action_nav": "genReactContainer",
                                    "redirection_data": {
                                        "data": [
                                            {
                                                "key": "bundleName",
                                                "isEncoded": "false",
                                                "value": "brickbatbridge"
                                            },
                                            {
                                                "key": "config",
                                                "isEncoded": "false",
                                                "value": "brickbatbridge"
                                            }
                                        ]
                                    }
                                }
                            }
                        },
                        "deferment": None
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
                "customTag1": "CM2204131951551550343789",
                "customTag4": "HE@CM2204131951551550343789@1@d675e16c-8285-455a-8649-1046d3098c50",
                "customTag3": capture_userid,
                "customTag5": ""
            },
            "sentAt": one_day_ago_epoch,
            "expiresAt": current_epoch_milliseconds,
            "version": 2,
            "destination": {
                "mailboxName": "CONSUMER_U2302161303194695860743@zencast",
                "type": "USER_RESTRICTED"
            }
        }
    }
    try:
        send_request = requests.post('http://zencast.nixy.stg-drove.phonepe.nb6/v1/communication/send/push/unicast',
                                 headers=custom_header_crm, json=crm_PN_and_inbox_Android)
        print(crm_PN_and_inbox_Android)
        response = send_request.json()
        print(send_request)
    except Exception as e:
        logger.info("API request failed", e)
        raise
    logger.info("Received Response", response)
    request_id = crm_PN_and_inbox_Android.get("requestId")
    response_message_id = response.get("data", {}).get("messageId")
    grouping_key = crm_PN_and_inbox_Android.get("appMessage", {}).get("groupingKey")
    sent_at = crm_PN_and_inbox_Android['appMessage']['sentAt']
    expires_at = crm_PN_and_inbox_Android['appMessage']['expiresAt']
    print(response)
    time.sleep(30)
    capture_deviceid = device_id()
    user_id = capture_userid
    payload = {
        "requestId": request_id,
        "entityId": user_id,
        "deviceId": capture_deviceid,
        "profileId": "CONSUMER_TRANSACTIONAL",
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
                                    "campaignId": "CM2204131951551550343789",
                                    "scope": "CAMPAIGN",
                                    "placements": ["DRAWER,INBOX,INTERSTITIAL"]
                                }
                            }
                        }
                    }
                ],
                "placements": [],
                "campaignId": "CM2204131951551550343789",
                "communicationIntent": "TRANSACTIONAL",
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
        logger.info("API request failed", e)
        raise
    logger.info("Response Received", response)
