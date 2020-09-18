from datetime import datetime, timedelta
import os
import sys
import copy

from slackmodule import find_public_channels, post_message


class Channels:
    def __init__(self, channel_arr) -> None:
        self.channels = channel_arr

    def has_channels(self) -> bool:
        return self.length() != 0

    def get_list(self) -> list:
        return copy.deepcopy(self.channels) if self.has_channels() else []

    def length(self) -> int:
        return len(self.channels)

    def new_channels(self) -> "Channels":
        return self.channel_elapsed_from_creation(7)

    def channel_elapsed_from_creation(self, days) -> "Channels":
        target_date = datetime.today() - timedelta(days=days)
        target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        print("target_date:" + str(target_date))

        channel_dict = self.channels
        new_channels = []
        for channel in channel_dict:

            created = datetime.fromtimestamp(channel["created"])
            is_archived = channel["is_archived"]
            if created < target_date:
                continue
            elif is_archived:
                continue

            new_channels.append(channel)
        return Channels(new_channels)


def handler(event, context) -> None:
    token = os.environ["TOKEN"]
    channel_id = os.environ["CHANNEL_ID"]
    slack_domain = os.environ["SLACK_DOMAIN"]

    execute(token, channel_id, slack_domain)


def execute(token, channel_id, slack_domain) -> None:
    channels = Channels(find_public_channels(token))
    channels = channels.new_channels()

    message = "週間新着チャンネルをお届け！\r\n\r\n"
    if channels.length() > 0:
        message += to_messages(channels, slack_domain)
    else:
        message += "...新着は無かったよ...またね..."
    print(message)

    if channel_id:
        post_message(token, channel_id, message)


def to_messages(channels, slack_domain) -> str:
    crlf = "\r\n"
    message = ""
    for channel in sorted(channels.get_list(), key=lambda channel: channel["created"]):
        message += "#" + channel["name"]
        message += " : " + str(datetime.fromtimestamp(channel["created"])) + " : "
        message += channel["purpose"]["value"]
        message += crlf

        if slack_domain:
            message += "https://" + str(slack_domain) + "/archives/" + str(channel["id"])
            message += crlf

        message += "---"
        message += crlf
    message += "channel_count:" + str(channels.length())
    return message


if __name__ == "__main__":
    args = sys.argv
    token = args[1]  # slack token
    channel_id = args[2]  # 通知先チャンネルID
    slack_domain = args[3]  # 通知先サブドメイン hogehoge.slack.com
    execute(token, channel_id, slack_domain)
