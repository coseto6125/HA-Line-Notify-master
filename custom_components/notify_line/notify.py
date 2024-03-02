"""
Custom component for Home Assistant to enable sending messages via Notify Line API.


Example configuration.yaml entry:

notify:
  - name: line_notification
    platform: notify_line
    access_token: 'line_access_token'

With this custom component loaded, you can send messaged to line Notify.
"""

import logging

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.notify import (
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_ACCESS_TOKEN

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://notify-api.line.me/api/notify"
ATTR_FILE = "file"
ATTR_URL = "url"
ATTR_STKPKGID = "stkpkgid"
ATTR_STKID = "stkid"
IMAGEFULLSIZE = "imageFullsize"
IMAGETHURMBNAIL = "imageThumbnail"
IMAGEFILE = "imageFile"
STKPKID = "stickerPackageId"
STKID = "stickerId"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
    }
)


def get_service(hass, config, discovery_info=None):
    """Get the Line notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    return LineNotificationService(access_token)


class LineNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, access_token):
        """Initialize the service."""
        self.access_token = access_token

    def send_message(self, message="", **kwargs):
        """Send some message."""
        if data := kwargs.get(ATTR_DATA):
            url = data.get(ATTR_URL)
            file = {IMAGEFILE: open(data.get(ATTR_FILE), "rb")}
            stkpkgid = data.get(ATTR_STKPKGID)
            stkid = data.get(ATTR_STKID)

        else:
            url = file = stkpkgid = stkid = None
        
        headers = {"AUTHORIZATION": f"Bearer {self.access_token}"}

        payload = {
            "message": message,
            IMAGEFULLSIZE: url,
            IMAGETHURMBNAIL: url,
            STKPKID: stkpkgid,
            STKID: stkid,
        }

        r = requests.post(BASE_URL, headers=headers, files=file, data=payload)
        if r.status_code != 200:
            _LOGGER.error(r.text)
