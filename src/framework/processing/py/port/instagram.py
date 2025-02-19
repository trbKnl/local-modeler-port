"""
DDP Instagram module

This module contains functions to handle *.jons files contained within an instagram ddp
"""

import logging

import pandas as pd

import port.helpers.extraction_helpers as eh
from port.helpers.validate import (
    DDPCategory,
    DDPFiletype,
    Language,
)


logger = logging.getLogger(__name__)

DDP_CATEGORIES = [
    DDPCategory(
        id="json_en",
        ddp_filetype=DDPFiletype.JSON,
        language=Language.EN,
        known_files=[
            "secret_conversations.json",
            "personal_information.json",
            "account_privacy_changes.json",
            "account_based_in.json",
            "recently_deleted_content.json",
            "liked_posts.json",
            "stories.json",
            "profile_photos.json",
            "followers.json",
            "signup_information.json",
            "comments_allowed_from.json",
            "login_activity.json",
            "your_topics.json",
            "camera_information.json",
            "recent_follow_requests.json",
            "devices.json",
            "professional_information.json",
            "follow_requests_you've_received.json",
            "eligibility.json",
            "pending_follow_requests.json",
            "videos_watched.json",
            "ads_interests.json",
            "account_searches.json",
            "following.json",
            "posts_viewed.json",
            "recently_unfollowed_accounts.json",
            "post_comments.json",
            "account_information.json",
            "accounts_you're_not_interested_in.json",
            "use_cross-app_messaging.json",
            "profile_changes.json",
            "reels.json",
        ],
    )
]


def accounts_not_interested_in_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "accounts_you're_not_interested_in.json")
    d = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = d["impressions_history_recs_hidden_authors"] #pyright: ignore
        for item in items:
            data = item.get("string_map_data", {})
            account_name = data.get("Username", {}).get("value", ""),

            datapoints.append((
                account_name,
            ))
        out = pd.DataFrame(datapoints, columns=["Account naam"]) #pyright: ignore

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out


def posts_viewed_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "posts_viewed.json")
    d = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = d["impressions_history_posts_seen"] #pyright: ignore
        for item in items:
            data = item.get("string_map_data", {})
            account_name = data.get("Author", {}).get("value", "")
            timestamp = eh.epoch_to_iso(data.get("Time", {}).get("timestamp", None))

            datapoints.append((
                account_name,
                timestamp,
            ))
        out = pd.DataFrame(datapoints, columns=["Auteur", "Datum en tijd"]) #pyright: ignore
        #out = out.groupby('Auteur').size().reset_index(name='Aantal')
        #out = out.sort_values(by="Aantal", ascending=False).reset_index(drop=True)

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out



def posts_not_interested_in_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "posts_you're_not_interested_in.json")
    data = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = data["impressions_history_posts_not_interested"] #pyright: ignore
        for item in items:
            d = eh.dict_denester(item.get("string_list_data"))
            datapoints.append((
                eh.fix_latin1_string(eh.find_item(d, "value")),
                eh.find_item(d, "href"),
                eh.epoch_to_iso(eh.find_item(d, "timestamp"))
            ))
        out = pd.DataFrame(datapoints, columns=["Post", "Link", "Date"]) #pyright: ignore
        out = out.sort_values(by="Date", key=eh.sort_isotimestamp_empty_timestamp_last)

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out



def videos_watched_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "videos_watched.json")
    d = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []
    try:
        items = d["impressions_history_videos_watched"] #pyright: ignore
        for item in items:
            data = item.get("string_map_data", {})
            account_name = data.get("Author", {}).get("value", "")
            timestamp = eh.epoch_to_iso(data.get("Time", {}).get("timestamp", None))

            datapoints.append((
                account_name,
                timestamp
            ))
        out = pd.DataFrame(datapoints, columns=["Auteur", "Datum en tijd"]) #pyright: ignore
        #out = out.groupby('Auteur').size().reset_index(name='Aantal')
        #out = out.sort_values(by="Aantal", ascending=False).reset_index(drop=True)

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out


def post_comments_to_df(instagram_zip: str) -> pd.DataFrame:
    """
    You can have 1 to n files of post_comments_<x>.json
    """

    out = pd.DataFrame()
    datapoints = []
    i = 1

    while True:
        b = eh.extract_file_from_zip(instagram_zip, f"post_comments_{i}.json")
        d = eh.read_json_from_bytes(b)

        if not d:
            break

        try:
            for item in d:
                data = item.get("string_map_data", {})
                media_owner = data.get("Media Owner", {}).get("value", "")
                timestamp = eh.epoch_to_iso(data.get("Time", {}).get("timestamp", None))
                if media_owner != "":
                    datapoints.append((
                        media_owner,
                        timestamp,
                    ))
            i += 1

        except Exception as e:
            logger.error("Exception caught: %s", e)
            return pd.DataFrame()

    out = pd.DataFrame(datapoints, columns=["Auteur", "Datum en tijd"]) #pyright: ignore
    #out = out.groupby('Auteur').size().reset_index(name='Aantal')
    #out = out.sort_values(by="Aantal", ascending=False).reset_index(drop=True)

    return out



def following_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "following.json")
    data = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = data["relationships_following"] # pyright: ignore
        for item in items:
            d = eh.dict_denester(item)
            datapoints.append((
                eh.fix_latin1_string(eh.find_item(d, "value")),
            ))
        out = pd.DataFrame(datapoints, columns=["Account naam"]) #pyright: ignore

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out


def n_following_followers_to_df(instagram_zip: str):

    b = eh.extract_file_from_zip(instagram_zip, "following.json")
    data = eh.read_json_from_bytes(b)
    unknown_value = "Unknown"

    following_count = unknown_value
    followers_count = unknown_value
    i = 1

    try:
        items = data["relationships_following"] # pyright: ignore
        following_count = len(items)

    except Exception as e:
        logger.error("Could not determine the number of following: %s", e)
        following_count = unknown_value

    b = eh.extract_file_from_zip(instagram_zip, f"followers_{i}.json")
    d = eh.read_json_from_bytes(b)
    if d:
        followers_count = 0

        while True and d:
            try:
                followers_count += len(d)

            except Exception as e:
                logger.error("Could not determine the number of followers: %s", e)
                followers_count = unknown_value
                break

            i += 1
            b = eh.extract_file_from_zip(instagram_zip, f"followers_{i}.json")
            d = eh.read_json_from_bytes(b)

    out = pd.DataFrame([(following_count, followers_count)], columns=["Aantal volgend", "Aantal volgers"]) #pyright: ignore
    return out, (following_count, followers_count)



def liked_comments_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "liked_comments.json")
    data = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = data["likes_comment_likes"] #pyright: ignore
        for item in items:
            d = eh.dict_denester(item)
            datapoints.append((
                eh.fix_latin1_string(eh.find_item(d, "title")),
                eh.fix_latin1_string(eh.find_item(d, "value")),
                eh.epoch_to_iso(eh.fix_latin1_string(eh.find_item(d, "timestamp"))),
            ))
        out = pd.DataFrame(datapoints, columns=["Account naam", "Waarde", "Datum en tijd"]) #pyright: ignore
        #out = out.groupby(['Account naam', 'Value']).size().reset_index(name='Aantal')
        #out = out.sort_values(by="Aantal", ascending=False).reset_index(drop=True)

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out


def liked_posts_to_df(instagram_zip: str) -> pd.DataFrame:

    b = eh.extract_file_from_zip(instagram_zip, "liked_posts.json")
    data = eh.read_json_from_bytes(b)

    out = pd.DataFrame()
    datapoints = []

    try:
        items = data["likes_media_likes"] #pyright: ignore
        for item in items:
            d = eh.dict_denester(item)
            datapoints.append((
                eh.fix_latin1_string(eh.find_item(d, "title")),
                eh.fix_latin1_string(eh.find_item(d, "value")),
                eh.epoch_to_iso(eh.fix_latin1_string(eh.find_item(d, "timestamp"))),
            ))
        out = pd.DataFrame(datapoints, columns=["Account naam", "Waarde", "Datum en tijd"]) #pyright: ignore
        #out = out.groupby(['Account naam', 'Value']).size().reset_index(name='Aantal') #pyright: ignore
        #out = out.sort_values(by="Aantal", ascending=False).reset_index(drop=True)

    except Exception as e:
        logger.error("Exception caught: %s", e)

    return out

