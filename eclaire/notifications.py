# Copyright 2019 KOGAN.COM PTY LTD

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

# Small picture of a QL-570
EMOTICON = '<img src="https://dujrsrsgsd3nh.cloudfront.net/img/emoticons/41288/print-1438820995.png" width="20" height="20" alt="(print)" />'


def hipchat_notification(card, api_key, room, user, colour=None):
    """
    Send notification to a hipchat room that a card was printed
    """
    creator = card.actions[0]['memberCreator']['fullName'] if card.actions else None

    if creator is not None:
        # Attempt to get first name
        creator = creator.split()[0].split('@')[0]
        message = '{emote} &nbsp;<i>{creator}</i> printed <b><a href="{url}">{title}</a></b>.'.format(
            emote=EMOTICON,
            creator=creator,
            url=card.url,
            title=card.name,
        )
    else:
        message = '{emote} &nbsp;Printed <b><a href="{url}">{title}</a></b>'.format(
            emote=EMOTICON,
            url=card.url,
            title=card.name
        )

    hipchat_url = 'https://api.hipchat.com/v1/rooms/message?auth_token={api_key}&format=json'.format(
        api_key=api_key,
        )

    requests.post(
        hipchat_url,
        data={
            'room_id': room,
            'from': user,
            'message': message,
            'message_format': 'html',
            'color': colour or 'gray'
        }
    )
