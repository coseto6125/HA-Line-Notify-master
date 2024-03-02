# HA Line Notify

Line Notify custom component for Home Assistant.

Line is a messaging application widely used in Asia. It has notification service called "Line Notify" which you can use their API to send messages and media to your Line account. This integration let you send message, image and sticker to your Line account with Home Assistant.

This integration is almost based on this [repository](https://github.com/yun-s-oh/Homeassistant/tree/master/custom_components/notify_line) and [this article](https://community.home-assistant.io/t/line-notify-api-integration/56328), but it seems to inactive and contains few errors. I fixed those and add proper documentation.

## Installation

1.  [Obtain Line Notify personal token.](https://notify-bot.line.me/en/)
2.  Copy `notify_line`folder from `custom_components` to your custom_components in Home Assistant directory.
3.  Add configuration to configuration.yaml

```
notify:
  - name: line_notification
    platform: notify_line
    access_token: 'PASTE_YOUR_PERSONAL_TOKEN_HERE'
```

4. Reboot your Home Assistant instance.
5. Call `notify.line_notification`(with `service data` described below) from script or automation as you desire.

## Supported data

Service data can be added in order to send message, image and sticker.

| Key        | Example value                   | Description                         |
| :--------- | :------------------------------ | :---------------------------------- |
| `message ` | `Hello`                         | Message to be sent out to recipient |
| `file`     | `/config/tmp/test.jpg`          | Directory of image file             |
| `url`      | `https://picsum.photos/600/400` | URL of image file                   |
| `stkpkgid` | `1`                             | Sticker package ID                  |
| `stkid`    | `2`                             | Sticker ID                          |

In order to send sticker, `stkpkgid` and `stkid` must be used together. List of sticker package ID and Sticker ID can be found [here](https://devdocs.line.me/files/sticker_list.pdf).

JPG and PNG image format are support, but you have to either choose to send with a file or url per round.

## Example

**Test call with service developer tools**
![test call](https://raw.githubusercontent.com/maxmacstn/HA-Line-Notify/master/sample_show.png)

**Send Camera Snapshot to Line when something was triggered.**

configuration.yaml

```
notify:
  - name: line_notification
    platform: notify_line
    access_token: 'PASTE_YOUR_PERSONAL_TOKEN_HERE'

homeassistant:
  whitelist_external_dirs:
    - /tmp
```

Note: You need to add whitelist directory in order to save camera image snapshot.

script.yaml

```
'send_line_notify':
  alias: Send Line notify
  sequence:
 - data:
      filename: /tmp/snapshot.jpg
    entity_id: camera.living_room
    service: camera.snapshot
 - delay: '2'
 - data:
      message: Snapshot from living room camera.
      data:
        file: /tmp/snapshot.jpg
    service: notify.line_notification
```

## To-Do

-   Multi-user support : let each user input their own token upon service call.
-   Simple login: using OAuth to obtain token from Line Notify API.

## Declaration

-   The above content is sourced from https://github.com/maxmacstn/HA-Line-Notify.
-   This git repository is optimized for certain core code and is primarily intended for personal use.
-   by coseto
