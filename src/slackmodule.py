import json
from urllib import parse, request

__all__ = ["find_public_channels", "post_message"]

BASE_API_URL = "https://slack.com/api"
CHANNELS_URL = BASE_API_URL + "/conversations.list"
POST_MESSAGE_URL = BASE_API_URL + "/chat.postMessage"


def find_public_channels(token) -> list:
    params = {"token": token, "types": "public_channel"}

    # MEMO 公開チャンネル全部取ってるので時間掛かる＆メモリ消費する
    channels = []
    while True:
        res_dict = __request_api(CHANNELS_URL, params)
        if not res_dict:
            return list()

        channels.extend(res_dict["channels"])
        nextcursor = res_dict["response_metadata"]["next_cursor"]
        if not nextcursor:
            break
        params["cursor"] = nextcursor

    return channels


def __request_api(url, params) -> dict:
    req = request.Request("{}?{}".format(url, parse.urlencode(params)))
    with request.urlopen(req) as res:
        body = res.read()

    try:
        res_dict = json.loads(body)
    except Exception:
        return dict()
    return res_dict


def post_message(token, channel_id, text) -> dict:
    params = {"token": token, "channel": channel_id, "text": text}

    return __request_api(POST_MESSAGE_URL, params)
