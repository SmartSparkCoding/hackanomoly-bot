import logging
from datetime import datetime
from datetime import timedelta

from slack_sdk.web.async_slack_response import AsyncSlackResponse

from nephthys.utils.env import env


USER_PROFILE_CACHE_TTL = timedelta(minutes=5)
_user_profile_cache: dict[str, tuple["UserProfileWrapper", datetime]] = {}


class UserProfileWrapper:
    def __init__(self, users_info_response: AsyncSlackResponse):
        user_data = users_info_response.get("user")
        if not user_data:
            raise ValueError(f"Slack user not found: {users_info_response}")
        self.raw_data = user_data

    def display_name(self) -> str:
        display_name = (
            self.raw_data["profile"].get("display_name")
            or self.raw_data["profile"].get("real_name")
            or self.raw_data["name"]
        )
        if not display_name:
            logging.error(
                f"SOMETHING HAS GONE TERRIBLY WRONG - user has no username: {self.raw_data}"
            )
            return ""
        return display_name

    def profile_pic_512x(self) -> str | None:
        return self.raw_data["profile"].get("image_512")


async def get_user_profile(slack_id: str) -> UserProfileWrapper:
    """Retrieve the user's display name from Slack given their Slack ID."""
    cached = _user_profile_cache.get(slack_id)
    now = datetime.now()
    if cached and now - cached[1] < USER_PROFILE_CACHE_TTL:
        return cached[0]

    response = await env.slack_client.users_info(user=slack_id)
    profile = UserProfileWrapper(response)
    _user_profile_cache[slack_id] = (profile, now)
    return profile
