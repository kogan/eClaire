import requests

# Small picture of a QL-570
EMOTICON = '<img src="https://dujrsrsgsd3nh.cloudfront.net/img/emoticons/41288/print-1438820995.png" width="20" height="20" alt="(print)" />'  # noqa


def hipchat_notification(card, api_key, room, user, colour=None):
    """
    Send notification to a hipchat room that a card was printed
    """
    creator = card.actions[0]["memberCreator"]["fullName"] if card.actions else None

    if creator is not None:
        # Attempt to get first name
        creator = creator.split()[0].split("@")[0]
        message = '{emote} &nbsp;<i>{creator}</i> printed <b><a href="{url}">{title}</a></b>.'.format(
            emote=EMOTICON, creator=creator, url=card.url, title=card.name
        )
    else:
        message = '{emote} &nbsp;Printed <b><a href="{url}">{title}</a></b>'.format(
            emote=EMOTICON, url=card.url, title=card.name
        )

    hipchat_url = "https://api.hipchat.com/v1/rooms/message?auth_token={api_key}&format=json".format(
        api_key=api_key
    )

    requests.post(
        hipchat_url,
        data={
            "room_id": room,
            "from": user,
            "message": message,
            "message_format": "html",
            "color": colour or "gray",
        },
    )
