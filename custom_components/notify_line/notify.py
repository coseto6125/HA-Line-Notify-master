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
from asyncio import run as asy_run

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from aiohttp import FormData, request
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
        asy_run(self.async_send_message(message, **kwargs))

    async def async_send_message(self, message="", **kwargs):
        if data := kwargs.get(ATTR_DATA):
            url = data.get(ATTR_URL)
            file_path = data.get(ATTR_FILE)
            stkpkgid = data.get(ATTR_STKPKGID)
            stkid = data.get(ATTR_STKID)

        else:
            url = file_path = stkpkgid = stkid = None

        headers = {"AUTHORIZATION": f"Bearer {self.access_token}"}

        payload = {
            "message": message,
            IMAGEFULLSIZE: url,
            IMAGETHURMBNAIL: url,
            STKPKID: stkpkgid,
            STKID: stkid,
        }

        data = FormData()
        for key, value in payload.items():
            if value:
                data.add_field(key, value)

        if file_path:
            data.add_field(IMAGEFILE, open(file_path, "rb"))

        async with request("POST", BASE_URL, headers=headers, data=data) as r:
            if r.status != 200:
                _LOGGER.error(await r.text())
